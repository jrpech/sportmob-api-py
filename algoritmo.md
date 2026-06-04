Necesito tu ayuda para diseñar e implementar un método en mi API desarrollada con Python y FastAPI que genere una propuesta de calendario de partidos para múltiples torneos de pádel.

IMPORTANTE:

* El método NO debe guardar información en la base de datos.
* El método únicamente debe generar una propuesta de calendario en memoria.
* Antes de escribir código, analiza completamente el problema.
* No implementes nada todavía.
* Primero describe el algoritmo, estructuras de datos, flujo y estrategia de asignación.
* Una vez aprobado el diseño, procederemos con la implementación en Python/FastAPI.

# Contexto General

Necesito construir un motor de scheduling para torneos de pádel.

El sistema debe generar automáticamente un calendario de partidos considerando:

* Disponibilidad de canchas.
* Disponibilidad de jugadores.
* Configuración de grupos.
* Equipos registrados.
* Fechas de inicio y fin de cada torneo.
* Múltiples torneos compartiendo los mismos espacios.

El resultado debe ser una propuesta de calendario sin persistir datos.

# Resultado esperado

El método debe devolver una estructura similar a:

[
{
"torneoId": 1,
"grupoId": 19283891,
"equipoA": 100,
"equipoB": 101,
"fecha": "2026-01-15",
"hora": "20:00",
"canchaId": 5
}
]

También debe devolver:

* Partidos asignados.
* Partidos pendientes.
* Espacios utilizados.
* Espacios libres.

# Obtención de espacios disponibles

Los espacios disponibles deben obtenerse mediante:

Cancha -> Fechas -> Horarios

Las canchas deben filtrarse por cuentaId.

Ejemplo:

Cancha 1
Lunes
20:00
21:00

Espacios generados:

* Cancha 1 - Lunes - 20:00
* Cancha 1 - Lunes - 21:00

Cada combinación Cancha + Día + Hora representa un espacio disponible.

Los espacios deben ordenarse cronológicamente.

# Obtención de torneos

Los torneos asociados a una cuenta se obtienen desde CuentaTorneo.

Filtrar por:

* cuentaId
* estado = false

Solo los torneos activos participan en el proceso.

# Configuración de grupos

Los torneos pueden estar configurados con uno o varios grupos.

Campos:

* dividirRR
* noGruposRR

Reglas:

Si dividirRR = true:

* Existen múltiples grupos.
* La cantidad de grupos es noGruposRR.

Si dividirRR = false:

* Existe un único grupo general.

# Referencia de lógica actual (C#)

Actualmente existe una implementación en una API .NET que utiliza la siguiente lógica para determinar cómo están conformados los grupos de un torneo.

Esta implementación NO debe copiarse literalmente, pero sí debe utilizarse como referencia para entender las reglas de negocio actuales.

```csharp
public List<Grupo> getParejasRRByTorneo(int torneoID)
{
    using var equipoR = new EquipoRepository();
    using var torneoR = new TorneoRepository();

    var retorno = new List<Grupo>();

    var infoTorneo = torneoR.getById(torneoID);

    var dividirGrupos = infoTorneo.dividirRR ?? false;

    var parejasRegistradas = equipoR.getXTorneo(torneoID);

    if (dividirGrupos == true)
    {
        var noGruposRR = infoTorneo.noGruposRR ?? 2;

        for (int i = 0; i < noGruposRR; i++)
        {
            var equiposGrupo = parejasRegistradas
                .Where(p => p.grupoRR == (19283891 + i))
                .ToList();

            var item = new Grupo
            {
                id = 19283891 + i,
                nombre = $"GRUPO {i + 1} de {equiposGrupo.Count} PAREJAS",
                equiposGrupo = equiposGrupo
            };

            retorno.Add(item);
        }
    }
    else
    {
        var equiposTodos = parejasRegistradas
            .Where(p => p.grupoRR == 19283890)
            .ToList();

        var item = new Grupo();

        item.id = 19283890;
        item.nombre = $"GRUPO GRAL {equiposTodos.Count} PAREJAS";
        item.equiposGrupo = equiposTodos;

        retorno.Add(item);
    }

    return retorno;
}
```

# Reglas derivadas de esta implementación

* Si dividirRR = false:

  * Existe un único grupo.
  * El identificador utilizado es 19283890.
  * Todos los equipos pertenecen a ese grupo.

* Si dividirRR = true:

  * Existen múltiples grupos.
  * La cantidad de grupos está definida por noGruposRR.
  * Los grupos utilizan identificadores consecutivos iniciando en 19283891.
  * Cada equipo tiene un campo grupoRR que indica a qué grupo pertenece.

Por lo tanto, para generar los partidos Round Robin, primero se debe reconstruir esta agrupación y posteriormente generar los enfrentamientos únicamente entre equipos del mismo grupo.


# Obtención de equipos

Los equipos registrados se obtienen desde la tabla Equipo.

Filtros:

* torneoId
* baja = false

# Generación de partidos

Dentro de cada grupo se debe generar un Round Robin completo.

Ejemplo:

Grupo A:

* Equipo 1
* Equipo 2
* Equipo 3
* Equipo 4

Partidos:

* Equipo 1 vs Equipo 2
* Equipo 1 vs Equipo 3
* Equipo 1 vs Equipo 4
* Equipo 2 vs Equipo 3
* Equipo 2 vs Equipo 4
* Equipo 3 vs Equipo 4

Los partidos solamente pueden generarse entre equipos del mismo grupo.

# Disponibilidad de jugadores

La disponibilidad se encuentra en:

TorneoDisponibilidadJugador

Campos:

* idTorneo
* idJugador

# Disponibilidad de parejas

Una pareja solamente puede jugar cuando ambos integrantes tienen disponibilidad.

La disponibilidad de la pareja es la intersección de ambos jugadores.

# Disponibilidad de partidos

Un partido solamente puede jugarse cuando:

* Ambos integrantes del Equipo A están disponibles.
* Ambos integrantes del Equipo B están disponibles.

La disponibilidad final del partido será la intersección de disponibilidad de los cuatro jugadores.

# Restricciones

* Un espacio solo puede utilizarse una vez.
* Todos los torneos comparten los mismos espacios.
* No puede existir traslape de horarios.
* Un equipo no puede jugar dos partidos al mismo tiempo.
* Se debe respetar el rango fechaInicio - fechaFin del torneo.
* Los espacios deben asignarse cronológicamente.

# Casos sin solución

Si un partido no puede asignarse:

* Por falta de espacios.
* Por incompatibilidad de disponibilidad.

Debe agregarse a una lista de pendientes.

# Lo que necesito de ti

Antes de implementar:

1. Diseña el algoritmo completo.
2. Define las estructuras de datos recomendadas en Python.
3. Explica cómo modelarías los espacios.
4. Explica cómo calcularías las intersecciones de disponibilidad.
5. Explica cómo resolverías la asignación de partidos.
6. Analiza complejidad y rendimiento.
7. Identifica posibles cuellos de botella.

No generes código todavía.
Primero quiero validar la arquitectura de la solución.
