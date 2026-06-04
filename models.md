Generame estas tablas en modelos

La tabla se llama asi en la base de datos sportmob_v2.cancha

ID                INT PK
- nombreCancha      VARCHAR(45) NULL
- ubicacionCancha   VARCHAR(100) NULL
- estadoCancha      TINYINT NULL
- ultimaModificacion DATETIME NULL
- idUsuario         INT NULL
- usuarioC          INT NULL
- cuentaId          INT NULL
- fechas            INT NULL

La tabla se llama asi en la base de datos sportmob_v2.fechas

- id (INT, PK)
- dia (VARCHAR(150)) NULL
- horarios (INT) NULL
- categoriaID (INT) NULL
- canchaID (INT) NULL

La tabla se llama asi en la base de datos sportmob_v2.horarios

- id (INT, PK)
- horario (VARCHAR(150)) NULL
- fechaID (INT) NULL


La tabla se llama asi en la base de datos sportmob_v2.torneo

Descripción:
Representa un torneo de pádel o deporte similar. Contiene la configuración general, estructura de grupos, fechas, costos y reglas de generación de partidos.

Campos principales:

Identificación
- id (INT, PK)
- nombre (VARCHAR) NULL
- tipoDeporte (VARCHAR) NULL
- estado (TINYINT) NULL

Estructura del torneo
- categorias (INT) NULL
- noGrupos (INT) NULL
- equiposPorgrupo (INT) NULL
- parejasEnGrupos (INT) NULL
- noJornadas (INT) NULL
- liguilla (TINYINT) NULL
- cantidadEquiposLiguilla (INT) NULL
- aplicaPlayIn (TINYINT) NULL

Fechas
- fechaInicio (VARCHAR) NULL
- fechaFin (VARCHAR) NULL
- FaseGrupoFin (DATETIME) NULL
- diasJuego (VARCHAR) NULL
- horaInicioTorneo (VARCHAR) NULL

Inscripciones
- cerrarInscripciones (TINYINT) NULL
- cerrarRegistrosPadel (TINYINT) NULL

Costos
- preventa (DOUBLE) NULL
- venta (DOUBLE) NULL
- finPreventa (VARCHAR) NULL
- tipoPago (VARCHAR) NULL

Configuración de partidos
- permiteEmpate (TINYINT) NULL
- cantidadSets (INT) NULL
- numeroJuegos (INT) NULL
- numeroJuegosTiebreak (INT) NULL
- modoDesempateScore (VARCHAR) NULL
- tiempoUsoCanchas (VARCHAR) NULL

Disponibilidad y calendarización
- solicitarHorario (TINYINT) NULL
- horasAntesNotificar (INT) NULL

Generación automática
- tipoGeneracion (INT) NULL
- dividirRR (TINYINT) NULL
- noGruposRR (INT) NULL

Arbitraje
- tieneArbitraje (TINYINT) NULL
- montoArbitraje (DOUBLE) NULL

Puntuación
- imc (DOUBLE) NULL
- pmr (DOUBLE) NULL

Estado y control
- finalizarTorneo (TINYINT) NULL
- ultimaModificacion (DATETIME) NULL
- usuarioC (INT) NULL

Web
- showWebView (TINYINT) NULL
- urlTorneo (VARCHAR) NULL


La tabla se llama asi en la base de datos sportmob_v2.equipo

Descripción:
Representa una pareja o equipo inscrito en un torneo y asignado a un grupo específico.

Relaciones:
- Torneo -> torneo.id
- Grupo -> null
- Categoria -> null

Campos principales:

Identificación
- id (INT, PK) NULL
- nombreEquipo (VARCHAR) NULL
- alias (VARCHAR) NULL
- claveEquipo (VARCHAR) NULL

Relaciones
- Torneo (INT)
- Grupo (INT) NULL
- Categoria (INT) NULL

Información visual
- fotoEquipo (VARCHAR) NULL
- fotoEquipo2 (VARCHAR) NULL
- fotoUniforme (VARCHAR) NULL

Registro
- fechaRegistroEquipo (DATETIME) NULL
- cuentaId (INT) NULL

Estado de inscripción
- jugadoresPagados (INT) NULL
- modoPago (VARCHAR) NULL
- importe (DOUBLE) NULL
- pagado (TINYINT) NULL
- estadoRegistroParejas (VARCHAR) NULL

Estado deportivo
- eliminado (TINYINT) NULL
- baja (TINYINT) NULL
- clasificado (TINYINT) NULL

