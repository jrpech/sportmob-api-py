from collections import defaultdict
from datetime import date, datetime, time, timedelta
from typing import DefaultDict, Dict, List, Optional, Set, Tuple

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cancha import Cancha
from app.models.config_calendar import ConfigCalendar
from app.models.equipo import Equipo as EquipoModel
from app.models.fechas import Fechas
from app.models.horarios import Horarios
from app.models.jornadas import Jornadas
from app.models.jugador_equipo import JugadorEquipo
from app.models.partidos_jornadas import PartidosJornadas
from app.models.relations_calendar import RelationsCalendar
from app.models.torneo import Torneo
from app.models.torneo_disponibilidad_jugador import TorneoDisponibilidadJugador
from app.schemas import BaseResponse
from app.services.scheduling_dtos import (
    DisponibilidadJugador,
    Equipo,
    Espacio,
    Grupo,
    MotivoPartidoPendiente,
    Partido,
    PartidoPendiente,
    ResultadoCalendario,
    construir_disponibilidad_equipo,
    construir_disponibilidad_jugador,
    construir_disponibilidad_partido,
    generar_partidos_round_robin,
    programar_partidos_greedy,
)


router = APIRouter(prefix="/api/Scheduler", tags=["Scheduler"])

GRUPO_GENERAL_ID = 19283890
GRUPO_INICIAL_DIVIDIDO_ID = 19283891


class ProgramarPartidosGreedyBody(BaseModel):
    canchas_ids: List[int] = Field(default_factory=list)
    torneos_ids: List[int] = Field(default_factory=list)


