# Scheduler Greedy de Partidos

## Objetivo

Este documento explica como funciona el scheduler greedy implementado en la API para proponer un calendario de partidos en memoria (sin guardar en base de datos).

El flujo cubre:

1. Construccion de datos desde canchas_ids y torneos_ids.
2. Construccion de disponibilidad por jugador.
3. Construccion de disponibilidad por equipo.
4. Construccion de disponibilidad por partido.
5. Asignacion greedy de partidos a espacios.

## Endpoint

- Metodo: POST
- URL: /api/Scheduler/programarPartidosGreedy
- Tag Swagger: Scheduler
- Body requerido: canchas_ids y torneos_ids

## Reglas del scheduler greedy

El metodo programar_partidos_greedy aplica estas reglas:

1. Ordenar partidos por menor cantidad de espacios factibles.
2. Asignar en orden cronologico (espacio mas temprano posible).
3. Registrar partidos pendientes cuando no hay asignacion valida.

Adicionalmente se respetan estas restricciones:

- Un espacio solo se usa una vez.
- Un equipo no puede jugar dos partidos al mismo tiempo.
- El espacio debe estar dentro del rango fecha_inicio-fecha_fin del torneo.

Si no se encuentran torneos validos en torneos_ids, el endpoint regresa:

```json
{
  "respuesta": "ERROR",
  "mensaje": "No se econtraron torneos",
  "data": null
}
```

## Estructuras principales

### Entrada

- canchas_ids: lista de ids de canchas a considerar.
- torneos_ids: lista de ids de torneos a considerar.

### Salida

- partidos_asignados: lista de partidos con su espacio asignado.
- partidos_pendientes: lista de partidos no asignados con motivo.
- espacios_utilizados: espacios que quedaron ocupados.
- espacios_libres: espacios no utilizados.

## Motivos de partido pendiente

- sin_disponibilidad_4_jugadores
- fuera_rango_torneo
- espacios_ocupados_por_conflictos
- sin_espacios_fisicos_disponibles

## Flujo de asignacion

1. Se consultan torneos por torneos_ids (solo esos torneos participan).
2. Se parsean fechaInicio y fechaFin de torneo a datetime.
3. Se consultan canchas por canchas_ids.
4. Se construyen espacios desde Cancha -> Fechas -> Horarios para el rango global.
5. Se consultan equipos por torneo (baja=false) y sus jugadores (jugadorequipo).
6. Se reconstruyen grupos RR segun dividirRR/noGruposRR.
7. Se generan partidos Round Robin por grupo.
8. Se consulta TorneoDisponibilidadJugador y se transforma a espacios factibles.
9. Se indexan disponibilidades Jugador -> Equipo -> Partido.
10. Para cada partido se construye su lista de candidatos validos:
   - Debe existir disponibilidad para el partido.
   - Debe existir el espacio fisico.
   - Debe caer en rango de fechas del torneo.
11. Se ordenan partidos por:
   - menor numero de candidatos,
   - primer candidato mas temprano,
   - partido_id (desempate estable).
12. Cada partido intenta tomar su primer candidato cronologico disponible.
13. Si no puede, se registra en pendientes con motivo.

## Ejemplo de request

### Body

```json
{
  "canchas_ids": [1, 2, 3],
  "torneos_ids": [10, 11]
}
```

### Swagger

- Metodo: POST
- URL en Swagger: /api/Scheduler/programarPartidosGreedy
- Captura de body JSON con canchas_ids y torneos_ids

### cURL

```bash
curl -X POST "http://localhost:8000/api/Scheduler/programarPartidosGreedy" \
  -H "Content-Type: application/json" \
  -d '{
    "canchas_ids": [1, 2, 3],
    "torneos_ids": [10, 11]
  }'
```

### JavaScript (fetch)

```javascript
const response = await fetch(
  "http://localhost:8000/api/Scheduler/programarPartidosGreedy",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      canchas_ids: [1, 2, 3],
      torneos_ids: [10, 11],
    }),
  }
);
const data = await response.json();
console.log(data);
```

## Ejemplo de response (OK)

```json
{
  "respuesta": "OK",
  "mensaje": "",
  "data": {
    "partidos_asignados": [
      {
        "partido_id": "g1-m1",
        "torneo_id": 1,
        "grupo_id": 1,
        "equipo_a_id": 100,
        "equipo_b_id": 101,
        "espacio_id": 10,
        "cancha_id": 5,
        "fecha": "2026-01-10",
        "hora": "20:00",
        "fecha_hora": "2026-01-10T20:00:00"
      },
      {
        "partido_id": "g1-m2",
        "torneo_id": 1,
        "grupo_id": 1,
        "equipo_a_id": 102,
        "equipo_b_id": 103,
        "espacio_id": 11,
        "cancha_id": 5,
        "fecha": "2026-01-11",
        "hora": "20:00",
        "fecha_hora": "2026-01-11T20:00:00"
      }
    ],
    "partidos_pendientes": [],
    "espacios_utilizados": [
      {
        "espacio_id": 10,
        "cancha_id": 5,
        "fecha": "2026-01-10",
        "hora": "20:00",
        "fecha_hora": "2026-01-10T20:00:00",
        "cuenta_id": 7
      },
      {
        "espacio_id": 11,
        "cancha_id": 5,
        "fecha": "2026-01-11",
        "hora": "20:00",
        "fecha_hora": "2026-01-11T20:00:00",
        "cuenta_id": 7
      }
    ],
    "espacios_libres": []
  }
}
```

## Ejemplo de response (sin torneos)

```json
{
  "respuesta": "ERROR",
  "mensaje": "No se econtraron torneos",
  "data": null
}
```

## Ejemplo de response con pendientes

```json
{
  "respuesta": "OK",
  "mensaje": "",
  "data": {
    "partidos_asignados": [],
    "partidos_pendientes": [
      {
        "partido": {
          "partido_id": "g1-m9",
          "torneo_id": 1,
          "grupo_id": 1,
          "equipo_a_id": 120,
          "equipo_b_id": 121
        },
        "motivo": "sin_disponibilidad_4_jugadores",
        "detalle": null
      }
    ],
    "espacios_utilizados": [],
    "espacios_libres": [
      {
        "espacio_id": 99,
        "cancha_id": 3,
        "fecha": "2026-01-20",
        "hora": "21:00",
        "fecha_hora": "2026-01-20T21:00:00",
        "cuenta_id": 7
      }
    ]
  }
}
```

## Notas practicas

- El endpoint no persiste datos, solo devuelve propuesta.
- El endpoint arma internamente todos los insumos de scheduling desde canchas_ids y torneos_ids.
- Los formatos de fecha recomendados son ISO 8601.
- Si se requiere mayor calidad global de asignacion, este scheduler puede evolucionar a busqueda local o backtracking; actualmente prioriza velocidad y simplicidad.