Estadísticas
- juegosJugados (INT) NULL
- juegosGanados (INT) NULL
- juegosEmpatados (INT) NULL
- juegosPerdidos (INT) NULL
- golesAFavor (DOUBLE) NULL
- golesEnContra (DOUBLE) NULL
- diferenciaDeGoles (DOUBLE) NULL
- puntos (DOUBLE) NULL
- puntosRanking (INT) NULL
- ptsExtrasOAmosnetacion (DOUBLE) NULL

Round Robin
- grupoRR (INT) NULL

Control
- ultimaModificacion (DATETIME) NULL
- idUsuario (INT) NULL
- usuarioC (INT) NULL


La tabla se llama asi en la base de datos sportmob_v2.jugadorequipo

Descripción:
Tabla puente que relaciona jugadores con equipos (parejas).

Relaciones:
- jugadorID -> jugador.id
- equipoID -> equipo.id

Campos:
- id (INT, PK)
- jugadorID (INT)
- equipoID (INT)


La tabla se llama sportmob_v2.TorneoDisponibilidadJugador;

Descripción:
Almacena los horarios en los que un jugador indica que puede participar dentro de un torneo específico.

Relaciones:
- idTorneo -> torneo.id
- idJugador -> jugador.id

Campos:
- id (INT, PK)
- idTorneo (INT)
- idJugador (INT)
- fecha (DATETIME)
- hora (VARCHAR(50))
- alta (DATETIME)

Índices:
- idx_torneo (idTorneo)
- idx_jugador (idJugador)
- idx_torneo_jugador (idTorneo, idJugador)


La tabla se llama sportmob_v2.jornadas;

La entidad representa una jornada o fase dentro de un torneo de pádel. Puede utilizarse tanto para jornadas de fase de grupos como para etapas de liguilla.

Propiedades:

Id (int): Identificador único de la jornada.
Nombre (string): Nombre descriptivo de la jornada.
FechaInicio (DateTime?): Fecha y hora de inicio de la jornada.
FechaFin (DateTime?): Fecha y hora de finalización de la jornada.

Información de tipo de jornada:

TipoJornada (string): Tipo de jornada. Ejemplos: "Grupos", "Liguilla", "Final", "Semifinal".
NombreLiguilla (string): Nombre de la liguilla o bracket al que pertenece.
EtapaLiguilla (string): Etapa de la liguilla. Ejemplos: Octavos, Cuartos, Semifinal, Final.
LlaveLiguilla (int?): Identificador de la llave dentro de la liguilla.
NumeroLlave (int?): Número consecutivo de la llave.
PosicionLlave (int?): Posición que ocupa dentro del bracket.
SiguienteJornada (int?): Id de la siguiente jornada relacionada en la progresión del bracket.

Información de fase de grupos:

NumeroJornada (string): Número o nombre de la jornada dentro del torneo.
JornadaFinalizada (bool?): Indica si la jornada ya fue completada.

Relaciones:

CategoriaId (int?): Categoría a la que pertenece la jornada.
TorneoId (int?): Torneo al que pertenece la jornada.
Partidos (int?): Cantidad de partidos asociados a la jornada.

Auditoría:

TorneoC (int?): Torneo de creación o referencia histórica.
UltimaModificacion (DateTime?): Fecha de última modificación.
IdUsuario (int?): Usuario que realizó la última modificación.
UsuarioC (int?): Usuario creador del registro.
CuentaId (int?): Cuenta propietaria del registro.

Consideraciones:

Mapear los campos tinyint como bool?.
Utilizar propiedades nullable para todos los campos que permiten NULL en la base de datos.
Agregar navegación opcional hacia Torneo, Categoría y Usuario si existen dichas entidades en el proyecto.
Utilizar nombres de propiedades en PascalCase siguiendo las convenciones de C#.


La tabla se llama sportmob_v2.partidosjornadas;

Descripción:
Representa un partido programado entre dos equipos dentro de un torneo.

Relaciones:
- idJornada -> jornada.id
- idEquipo1 -> equipo.id
- idEquipo2 -> equipo.id
- lugar -> NULL
- grupoID -> NULL

Campos principales:

Identificación
- id (INT, PK)

Participantes
- idEquipo1 (INT) NULL
- idEquipo2 (INT) NULL
- grupoID (INT) NULL

Programación
- fechaHoraPartido (DATETIME) NULL
- hora (VARCHAR) NULL
- lugar (INT) NULL
- etiquetaCancha (VARCHAR) NULL

Resultado
- marcadorEquipo1 (INT) NULL
- marcadorEquipo2 (INT) NULL
- estadoPartido (VARCHAR) NULL

Control
- tipoPartido (VARCHAR) NULL
- partidoSugerido (TINYINT) NULL
- modificadoManual (TINYINT) NULL
- currentStatePadel (VARCHAR) NULL