def _parse_datetime_value(raw_value: Optional[str]) -> Optional[datetime]:
    if not raw_value:
        return None

    value = raw_value.strip()
    formats = (
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _parse_time_value(raw_value: Optional[str]) -> Optional[time]:
    if not raw_value:
        return None

    value = raw_value.strip()
    formats = (
        "%H:%M:%S",
        "%H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    )
    for fmt in formats:
        try:
            parsed = datetime.strptime(value, fmt)
            return parsed.time()
        except ValueError:
            continue

    try:
        parsed_iso = datetime.fromisoformat(value)
        return parsed_iso.time()
    except ValueError:
        return None


def _normalizar_dia_semana(value: Optional[str]) -> Optional[int]:
    if not value:
        return None

    dia = value.strip().lower()
    mapping = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "sábado": 5,
        "domingo": 6,
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    return mapping.get(dia)


def _construir_espacios(
    canchas: List[Cancha],
    fechas: List[Fechas],
    horarios: List[Horarios],
    fecha_min: date,
    fecha_max: date,
) -> List[Espacio]:
    cancha_por_id = {cancha.ID: cancha for cancha in canchas}

    horarios_por_fecha: Dict[int, List[Horarios]] = {}
    for horario in horarios:
        horarios_por_fecha.setdefault(horario.fechaID, []).append(horario)

    espacios: List[Espacio] = []
    seen_keys: Set[Tuple[int, date, str]] = set()
    espacio_id = 1
    current = fecha_min
    while current <= fecha_max:
        weekday = current.weekday()
        for fecha_cfg in fechas:
            if _normalizar_dia_semana(fecha_cfg.dia) != weekday:
                continue

            cancha = cancha_por_id.get(fecha_cfg.canchaID)
            if cancha is None:
                continue

            for horario in horarios_por_fecha.get(fecha_cfg.id, []):
                time_value = _parse_time_value(horario.horario)
                if time_value is None:
                    continue

                hora = time_value.strftime("%H:%M")
                dedupe_key = (cancha.ID, current, hora)
                if dedupe_key in seen_keys:
                    continue
                seen_keys.add(dedupe_key)

                fecha_hora = datetime.combine(current, time_value)
                espacios.append(
                    Espacio(
                        espacio_id=espacio_id,
                        cancha_id=cancha.ID,
                        fecha=current,
                        hora=hora,
                        fecha_hora=fecha_hora,
                        cuenta_id=cancha.cuentaId or 0,
                    )
                )
                espacio_id += 1
        current += timedelta(days=1)

    return espacios


def _construir_grupos_torneo(torneo: Torneo, equipos: List[Equipo]) -> List[Grupo]:
    grupos: List[Grupo] = []
    dividir = bool(torneo.dividirRR)

    if dividir:
        no_grupos = torneo.noGruposRR or 2
        for i in range(no_grupos):
            grupo_id = GRUPO_INICIAL_DIVIDIDO_ID + i
            equipos_grupo = [equipo for equipo in equipos if equipo.grupo_rr == grupo_id]
            grupos.append(Grupo(grupo_id=grupo_id, torneo_id=torneo.id, equipos=equipos_grupo))
    else:
        equipos_grupo = [equipo for equipo in equipos if equipo.grupo_rr == GRUPO_GENERAL_ID]
        if not equipos_grupo:
            equipos_grupo = equipos
        grupos.append(Grupo(grupo_id=GRUPO_GENERAL_ID, torneo_id=torneo.id, equipos=equipos_grupo))

    return grupos


def _construir_disponibilidad_jugadores_desde_db(
    disponibilidades_db: List[TorneoDisponibilidadJugador],
    espacios: List[Espacio],
) -> List[DisponibilidadJugador]:
    espacios_ids_por_fecha_hora: Dict[Tuple[date, str], Set[int]] = {}
    for espacio in espacios:
        key = (espacio.fecha, espacio.hora)
        espacios_ids_por_fecha_hora.setdefault(key, set()).add(espacio.espacio_id)

    disponibilidades: List[DisponibilidadJugador] = []
    for item in disponibilidades_db:
        fecha_item = item.fecha.date()
        hora_value = _parse_time_value(item.hora)
        if hora_value is None:
            hora_value = item.fecha.time()
        hora_item = hora_value.strftime("%H:%M")
        key = (fecha_item, hora_item)
        espacios_disponibles = list(espacios_ids_por_fecha_hora.get(key, set()))

        disponibilidades.append(
            DisponibilidadJugador(
                torneo_id=item.idTorneo,
                jugador_id=item.idJugador,
                espacios_disponibles=espacios_disponibles,
            )
        )

    return disponibilidades


def _parse_torneos_ids_value(raw_value: Optional[str]) -> List[int]:
    if not raw_value:
        return []

    torneo_ids: List[int] = []
    for token in raw_value.split(","):
        value = token.strip()
        if not value:
            continue
        torneo_ids.append(int(value))

    return sorted(set(torneo_ids))


def _construir_espacios_desde_relaciones(
    relaciones: List[RelationsCalendar],
    cuenta_por_cancha: Dict[int, int],
) -> List[Espacio]:
    espacios_tmp: List[Tuple[date, str, int, datetime, int]] = []
    seen_keys: Set[Tuple[int, date, str]] = set()

    for relacion in relaciones:
        hora_value = _parse_time_value(relacion.hora)
        if hora_value is None:
            hora_value = relacion.fecha.time()

        hora = hora_value.strftime("%H:%M")
        fecha_slot = relacion.fecha.date()
        dedupe_key = (relacion.canchaID, fecha_slot, hora)
        if dedupe_key in seen_keys:
            continue
        seen_keys.add(dedupe_key)

        espacios_tmp.append(
            (
                fecha_slot,
                hora,
                relacion.canchaID,
                datetime.combine(fecha_slot, hora_value),
                cuenta_por_cancha.get(relacion.canchaID, 0),
            )
        )

    espacios_tmp.sort(key=lambda item: (item[0], item[1], item[2]))

    espacios: List[Espacio] = []
    for i, (fecha_slot, hora, cancha_id, fecha_hora, cuenta_id) in enumerate(espacios_tmp, start=1):
        espacios.append(
            Espacio(
                espacio_id=i,
                cancha_id=cancha_id,
                fecha=fecha_slot,
                hora=hora,
                fecha_hora=fecha_hora,
                cuenta_id=cuenta_id,
            )
        )

    return espacios


def _construir_disponibilidad_jugadores_por_dia_hora_minima(
    disponibilidades_db: List[TorneoDisponibilidadJugador],
    espacios: List[Espacio],
) -> List[DisponibilidadJugador]:
    disponibilidad_minima: Dict[Tuple[int, int, int], time] = {}
    for item in disponibilidades_db:
        weekday = item.fecha.weekday()
        hora_value = _parse_time_value(item.hora)
        if hora_value is None:
            hora_value = item.fecha.time()

        key = (item.idTorneo, item.idJugador, weekday)
        current_min = disponibilidad_minima.get(key)
        if current_min is None or hora_value < current_min:
            disponibilidad_minima[key] = hora_value

    espacios_por_weekday: Dict[int, List[Espacio]] = defaultdict(list)
    for espacio in espacios:
        espacios_por_weekday[espacio.fecha.weekday()].append(espacio)

    disponibilidades: List[DisponibilidadJugador] = []
    for (torneo_id, jugador_id, weekday), hora_minima in disponibilidad_minima.items():
        espacios_ids: List[int] = []
        for espacio in espacios_por_weekday.get(weekday, []):
            hora_espacio = _parse_time_value(espacio.hora)
            if hora_espacio is None or hora_espacio < hora_minima:
                continue
            espacios_ids.append(espacio.espacio_id)

        espacios_disponibles = espacios_ids
        disponibilidades.append(
            DisponibilidadJugador(
                torneo_id=torneo_id,
                jugador_id=jugador_id,
                espacios_disponibles=espacios_disponibles,
            )
        )

    return disponibilidades


def _programar_partidos_por_slots(
    partidos: List[Partido],
    espacios: List[Espacio],
    rangos_torneo: Dict[int, Tuple[date, date]],
    disponibilidad_partido: Dict[str, Set[int]],
    jugadores_por_equipo: Dict[int, Set[int]],
) -> ResultadoCalendario:
    partidos_by_id: Dict[str, Partido] = {partido.partido_id: partido for partido in partidos}
    espacios_by_id: Dict[int, Espacio] = {espacio.espacio_id: espacio for espacio in espacios}

    espacios_validos_por_partido: Dict[str, Set[int]] = {}
    for partido in partidos:
        rango = rangos_torneo.get(partido.torneo_id)
        if rango is None:
            espacios_validos_por_partido[partido.partido_id] = set()
            continue

        fecha_inicio, fecha_fin = rango
        espacios_validos_por_partido[partido.partido_id] = {
            espacio_id
            for espacio_id in disponibilidad_partido.get(partido.partido_id, set())
            if espacio_id in espacios_by_id and fecha_inicio <= espacios_by_id[espacio_id].fecha <= fecha_fin
        }

    pendientes_ids: Set[str] = {partido.partido_id for partido in partidos}
    espacios_utilizados_ids: Set[int] = set()
    equipos_ocupados_por_fecha_hora: DefaultDict[datetime, Set[int]] = defaultdict(set)
    jugadores_ocupados_por_fecha_hora: DefaultDict[datetime, Set[int]] = defaultdict(set)

    resultado = ResultadoCalendario()

    for espacio in espacios:
        if espacio.espacio_id in espacios_utilizados_ids:
            continue

        candidatos: List[Partido] = []
        for partido_id in list(pendientes_ids):
            if espacio.espacio_id not in espacios_validos_por_partido.get(partido_id, set()):
                continue

            partido = partidos_by_id[partido_id]
            equipos_ocupados = equipos_ocupados_por_fecha_hora[espacio.fecha_hora]
            if partido.equipo_a_id in equipos_ocupados or partido.equipo_b_id in equipos_ocupados:
                continue

            jugadores_slot = jugadores_ocupados_por_fecha_hora[espacio.fecha_hora]
            jugadores_partido = jugadores_por_equipo.get(partido.equipo_a_id, set()) | jugadores_por_equipo.get(partido.equipo_b_id, set())
            if jugadores_slot & jugadores_partido:
                continue

            candidatos.append(partido)

        if not candidatos:
            continue

        # Priorizamos el partido con menos opciones futuras para maximizar asignaciones validas.
        partido_seleccionado = min(
            candidatos,
            key=lambda item: (len(espacios_validos_por_partido.get(item.partido_id, set())), item.partido_id),
        )

        jugadores_partido = jugadores_por_equipo.get(partido_seleccionado.equipo_a_id, set()) | jugadores_por_equipo.get(partido_seleccionado.equipo_b_id, set())

        resultado.partidos_asignados.append(
            {
                "partido_id": partido_seleccionado.partido_id,
                "torneo_id": partido_seleccionado.torneo_id,
                "grupo_id": partido_seleccionado.grupo_id,
                "equipo_a_id": partido_seleccionado.equipo_a_id,
                "equipo_b_id": partido_seleccionado.equipo_b_id,
                "espacio_id": espacio.espacio_id,
                "cancha_id": espacio.cancha_id,
                "fecha": espacio.fecha,
                "hora": espacio.hora,
                "fecha_hora": espacio.fecha_hora,
            }
        )

        pendientes_ids.remove(partido_seleccionado.partido_id)
        espacios_utilizados_ids.add(espacio.espacio_id)
        equipos_ocupados_por_fecha_hora[espacio.fecha_hora].add(partido_seleccionado.equipo_a_id)
        equipos_ocupados_por_fecha_hora[espacio.fecha_hora].add(partido_seleccionado.equipo_b_id)
        jugadores_ocupados_por_fecha_hora[espacio.fecha_hora].update(jugadores_partido)

    for partido_id in sorted(pendientes_ids):
        partido = partidos_by_id[partido_id]
        espacios_factibles = espacios_validos_por_partido.get(partido_id, set())

        if not espacios_factibles:
            motivo = MotivoPartidoPendiente.sin_disponibilidad_4_jugadores
            if partido.torneo_id not in rangos_torneo:
                motivo = MotivoPartidoPendiente.fuera_rango_torneo
        else:
            motivo = MotivoPartidoPendiente.espacios_ocupados_por_conflictos

        resultado.partidos_pendientes.append(PartidoPendiente(partido=partido, motivo=motivo))

    resultado.espacios_utilizados = [
        espacio
        for espacio in espacios
        if espacio.espacio_id in espacios_utilizados_ids
    ]
    resultado.espacios_libres = [
        espacio
        for espacio in espacios
        if espacio.espacio_id not in espacios_utilizados_ids
    ]

    return resultado

@router.post("/programarPartidosGreedy", response_model=BaseResponse)
def programar_partidos_greedy_endpoint(
    body: ProgramarPartidosGreedyBody,
    db: Session = Depends(get_db),
):
    try:
        torneos_ids = sorted(set(body.torneos_ids))
        canchas_ids = sorted(set(body.canchas_ids))

        torneos = (
            db.query(Torneo)
            .filter(Torneo.id.in_(torneos_ids))
            .all()
            if torneos_ids
            else []
        )

        if not torneos:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se econtraron torneos",
                data=None,
            )

        rangos_torneo: Dict[int, Tuple[date, date]] = {}
        fechas_inicio: List[date] = []
        fechas_fin: List[date] = []
        for torneo in torneos:
            fecha_inicio_dt = _parse_datetime_value(torneo.fechaInicio)
            fecha_fin_dt = torneo.FaseGrupoFin
            if fecha_inicio_dt is None or fecha_fin_dt is None:
                continue

            fecha_inicio = fecha_inicio_dt.date()
            fecha_fin = fecha_fin_dt.date()
            rangos_torneo[torneo.id] = (fecha_inicio, fecha_fin)
            fechas_inicio.append(fecha_inicio)
            fechas_fin.append(fecha_fin)

        if not rangos_torneo:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se econtraron torneos",
                data=None,
            )

        canchas = db.query(Cancha).filter(Cancha.ID.in_(canchas_ids)).all() if canchas_ids else []
        cancha_ids = [cancha.ID for cancha in canchas]
        fechas_cfg = db.query(Fechas).filter(Fechas.canchaID.in_(cancha_ids)).all() if cancha_ids else []
        fecha_cfg_ids = [item.id for item in fechas_cfg]
        horarios_cfg = db.query(Horarios).filter(Horarios.fechaID.in_(fecha_cfg_ids)).all() if fecha_cfg_ids else []

        espacios = _construir_espacios(
            canchas=canchas,
            fechas=fechas_cfg,
            horarios=horarios_cfg,
            fecha_min=min(fechas_inicio),
            fecha_max=max(fechas_fin),
        )
        
        torneo_ids = [torneo.id for torneo in torneos]
        equipos_db = (
            db.query(EquipoModel)
            .filter(EquipoModel.Torneo.in_(torneo_ids))
            .filter(EquipoModel.baja.is_(False))
            .all()
        )

        equipo_ids = [equipo.id for equipo in equipos_db]
        jugadores_equipo = (
            db.query(JugadorEquipo)
            .filter(JugadorEquipo.equipoID.in_(equipo_ids))
            .all()
            if equipo_ids
            else []
        )
        jugadores_por_equipo: Dict[int, List[int]] = {}
        for item in jugadores_equipo:
            jugadores_por_equipo.setdefault(item.equipoID, []).append(item.jugadorID)

        equipos_dto: List[Equipo] = []
        for equipo in equipos_db:
            jugadores_ids = sorted(set(jugadores_por_equipo.get(equipo.id, [])))
            if len(jugadores_ids) < 2:
                continue

            equipos_dto.append(
                Equipo(
                    equipo_id=equipo.id,
                    torneo_id=equipo.Torneo,
                    grupo_rr=equipo.grupoRR or GRUPO_GENERAL_ID,
                    jugador_1_id=jugadores_ids[0],
                    jugador_2_id=jugadores_ids[1],
                    nombre_equipo=equipo.nombreEquipo,
                )
            )

        equipos_por_torneo: Dict[int, List[Equipo]] = {}
        for equipo in equipos_dto:
            equipos_por_torneo.setdefault(equipo.torneo_id, []).append(equipo)

        grupos: List[Grupo] = []
        for torneo in torneos:
            grupos.extend(_construir_grupos_torneo(torneo, equipos_por_torneo.get(torneo.id, [])))

        partidos: List[Partido] = generar_partidos_round_robin(grupos)

        jugador_ids = sorted({item.jugadorID for item in jugadores_equipo})
        disponibilidades_db = (
            db.query(TorneoDisponibilidadJugador)
            .filter(TorneoDisponibilidadJugador.idTorneo.in_(torneo_ids))
            .filter(TorneoDisponibilidadJugador.idJugador.in_(jugador_ids))
            .filter(
                (TorneoDisponibilidadJugador.hora.is_(None))
                | (func.lower(func.trim(TorneoDisponibilidadJugador.hora)) != "no puedo")
            )
            .all()
            if jugador_ids
            else []
        )
        disponibilidades_jugador = _construir_disponibilidad_jugadores_desde_db(disponibilidades_db, espacios)

        disponibilidad_jugador_index = construir_disponibilidad_jugador(disponibilidades_jugador)
        disponibilidad_equipo = construir_disponibilidad_equipo(equipos_dto, disponibilidad_jugador_index)
        disponibilidad_partido = (
            construir_disponibilidad_partido(partidos, disponibilidad_equipo)
            if disponibilidades_db
            else None
        )

        resultado = programar_partidos_greedy(
            partidos=partidos,
            espacios=espacios,
            disponibilidad_partido=disponibilidad_partido,
            rangos_torneo=rangos_torneo,
        )

        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data= resultado
        )
    except Exception as ex:
        return BaseResponse(
            respuesta="ERROR",
            mensaje=str(ex),
            data=None,
        )


