from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from enum import Enum
import random
from typing import Any, DefaultDict, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field


class MotivoPartidoPendiente(str, Enum):
    """Motivos estandar para explicar por que un partido no pudo asignarse."""

    sin_disponibilidad_4_jugadores = "sin_disponibilidad_4_jugadores"
    fuera_rango_torneo = "fuera_rango_torneo"
    espacios_ocupados_por_conflictos = "espacios_ocupados_por_conflictos"
    sin_espacios_fisicos_disponibles = "sin_espacios_fisicos_disponibles"


class Espacio(BaseModel):
    """Unidad minima de calendario: cancha + fecha + hora."""

    espacio_id: int
    cancha_id: int
    fecha: date
    hora: str
    fecha_hora: datetime
    cuenta_id: int


class Equipo(BaseModel):
    """Equipo/pareja participante en un torneo."""

    equipo_id: int
    torneo_id: int
    grupo_rr: int
    jugador_1_id: int
    jugador_2_id: int
    nombre_equipo: Optional[str] = None


class Grupo(BaseModel):
    """Agrupacion de equipos para Round Robin dentro de un torneo."""

    grupo_id: int
    torneo_id: int
    equipos: List[Equipo] = Field(default_factory=list)


class Partido(BaseModel):
    """Partido generado para calendarizacion entre dos equipos del mismo grupo."""

    partido_id: str
    torneo_id: int
    grupo_id: int
    equipo_a_id: int
    equipo_b_id: int


class DisponibilidadJugador(BaseModel):
    """Disponibilidad declarada por jugador para un torneo."""

    torneo_id: int
    jugador_id: int
    espacios_disponibles: List[int] = Field(default_factory=list)


class PartidoPendiente(BaseModel):
    """Partido que no logro ser asignado con la estrategia actual."""

    partido: Partido
    motivo: MotivoPartidoPendiente
    detalle: Optional[str] = None


class ResultadoCalendario(BaseModel):
    """Resultado en memoria de la propuesta de calendario."""

    partidos_asignados: List[Dict[str, Any]] = Field(default_factory=list)
    partidos_pendientes: List[PartidoPendiente] = Field(default_factory=list)
    espacios_utilizados: List[Espacio] = Field(default_factory=list)
    espacios_libres: List[Espacio] = Field(default_factory=list)


JugadorPorTorneoKey = Tuple[int, int]
RangoFechaTorneo = Tuple[date, date]


def construir_disponibilidad_jugador(
    disponibilidades: List[DisponibilidadJugador],
) -> Dict[JugadorPorTorneoKey, Set[int]]:
    """Construye indice (torneo_id, jugador_id) -> espacios disponibles."""

    indice: DefaultDict[JugadorPorTorneoKey, Set[int]] = defaultdict(set)
    for disponibilidad in disponibilidades:
        key = (disponibilidad.torneo_id, disponibilidad.jugador_id)
        indice[key].update(disponibilidad.espacios_disponibles)
    return dict(indice)


def construir_disponibilidad_equipo(
    equipos: List[Equipo],
    disponibilidad_jugador: Dict[JugadorPorTorneoKey, Set[int]],
) -> Dict[int, Set[int]]:
    """Construye indice equipo_id -> espacios comunes entre sus 2 jugadores."""

    disponibilidad_equipo: Dict[int, Set[int]] = {}
    for equipo in equipos:
        espacios_j1 = disponibilidad_jugador.get((equipo.torneo_id, equipo.jugador_1_id), set())
        espacios_j2 = disponibilidad_jugador.get((equipo.torneo_id, equipo.jugador_2_id), set())
        disponibilidad_equipo[equipo.equipo_id] = espacios_j1 & espacios_j2
    return disponibilidad_equipo


def construir_disponibilidad_partido(
    partidos: List[Partido],
    disponibilidad_equipo: Dict[int, Set[int]],
) -> Dict[str, Set[int]]:
    """Construye indice partido_id -> espacios comunes entre ambos equipos."""

    disponibilidad_partido: Dict[str, Set[int]] = {}

    print("KEYS DISPONIBILIDAD EQUIPO:")
    print(disponibilidad_equipo.keys())

    for partido in partidos:
        espacios_a = disponibilidad_equipo.get(partido.equipo_a_id, set())
        espacios_b = disponibilidad_equipo.get(partido.equipo_b_id, set())

        disponibilidad_partido[partido.partido_id] = espacios_a & espacios_b

    return disponibilidad_partido


def generar_partidos_round_robin(grupos: List[Grupo]) -> List[Partido]:
    """Genera todos los partidos Round Robin por grupo con ids deterministas."""

    partidos: List[Partido] = []
    for grupo in grupos:
        correlativo_grupo = 1
        equipos = grupo.equipos
        for i in range(len(equipos)):
            for j in range(i + 1, len(equipos)):
                equipo_a = equipos[i]
                equipo_b = equipos[j]
                partidos.append(
                    Partido(
                        partido_id=f"t{grupo.torneo_id}-g{grupo.grupo_id}-m{correlativo_grupo}",
                        torneo_id=grupo.torneo_id,
                        grupo_id=grupo.grupo_id,
                        equipo_a_id=equipo_a.equipo_id,
                        equipo_b_id=equipo_b.equipo_id,
                    )
                )
                correlativo_grupo += 1
    return partidos


