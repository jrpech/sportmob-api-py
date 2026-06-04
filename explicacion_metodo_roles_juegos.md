Necesito tu ayuda para poder construir un metodo en mi API para generar sin guardar aun, un calendario de partidos para n torneos
Primero debes obtener los espacios disponibles que se podran usar para que todos los torneos puedan tener espacios para jugar
estos espacios los puedes obtener de la relacion que existe entre lo siguiente

Obtener espacios
cancha -> fechas -> horarios

en cancha quiero que para obtener esos espacios los busques por cuentaId

Ejemplo relacion de espacios entre la relacion

C1 -> Lun -> 20:00 -> este es un espacio

Para obtener los torneos relacionados a una cuenta los puedes obtener de la siguiente tabla cuentatorneo
atraves de ella puedes filtrar por cuenta, el extra seria tomar los torneos que tengan el estado igual a false

despues de ello tendras que conocer como estas compuestos los grupos y que equipos hay en ello, te dare una contextualizacion de la siguiente forma

Las columnas que existen en torneo, se puede conocer como esta configurado si es por grupos o un solo grupo son
- dividirRR (TINYINT) -> si este valor esta en true, el noGruposRR tiene un numero distinto o mayor a 1
- noGruposRR (INT) -> este valor contiene un numero distinto o mayor a 1

atraves de ello puedes saber cuantos grupos se tienen configurado

un ejemplo de codigo que uso en mi API de net core C# es este

//Metodo que se encarga de buscar a las parejas del torneo separando por grupos si esta aplicado desde el torneo
public List<Grupo> getParejasRRByTorneo(int torneoID)
{
    //Repositorios
    using var equipoR = new EquipoRepository();
    using var torneoR = new TorneoRepository();

    //retorno
    var retorno = new List<Grupo>();

    //Informacion del torneo
    var infoTorneo = torneoR.getById(torneoID);

    //Consultamos la config del torneo para saber si aplica la separacion de grupos
    var dividirGrupos = infoTorneo.dividirRR ?? false;

    //Buscamos a las parejas registrados
    var parejasRegistradas = equipoR.getXTorneo(torneoID);

    if (dividirGrupos == true)
    {
        var noGruposRR = infoTorneo.noGruposRR ?? 2;

        for (int i = 0; i < noGruposRR; i++)
        {
            var equiposGrupo = parejasRegistradas.Where(p => p.grupoRR == (19283891 + i)).ToList();

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
        var equiposTodos = parejasRegistradas.Where(p => p.grupoRR == 19283890).ToList();

        var item = new Grupo();

        item.id = 19283890;
        item.nombre = $"GRUPO GRAL {equiposTodos.Count} PAREJAS";
        item.equiposGrupo = equiposTodos;

        retorno.Add(item);

    }

    return retorno;
}

ahora de aqui, para poder conocer que equipos estan registrados de manera global en el torneo se hace atraves del modelo equipo
alli tienes una propiedad que se llama Torneo y con eso filtras y considera una propiedad mas que es baja que sea false
asi trabaja este metodo var parejasRegistradas = equipoR.getXTorneo(torneoID);

Despues de eso tu deberas conocer como estan las preferencias de cada jugador en un equipo, esto servira para armar una interseccion de horarios
donde los jugadores dicen que dia y horario pueden jugar y con eso armar los partidos

la tabla se llama TorneoDisponibilidadJugador alli mediante las columnas idTorneo y idJugador puedes saber como estan 
los dias en los que el puede jugar cada jugador en el torneo


Ahora lo que se debe lograr es lo siguiente:

Quiero mediante un metodo en mi API, un proceso para armar un calendario de partidos para padel
este metodo debe darme los dias en los que habra partidos considerando la fecha de inicio y fin del torneo, con estos valores
se puede conocer si es torneo de una semana o de n semanas, el equilibrio de que partidos van dia a dia, depende del dia que tienen las canchas
te sugiero ordenar los dias, si por ejemplo existen 6 espacios para Lun, pues son seis espacios, el criterio mas complejo es decir que partidos
van ya que estos dependen de la disponibilidad de cada jugador y de alli saber realmente cuando pueden jugar cada pareja
otra cosa que debes tener en cuenta es que por cada torneo en los grupos, se dan entre los equipos del mismo grupo