@router.post("/programarPartidosGreedyPorCalendar", response_model=BaseResponse)
def programar_partidos_greedy_por_calendar_endpoint(
    calendarID: int,
    db: Session = Depends(get_db),
):
    try:

        config_calendar = db.query(ConfigCalendar).filter(ConfigCalendar.id == calendarID).first()
        if config_calendar is None:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se encontro configuracion para el calendarID enviado",
                data=None,
            )

        try:
            torneos_ids = _parse_torneos_ids_value(config_calendar.tournaments)
        except ValueError:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="La cadena de torneos en config_calendar es invalida",
                data=None,
            )

        if not torneos_ids:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se encontraron torneos en la configuracion del calendario",
                data=None,
            )

        torneos = db.query(Torneo).filter(Torneo.id.in_(torneos_ids)).all()
        if not torneos:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se econtraron torneos",
                data=None,
            )
        
        #Borramos los partidos relacionos desde jornada
        jornadas = db.query(Jornadas).filter(Jornadas.torneo.in_(torneos_ids)).all()
        for jornada in jornadas:
            partidos_jornada = db.query(PartidosJornadas).filter(PartidosJornadas.idJornada == jornada.id).all()
            for partido in partidos_jornada:
                db.delete(partido)
            db.delete(jornada)
        db.flush()

        rangos_torneo: Dict[int, Tuple[date, date]] = {}
        for torneo in torneos:
            fecha_inicio_dt = _parse_datetime_value(torneo.fechaInicio)
            fecha_fin_dt = torneo.FaseGrupoFin
            if fecha_inicio_dt is None or fecha_fin_dt is None:
                continue

            rangos_torneo[torneo.id] = (fecha_inicio_dt.date(), fecha_fin_dt.date())

        if not rangos_torneo:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se econtraron rangos validos para torneos",
                data=None,
            )

        relaciones = db.query(RelationsCalendar).filter(RelationsCalendar.calendarID == calendarID).all()
        if not relaciones:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se encontraron espacios disponibles para este calendario",
                data=None,
            )
        
        #Limpiamos los partidoID que tengan las relaciones para volver a asignarlos
        for relacion in relaciones:
            relacion.partidoID = None
        db.flush()

        canchas_ids = sorted({relacion.canchaID for relacion in relaciones})
        canchas_db = db.query(Cancha).filter(Cancha.ID.in_(canchas_ids)).all() if canchas_ids else []
        cuenta_por_cancha = {cancha.ID: (cancha.cuentaId or 0) for cancha in canchas_db}
        espacios = _construir_espacios_desde_relaciones(relaciones, cuenta_por_cancha)

        if not espacios:
            return BaseResponse(
                respuesta="ERROR",
                mensaje="No se pudieron construir espacios validos desde relations_calendar",
                data=None,
            )

        torneo_ids = [torneo.id for torneo in torneos]
        equipos_db = (
            db.query(EquipoModel)
            .filter(EquipoModel.Torneo.in_(torneo_ids))
            .filter(EquipoModel.baja.is_(False))
            .all()
        )

        equipo_ids = [equipo.id for equipo in equipos_db]
        jugadores_equipo = (
            db.query(JugadorEquipo)
            .filter(JugadorEquipo.equipoID.in_(equipo_ids))
            .all()
            if equipo_ids
            else []
        )

        jugadores_por_equipo_raw: Dict[int, List[int]] = {}
        for item in jugadores_equipo:
            jugadores_por_equipo_raw.setdefault(item.equipoID, []).append(item.jugadorID)

        equipos_dto: List[Equipo] = []
        for equipo in equipos_db:
            jugadores_ids = sorted(set(jugadores_por_equipo_raw.get(equipo.id, [])))
            if len(jugadores_ids) < 2:
                continue

            equipos_dto.append(
                Equipo(
                    equipo_id=equipo.id,
                    torneo_id=equipo.Torneo,
                    grupo_rr=equipo.grupoRR or GRUPO_GENERAL_ID,
                    jugador_1_id=jugadores_ids[0],
                    jugador_2_id=jugadores_ids[1],
                    nombre_equipo=equipo.nombreEquipo,
                )
            )

        equipos_por_torneo: Dict[int, List[Equipo]] = {}
        for equipo in equipos_dto:
            equipos_por_torneo.setdefault(equipo.torneo_id, []).append(equipo)

        grupos: List[Grupo] = []
        for torneo in torneos:
            grupos.extend(_construir_grupos_torneo(torneo, equipos_por_torneo.get(torneo.id, [])))

        partidos: List[Partido] = generar_partidos_round_robin(grupos)

        jugador_ids = sorted({item.jugadorID for item in jugadores_equipo})
        disponibilidades_db = (
            db.query(TorneoDisponibilidadJugador)
            .filter(TorneoDisponibilidadJugador.idTorneo.in_(torneo_ids))
            .filter(TorneoDisponibilidadJugador.idJugador.in_(jugador_ids))
            .filter(
                (TorneoDisponibilidadJugador.hora.is_(None))
                | (func.lower(func.trim(TorneoDisponibilidadJugador.hora)) != "no puedo")
            )
            .all()
            if jugador_ids
            else []
        )

        disponibilidades_jugador = _construir_disponibilidad_jugadores_por_dia_hora_minima(
            disponibilidades_db=disponibilidades_db,
            espacios=espacios,
        )
        disponibilidad_jugador_index = construir_disponibilidad_jugador(disponibilidades_jugador)
        disponibilidad_equipo = construir_disponibilidad_equipo(equipos_dto, disponibilidad_jugador_index)
        disponibilidad_partido = construir_disponibilidad_partido(partidos, disponibilidad_equipo)

        jugadores_por_equipo: Dict[int, Set[int]] = {
            equipo.equipo_id: {equipo.jugador_1_id, equipo.jugador_2_id}
            for equipo in equipos_dto
        }

        resultado = _programar_partidos_por_slots(
            partidos=partidos,
            espacios=espacios,
            rangos_torneo=rangos_torneo,
            disponibilidad_partido=disponibilidad_partido,
            jugadores_por_equipo=jugadores_por_equipo,
        )

        #Procedemos a guardar en relacion a jornadas partidos entre torneo y grupoID
        for torneo in torneos_ids:
            for grupo in grupos:
                if grupo.torneo_id != torneo:
                    continue

                partidos_grupo = [
                    item
                    for item in resultado.partidos_asignados
                    if item["torneo_id"] == torneo
                    and item["grupo_id"] == grupo.grupo_id
                ]

                fechas = [
                            partido["fecha"]
                            for partido in partidos_grupo
                        ]

                fecha_inicio = min(fechas)
                fecha_fin = max(fechas)

                jornada = Jornadas(
                    nombre="Jornada 1",
                    fechaInicio=fecha_inicio,
                    fechaFin=fecha_fin,
                    categoria=0,
                    torneo=torneo,
                    tipoJornada="REGULAR",
                    llaveLiguilla=0,
                    numeroLlave=0,
                    posicionLlave=0,
                    siguienteJornada=0,
                    jornadaFinalizada=False,
                    torneoC=torneo,
                    ultimaModificacion=datetime.now(),
                    cuentaId=config_calendar.cuentaID,
                )

                db.add(jornada)
                db.flush()

                for partido_asignado in resultado.partidos_asignados:
                    if partido_asignado["torneo_id"] != torneo or partido_asignado["grupo_id"] != grupo.grupo_id:
                        continue
                    #Buscamos la informacion de la cancha
                    canchaPartido = db.query(Cancha).filter(Cancha.ID == partido_asignado["cancha_id"]).first()
                    #creamos los partidos jornadas
                    partido = PartidosJornadas(
                        idJornada=jornada.id,
                        idEquipo1=partido_asignado["equipo_a_id"],
                        idEquipo2=partido_asignado["equipo_b_id"],
                        fechaHoraPartido=partido_asignado["fecha"],
                        lugar = partido_asignado["cancha_id"],
                        hora = partido_asignado["hora"],
                        marcadorEquipo1 = 0,
                        marcadorEquipo2 = 0,
                        estadoPartido="POR JUGAR",
                        fechaHoraInicioPartido = "0001-01-01 00:00:00", 
                        fechaHoraFinPrimerTiempo = "0001-01-01 00:00:00",
                        fechaHoraInicioSegundoTiempo = "0001-01-01 00:00:00",
                        fechaHoraFinPartido = "0001-01-01 00:00:00",
                        fechaHoraPausa = "0001-01-01 00:00:00",
                        pausaAcumuladaPrimerTiempo = 0.0,
                        pausaAcumuladaSegundoTiempo = 0.0,  
                        bajaPartido = False,
                        ultimaModificacion = datetime.now(),
                        fechaHoraTiemposExtra = "0001-01-01 00:00:00",
                        fechaHora1erTiempoExtra = "0001-01-01 00:00:00",
                        fechaHora2doTiempoExtra = "0001-01-01 00:00:00",
                        descanso1erTiempoExtra = "0001-01-01 00:00:00",
                        pausaAcumulada1erTiempoExtra = 0.0,
                        pausaAcumulada2doTiempoExtra = 0.0,
                        etiquetaCancha = (
                                            f"{canchaPartido.nombreCancha} - "
                                            f"{partido_asignado['fecha'].strftime('%d/%m/%Y')} - "
                                            f"{partido_asignado['hora']}"
                                        ) if canchaPartido else "",
                        noPartidoPadel = 0,
                        grupoID = grupo.grupo_id,                  
                    )
                    db.add(partido)
                    db.flush()
                    partido_asignado["partido_id"] = str(partido.id)

                for partido_pendiente in resultado.partidos_pendientes:
                    if partido_pendiente.partido.torneo_id != torneo or partido_pendiente.partido.grupo_id != grupo.grupo_id:
                        continue
                    partido = PartidosJornadas(
                        idJornada=jornada.id,
                        idEquipo1=partido_pendiente.partido.equipo_a_id,
                        idEquipo2=partido_pendiente.partido.equipo_b_id,
                        fechaHoraPartido="0001-01-01 00:00:00",
                        lugar = None,
                        hora = None,
                        marcadorEquipo1 = 0,
                        marcadorEquipo2 = 0,
                        estadoPartido="POR JUGAR",
                        fechaHoraInicioPartido = "0001-01-01 00:00:00", 
                        fechaHoraFinPrimerTiempo = "0001-01-01 00:00:00",
                        fechaHoraInicioSegundoTiempo = "0001-01-01 00:00:00",
                        fechaHoraFinPartido = "0001-01-01 00:00:00",
                        fechaHoraPausa = "0001-01-01 00:00:00",
                        pausaAcumuladaPrimerTiempo = 0.0,
                        pausaAcumuladaSegundoTiempo = 0.0,  
                        bajaPartido = False,
                        ultimaModificacion = datetime.now(),
                        fechaHoraTiemposExtra = "0001-01-01 00:00:00",
                        fechaHora1erTiempoExtra = "0001-01-01 00:00:00",
                        fechaHora2doTiempoExtra = "0001-01-01 00:00:00",
                        descanso1erTiempoExtra = "0001-01-01 00:00:00",
                        pausaAcumulada1erTiempoExtra = 0.0,
                        pausaAcumulada2doTiempoExtra = 0.0,
                        etiquetaCancha = "",
                        noPartidoPadel = 0,
                        grupoID = grupo.grupo_id,                  
                    )
                    db.add(partido)
                    db.flush()

        # Procedemos a guardar sobre RelationsCalendar los partidos programados en los espacios para marcar que ya no estan disponibles
        for partido_asignado in resultado.partidos_asignados:
            relacion = (
                db.query(RelationsCalendar)
                .filter(
                    RelationsCalendar.calendarID == calendarID,
                    RelationsCalendar.canchaID == partido_asignado["cancha_id"],
                    RelationsCalendar.fecha == partido_asignado["fecha"],
                    RelationsCalendar.hora == partido_asignado["hora"]
                )
                .first()
            )

            if relacion:
                relacion.partidoID = int(partido_asignado["partido_id"])

        db.flush()
        db.commit()
                      

        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data=resultado,
        )
    except Exception as ex:
        db.rollback()
        return BaseResponse(
            respuesta="ERROR",
            mensaje=str(ex),
            data=None,
        )