def _espacio_en_rango_torneo(espacio: Espacio, rango: RangoFechaTorneo) -> bool:
    fecha_inicio, fecha_fin = rango
    return fecha_inicio <= espacio.fecha <= fecha_fin


def programar_partidos_greedy(
    partidos: List[Partido],
    espacios: List[Espacio],
    disponibilidad_partido: Optional[Dict[str, Set[int]]],
    rangos_torneo: Dict[int, RangoFechaTorneo],
) -> ResultadoCalendario:
    """Asigna partidos con estrategia greedy: menor factibilidad y espacio cronologico."""

    espacios_por_id: Dict[int, Espacio] = {espacio.espacio_id: espacio for espacio in espacios}
    usar_fallback_aleatorio = not disponibilidad_partido
    espacios_ordenados = sorted(espacios, key=lambda e: e.fecha_hora)
    espacios_utilizados_ids: Set[int] = set()
    equipos_ocupados_por_fecha_hora: DefaultDict[datetime, Set[int]] = defaultdict(set)

    candidatos_por_partido: Dict[str, List[Espacio]] = {}
    motivo_base_por_partido: Dict[str, MotivoPartidoPendiente] = {}

    for partido in partidos:
        if usar_fallback_aleatorio:
            espacios_factibles_ids = set(espacios_por_id.keys())
        else:
            espacios_factibles_ids = disponibilidad_partido.get(partido.partido_id, set())

        if not espacios_factibles_ids:
            candidatos_por_partido[partido.partido_id] = []
            motivo_base_por_partido[partido.partido_id] = MotivoPartidoPendiente.sin_disponibilidad_4_jugadores
            continue

        espacios_existentes = [
            espacios_por_id[espacio_id]
            for espacio_id in espacios_factibles_ids
            if espacio_id in espacios_por_id
        ]
        if not espacios_existentes:
            candidatos_por_partido[partido.partido_id] = []
            motivo_base_por_partido[partido.partido_id] = MotivoPartidoPendiente.sin_espacios_fisicos_disponibles
            continue

        rango = rangos_torneo.get(partido.torneo_id)
        if rango is None:
            candidatos_por_partido[partido.partido_id] = []
            motivo_base_por_partido[partido.partido_id] = MotivoPartidoPendiente.fuera_rango_torneo
            continue

        espacios_en_rango = [espacio for espacio in espacios_existentes if _espacio_en_rango_torneo(espacio, rango)]
        if not espacios_en_rango:
            candidatos_por_partido[partido.partido_id] = []
            motivo_base_por_partido[partido.partido_id] = MotivoPartidoPendiente.fuera_rango_torneo
            continue

        if usar_fallback_aleatorio:
            random.shuffle(espacios_en_rango)
            candidatos_por_partido[partido.partido_id] = espacios_en_rango
        else:
            candidatos_por_partido[partido.partido_id] = sorted(espacios_en_rango, key=lambda e: e.fecha_hora)

    if usar_fallback_aleatorio:
        partidos_ordenados = partidos[:]
        random.shuffle(partidos_ordenados)
    else:
        partidos_ordenados = sorted(
            partidos,
            key=lambda p: (
                len(candidatos_por_partido.get(p.partido_id, [])),
                candidatos_por_partido[p.partido_id][0].fecha_hora if candidatos_por_partido.get(p.partido_id) else datetime.max,
                p.partido_id,
            ),
        )

    resultado = ResultadoCalendario()

    for partido in partidos_ordenados:
        candidatos = candidatos_por_partido.get(partido.partido_id, [])
        asignado = False

        for espacio in candidatos:
            if espacio.espacio_id in espacios_utilizados_ids:
                continue

            equipos_ocupados = equipos_ocupados_por_fecha_hora[espacio.fecha_hora]
            if partido.equipo_a_id in equipos_ocupados or partido.equipo_b_id in equipos_ocupados:
                continue

            resultado.partidos_asignados.append(
                {
                    "partido_id": partido.partido_id,
                    "torneo_id": partido.torneo_id,
                    "grupo_id": partido.grupo_id,
                    "equipo_a_id": partido.equipo_a_id,
                    "equipo_b_id": partido.equipo_b_id,
                    "espacio_id": espacio.espacio_id,
                    "cancha_id": espacio.cancha_id,
                    "fecha": espacio.fecha,
                    "hora": espacio.hora,
                    "fecha_hora": espacio.fecha_hora,
                }
            )
            espacios_utilizados_ids.add(espacio.espacio_id)
            equipos_ocupados.add(partido.equipo_a_id)
            equipos_ocupados.add(partido.equipo_b_id)
            asignado = True
            break

        if not asignado:
            motivo = motivo_base_por_partido.get(
                partido.partido_id,
                MotivoPartidoPendiente.espacios_ocupados_por_conflictos,
            )
            resultado.partidos_pendientes.append(PartidoPendiente(partido=partido, motivo=motivo))

    resultado.espacios_utilizados = [
        espacio
        for espacio in espacios_ordenados
        if espacio.espacio_id in espacios_utilizados_ids
    ]
    resultado.espacios_libres = [
        espacio
        for espacio in espacios_ordenados
        if espacio.espacio_id not in espacios_utilizados_ids
    ]

    return resultado