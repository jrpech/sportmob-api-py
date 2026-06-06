from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional, Set, Tuple

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cancha import Cancha
from app.models.equipo import Equipo as EquipoModel
from app.models.fechas import Fechas
from app.models.horarios import Horarios
from app.models.jugador_equipo import JugadorEquipo
from app.models.torneo import Torneo
from app.models.torneo_disponibilidad_jugador import TorneoDisponibilidadJugador
from app.schemas import BaseResponse
from app.services.scheduling_dtos import (
    DisponibilidadJugador,
    Equipo,
    Espacio,
    Grupo,
    Partido,
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
