import unittest
from datetime import date, datetime

from app.services.scheduling_dtos import (
    DisponibilidadJugador,
    Espacio,
    Equipo,
    Grupo,
    Partido,
    construir_disponibilidad_equipo,
    construir_disponibilidad_jugador,
    construir_disponibilidad_partido,
    generar_partidos_round_robin,
    programar_partidos_greedy,
)


class SchedulingAvailabilityTests(unittest.TestCase):
    def test_construir_disponibilidad_jugador_combina_registros_por_torneo_y_jugador(self):
        disponibilidades = [
            DisponibilidadJugador(torneo_id=1, jugador_id=10, espacios_disponibles=[1, 2, 3]),
            DisponibilidadJugador(torneo_id=1, jugador_id=10, espacios_disponibles=[3, 4]),
            DisponibilidadJugador(torneo_id=1, jugador_id=11, espacios_disponibles=[2]),
            DisponibilidadJugador(torneo_id=2, jugador_id=10, espacios_disponibles=[8]),
        ]

        indice = construir_disponibilidad_jugador(disponibilidades)

        self.assertEqual(indice[(1, 10)], {1, 2, 3, 4})
        self.assertEqual(indice[(1, 11)], {2})
        self.assertEqual(indice[(2, 10)], {8})

    def test_construir_disponibilidad_equipo_interseca_jugadores(self):
        equipos = [
            Equipo(
                equipo_id=100,
                torneo_id=1,
                grupo_rr=1,
                jugador_1_id=10,
                jugador_2_id=11,
            ),
            Equipo(
                equipo_id=101,
                torneo_id=1,
                grupo_rr=1,
                jugador_1_id=12,
                jugador_2_id=13,
            ),
        ]
        disponibilidad_jugador = {
            (1, 10): {1, 2, 3},
            (1, 11): {2, 3, 4},
            (1, 12): {5},
        }

        indice = construir_disponibilidad_equipo(equipos, disponibilidad_jugador)

        self.assertEqual(indice[100], {2, 3})
        self.assertEqual(indice[101], set())

    def test_construir_disponibilidad_partido_interseca_equipos(self):
        partidos = [
            Partido(
                partido_id="m1",
                torneo_id=1,
                grupo_id=1,
                equipo_a_id=100,
                equipo_b_id=101,
            ),
            Partido(
                partido_id="m2",
                torneo_id=1,
                grupo_id=1,
                equipo_a_id=100,
                equipo_b_id=999,
            ),
        ]
        disponibilidad_equipo = {
            100: {2, 3, 4},
            101: {3, 6},
        }

        indice = construir_disponibilidad_partido(partidos, disponibilidad_equipo)

        self.assertEqual(indice["m1"], {3})
        self.assertEqual(indice["m2"], set())

    def test_generar_partidos_round_robin_genera_combinaciones_unicas(self):
        grupo = Grupo(
            grupo_id=7,
            torneo_id=1,
            equipos=[
                Equipo(equipo_id=100, torneo_id=1, grupo_rr=7, jugador_1_id=1, jugador_2_id=2),
                Equipo(equipo_id=101, torneo_id=1, grupo_rr=7, jugador_1_id=3, jugador_2_id=4),
                Equipo(equipo_id=102, torneo_id=1, grupo_rr=7, jugador_1_id=5, jugador_2_id=6),
                Equipo(equipo_id=103, torneo_id=1, grupo_rr=7, jugador_1_id=7, jugador_2_id=8),
            ],
        )

        partidos = generar_partidos_round_robin([grupo])

        self.assertEqual(len(partidos), 6)
        pares = {(p.equipo_a_id, p.equipo_b_id) for p in partidos}
        self.assertEqual(
            pares,
            {
                (100, 101),
                (100, 102),
                (100, 103),
                (101, 102),
                (101, 103),
                (102, 103),
            },
        )
        self.assertEqual([p.partido_id for p in partidos], [f"g7-m{i}" for i in range(1, 7)])

    def test_generar_partidos_round_robin_maneja_varios_grupos(self):
        grupo_a = Grupo(
            grupo_id=1,
            torneo_id=10,
            equipos=[
                Equipo(equipo_id=1, torneo_id=10, grupo_rr=1, jugador_1_id=11, jugador_2_id=12),
                Equipo(equipo_id=2, torneo_id=10, grupo_rr=1, jugador_1_id=13, jugador_2_id=14),
                Equipo(equipo_id=3, torneo_id=10, grupo_rr=1, jugador_1_id=15, jugador_2_id=16),
            ],
        )
        grupo_b = Grupo(
            grupo_id=2,
            torneo_id=10,
            equipos=[
                Equipo(equipo_id=4, torneo_id=10, grupo_rr=2, jugador_1_id=17, jugador_2_id=18),
            ],
        )
        grupo_c = Grupo(
            grupo_id=3,
            torneo_id=20,
            equipos=[
                Equipo(equipo_id=5, torneo_id=20, grupo_rr=3, jugador_1_id=21, jugador_2_id=22),
                Equipo(equipo_id=6, torneo_id=20, grupo_rr=3, jugador_1_id=23, jugador_2_id=24),
            ],
        )

        partidos = generar_partidos_round_robin([grupo_a, grupo_b, grupo_c])

        self.assertEqual(len(partidos), 4)
        self.assertEqual([p.partido_id for p in partidos], ["g1-m1", "g1-m2", "g1-m3", "g3-m1"])
        self.assertEqual([p.torneo_id for p in partidos], [10, 10, 10, 20])

    def test_scheduler_greedy_prioriza_menor_cantidad_de_espacios_factibles(self):
        espacios = [
            Espacio(
                espacio_id=1,
                cancha_id=10,
                fecha=date(2026, 1, 10),
                hora="20:00",
                fecha_hora=datetime(2026, 1, 10, 20, 0),
                cuenta_id=1,
            ),
            Espacio(
                espacio_id=2,
                cancha_id=10,
                fecha=date(2026, 1, 11),
                hora="20:00",
                fecha_hora=datetime(2026, 1, 11, 20, 0),
                cuenta_id=1,
            ),
        ]
        partidos = [
            Partido(partido_id="p_flexible", torneo_id=1, grupo_id=1, equipo_a_id=100, equipo_b_id=101),
            Partido(partido_id="p_restringido", torneo_id=1, grupo_id=1, equipo_a_id=102, equipo_b_id=103),
        ]
        disponibilidad_partido = {
            "p_flexible": {1, 2},
            "p_restringido": {1},
        }

        resultado = programar_partidos_greedy(
            partidos=partidos,
            espacios=espacios,
            disponibilidad_partido=disponibilidad_partido,
            rangos_torneo={1: (date(2026, 1, 1), date(2026, 1, 31))},
        )

        self.assertEqual(len(resultado.partidos_asignados), 2)
        asignados = {item["partido_id"]: item["espacio_id"] for item in resultado.partidos_asignados}
        self.assertEqual(asignados["p_restringido"], 1)
        self.assertEqual(asignados["p_flexible"], 2)

    def test_scheduler_greedy_asigna_cronologicamente(self):
        espacios = [
            Espacio(
                espacio_id=40,
                cancha_id=8,
                fecha=date(2026, 2, 2),
                hora="21:00",
                fecha_hora=datetime(2026, 2, 2, 21, 0),
                cuenta_id=1,
            ),
            Espacio(
                espacio_id=20,
                cancha_id=8,
                fecha=date(2026, 2, 1),
                hora="20:00",
                fecha_hora=datetime(2026, 2, 1, 20, 0),
                cuenta_id=1,
            ),
            Espacio(
                espacio_id=30,
                cancha_id=8,
                fecha=date(2026, 2, 1),
                hora="22:00",
                fecha_hora=datetime(2026, 2, 1, 22, 0),
                cuenta_id=1,
            ),
        ]
        partidos = [
            Partido(partido_id="p1", torneo_id=1, grupo_id=1, equipo_a_id=1, equipo_b_id=2),
        ]
        disponibilidad_partido = {"p1": {30, 40, 20}}

        resultado = programar_partidos_greedy(
            partidos=partidos,
            espacios=espacios,
            disponibilidad_partido=disponibilidad_partido,
            rangos_torneo={1: (date(2026, 2, 1), date(2026, 2, 28))},
        )

        self.assertEqual(len(resultado.partidos_asignados), 1)
        self.assertEqual(resultado.partidos_asignados[0]["espacio_id"], 20)

    def test_scheduler_greedy_registra_pendientes(self):
        espacios = [
            Espacio(
                espacio_id=1,
                cancha_id=1,
                fecha=date(2026, 3, 10),
                hora="20:00",
                fecha_hora=datetime(2026, 3, 10, 20, 0),
                cuenta_id=1,
            ),
        ]
        partidos = [
            Partido(partido_id="p_sin_disp", torneo_id=1, grupo_id=1, equipo_a_id=10, equipo_b_id=11),
            Partido(partido_id="p_fuera_rango", torneo_id=1, grupo_id=1, equipo_a_id=12, equipo_b_id=13),
        ]
        disponibilidad_partido = {
            "p_sin_disp": set(),
            "p_fuera_rango": {1},
        }

        resultado = programar_partidos_greedy(
            partidos=partidos,
            espacios=espacios,
            disponibilidad_partido=disponibilidad_partido,
            rangos_torneo={1: (date(2026, 3, 1), date(2026, 3, 9))},
        )

        self.assertEqual(len(resultado.partidos_asignados), 0)
        self.assertEqual(len(resultado.partidos_pendientes), 2)
        motivos = {p.partido.partido_id: p.motivo for p in resultado.partidos_pendientes}
        self.assertEqual(motivos["p_sin_disp"], "sin_disponibilidad_4_jugadores")
        self.assertEqual(motivos["p_fuera_rango"], "fuera_rango_torneo")


if __name__ == "__main__":
    unittest.main()
