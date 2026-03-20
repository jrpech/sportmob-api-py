using dosxl.Models.Models;
using dosxl.Models.Request;
using dosxl.Utils;
using FluentNHibernate.Conventions;
using FluentNHibernate.Testing.Values;
using NHibernate.Criterion;
using System;
using System.Collections.Generic;
using System.Linq;

namespace dosxl.Models.Repository
{
    public class PartidosRepository : RepositoryBase<PartidosJornadas>
    {
        public List<PartidosJornadas> getAll()
        {
            return _session.Query<PartidosJornadas>().ToList();
        }
        public PartidosJornadas getByIdPartido(int id)
        {
            return _session.Query<PartidosJornadas>().Where(x => x.id == id).FirstOrDefault();
        }
        
        public List<PartidosJornadas> partidosConEstadoPorJugar(int idEquipo)
        {
            return _session.Query<PartidosJornadas>().Where(
                x => ((x.idEquipo1.id == idEquipo && x.idEquipo2 != null ) || (x.idEquipo2.id == idEquipo && x.idEquipo1 != null))  &&
                x.estadoPartido == "POR JUGAR"
                ).OrderBy(x => x.fechaHoraPartido).ToList();
        }
        public List<PartidosJornadas> partidosConEstadoFinalizadoPartidosPorEquipo(int idEquipo)
        {
            return _session.Query<PartidosJornadas>().Where(
                x => ((x.idEquipo1.id == idEquipo && x.idEquipo2 != null) || (x.idEquipo2.id == idEquipo && x.idEquipo1 != null)) &&
                x.estadoPartido == "FINALIZADO"
                ).OrderBy(x => x.fechaHoraPartido).ToList();
        }
        public List<PartidosJornadas> partidosConEstadofinalizado(int idEquipo)
        {
            return _session.Query<PartidosJornadas>().Where(
                x=> (x.idEquipo1.id == idEquipo || x.idEquipo2.id == idEquipo) &&
                x.estadoPartido == "FINALIZADO" &&
                x.tipoPartido == "REGULAR"
                ).OrderByDescending(x => x.fechaHoraPartido)
                              .ToList(); 
        }
        public List<PartidosJornadas> partidosEmpatados(int idEquipo)
        {
            return _session.Query<PartidosJornadas>().Where(
                x => (x.idEquipo1.id == idEquipo || x.idEquipo2.id == idEquipo) &&  x.marcadorEquipo1 == x.marcadorEquipo2 &&
                x.estadoPartido == "FINALIZADO" &&
                x.tipoPartido == "REGULAR"
                ).ToList();
        }
        public List<PartidosJornadas> partidosGanados(int idEquipo)
        {
            return _session.Query<PartidosJornadas>().Where(
                x => ((x.idEquipo1.id == idEquipo && x.marcadorEquipo1 > x.marcadorEquipo2) ||( x.idEquipo2.id == idEquipo && x.marcadorEquipo2 > x.marcadorEquipo1)) &&
                x.estadoPartido == "FINALIZADO" &&
                x.tipoPartido == "REGULAR"
                ).ToList();
        }
        public List<PartidosJornadas> partidosPerdidos(int idEquipo)
        {
            return _session.Query<PartidosJornadas>().Where(
                x => ((x.idEquipo1.id == idEquipo && x.marcadorEquipo1 < x.marcadorEquipo2) || (x.idEquipo2.id == idEquipo && x.marcadorEquipo2 < x.marcadorEquipo1)) &&
                x.estadoPartido == "FINALIZADO" &&
                x.tipoPartido == "REGULAR"
                ).ToList();
        }
        public List<PartidosJornadas> partidosConGolesAfavorEquipo1(int idEquipo)
        {
          return _session.Query<PartidosJornadas>().Where(
                x => (x.idEquipo1.id == idEquipo ) &&
                x.estadoPartido == "FINALIZADO" &&
                x.tipoPartido == "REGULAR"
                ).ToList();

        }
        public List<PartidosJornadas> partidosConGolesAfavorEquipo2(int idEquipo)
        {
            return _session.Query<PartidosJornadas>().Where(
                  x => (x.idEquipo2.id == idEquipo) &&
                  x.estadoPartido == "FINALIZADO" &&
                x.tipoPartido == "REGULAR"
                  ).ToList();

        }
        public PartidosJornadas getById(int id)
        {
            return _session.Query<PartidosJornadas>().Where(x =>
                      x.id == id).FirstOrDefault();
        }

        public PartidosJornadas porIDyEquipo1(int id, int idequipo)
        {
            return _session.Query<PartidosJornadas>().Where(x =>
                      x.id == id && x.idEquipo1.id == idequipo).FirstOrDefault();
        }
        public PartidosJornadas porIDyEquipo2(int id, int idequipo)
        {
            return _session.Query<PartidosJornadas>().Where(x =>
                      x.id == id && x.idEquipo2.id == idequipo).FirstOrDefault();
        }
        public PartidosJornadas ultimoid()
        {
            var lastID = _session.CreateCriteria(typeof(PartidosJornadas))
                .SetProjection(Projections.Max("id")).UniqueResult();
            int idjornada = int.Parse(lastID.ToString());

            return _session.Query<PartidosJornadas>().Where(x => x.id == idjornada).FirstOrDefault();
        }
        
        public List<PartidosJornadas> partidosPorJonada(int jornada, DateTime fechainicio, DateTime fechafin)
        {
            return _session.Query<PartidosJornadas>().Where(x => x.idJornada.id == jornada && x.fechaHoraPartido >= fechainicio && x.fechaHoraPartido <= fechafin).ToList();
        }
        public List<PartidosJornadas> partidosPorJonadaID(int jornada)
        {
            return _session.Query<PartidosJornadas>().Where(x => x.idJornada.id == jornada).ToList();
        }
        public List<PartidosJornadas> partidosPorLiguilla(int idJornada)
        {
            return _session.Query<PartidosJornadas>().Where(x => 
            x.idJornada.id == idJornada &&
            x.tipoPartido == "LIGUILLA").ToList();
        }
        public Partido crearPartidoLiguilla(List<PartidosJornadas> partidos, int siguienteJornada)
        {
            EventosPartidoRepository eventol = new EventosPartidoRepository();
            Partido partido = new Partido();
            PartidosJornadas partidodato = new PartidosJornadas();

            if (partidos.Count > 1)
                partidodato = partidos[1];
            else
                partidodato = partidos[0]; 

            var marcadorEquipo1 = 0;
            var marcadorEquipo2 = 0;
            
            foreach (PartidosJornadas elem in partidos) 
            {
                if (elem.idaOvuelta == "IDA") 
                {
                    partido.equipo1 = elem.idEquipo1;
                    partido.equipo2 = elem.idEquipo2;

                  partido.marcadorIda = elem.marcadorEquipo1 + "-" + elem.marcadorEquipo2;

                  marcadorEquipo1 = marcadorEquipo1 + elem.marcadorEquipo1;
                  marcadorEquipo2 = marcadorEquipo2 + elem.marcadorEquipo2;
                   
                  partido.estadoPartidoIda = elem.estadoPartido;
                  partido.idPartidoIda = elem.id;
                  partido.fechaHoraIda = elem.fechaHoraPartido;
                  partido.lugarPartidoIda = elem.lugar;
                  partido.horaIda = elem.hora;

                }
                if (elem.idaOvuelta == "VUELTA") 
                { 
                  partido.marcadorVuelta = elem.marcadorEquipo1 + "-" + elem.marcadorEquipo2;
                    
                  partido.estadoPartidoVuelta = elem.estadoPartido;
                  partido.idPartidoVuelta = elem.id;
                  partido.fechaHoraVuelta = elem.fechaHoraPartido;
                  partido.lugarPartidoVuelta = elem.lugar;
                  partido.horaVuelta = elem.hora;

                    marcadorEquipo1 = marcadorEquipo1 + elem.marcadorEquipo2;
                    marcadorEquipo2 = marcadorEquipo2 + elem.marcadorEquipo1;
                }                  
            }

            partido.marcadorGlobal = marcadorEquipo1 +"-"+ marcadorEquipo2;
            
            var partidosfinalizados = partidos.Where(x => x.estadoPartido == "FINALIZADO");
            var totaldepartidos = partidos.Count();

            if (partidosfinalizados.Count() == totaldepartidos)
            {
                var penalesequipo1 = eventol.penalesAnotados(partidodato.id, partidos[0].idEquipo1.id);
                var penalesequipo2 = eventol.penalesAnotados(partidodato.id, partidos[0].idEquipo2.id);

                if (penalesequipo1.Count != 0 || penalesequipo2.Count != 0)
                {
                 partido.tandaPenales = "(" + penalesequipo1.Count + "-" + penalesequipo2.Count + ")";
                }
                else
                    partido.tandaPenales = "";


                equipoEliminadoliguillaYequipoPasa(partidos[0], marcadorEquipo1, marcadorEquipo2, siguienteJornada,penalesequipo1.Count, penalesequipo2.Count);

            }
            return partido;
        }
        public bool equipoEliminadoliguillaYequipoPasa(PartidosJornadas partido, int marcador1, int marcador2, int siguienteJornada, int totalpenale1,int totalpenale2)
        {
            var  result = false;

            EquipoRepository equipol = new EquipoRepository();
            EventosPartidoRepository eventol = new EventosPartidoRepository();
            JornadasRepository jornadal = new JornadasRepository();
            Jornadas jornadatercerlugar = new Jornadas();
            //penales
            if (marcador1 == marcador2)
            {
                if (totalpenale1 > totalpenale2)
                {
                    if (partido.idJornada.etapaLiguilla != "SEMIFINAL")
                        equipol.cambiaestadoequipo(partido.idEquipo2.id);

                    siguientePartido(partido.idEquipo1.id, siguienteJornada, partido.idJornada.posicionLlave);

                    if (partido.idJornada.etapaLiguilla == "SEMIFINAL")
                    {
                        jornadatercerlugar = jornadal.byetapajornada("TERCERLUGAR", partido.idJornada.nombreLiguilla);
                        siguientePartido(partido.idEquipo2.id, jornadatercerlugar.id, partido.idJornada.posicionLlave);
                    }
                    
                }

                if (totalpenale1 < totalpenale2)
                {
                    if (partido.idJornada.etapaLiguilla != "SEMIFINAL")
                        equipol.cambiaestadoequipo(partido.idEquipo1.id);

                    siguientePartido(partido.idEquipo2.id, siguienteJornada, partido.idJornada.posicionLlave);

                    if (partido.idJornada.etapaLiguilla == "SEMIFINAL")
                    {
                        jornadatercerlugar = jornadal.byetapajornada("TERCERLUGAR", partido.idJornada.nombreLiguilla);

                        siguientePartido(partido.idEquipo1.id, jornadatercerlugar.id, partido.idJornada.posicionLlave);
                    }
                }
                
                result = true;
            }
            else
            {
                if (marcador1 > marcador2)
                {
                    if (partido.idJornada.etapaLiguilla != "SEMIFINAL")
                        equipol.cambiaestadoequipo(partido.idEquipo2.id);

                    siguientePartido(partido.idEquipo1.id, siguienteJornada, partido.idJornada.posicionLlave);

                    if (partido.idJornada.etapaLiguilla == "SEMIFINAL")
                    {
                        jornadatercerlugar = jornadal.byetapajornada("TERCERLUGAR", partido.idJornada.nombreLiguilla);
                        siguientePartido(partido.idEquipo2.id, jornadatercerlugar.id, partido.idJornada.posicionLlave);
                    }
                }

                if (marcador1 < marcador2)
                {
                    if (partido.idJornada.etapaLiguilla != "SEMIFINAL")
                        equipol.cambiaestadoequipo(partido.idEquipo1.id);

                    siguientePartido(partido.idEquipo2.id, siguienteJornada, partido.idJornada.posicionLlave);

                    if (partido.idJornada.etapaLiguilla == "SEMIFINAL")
                    {
                        jornadatercerlugar = jornadal.byetapajornada("TERCERLUGAR", partido.idJornada.nombreLiguilla);
                        siguientePartido(partido.idEquipo1.id, jornadatercerlugar.id, partido.idJornada.posicionLlave);
                    }
                }
                result = true;
            }


            return result;
        }

        public bool siguientePartido(int equipoID, int siguienteJornada, int posicionLlave)
        {
            bool result = false;
            EquipoRepository equipol = new EquipoRepository();
            List<PartidosJornadas> partidos = new List<PartidosJornadas>();
            PartidosJornadas partido = new PartidosJornadas();
            Equipo equipo = new Equipo();
            partidos = partidosPorJonadaID(siguienteJornada);


            if (partidos.Count != 0) 
            {
                equipo = equipol.getEquipoPorId(equipoID);

                foreach (PartidosJornadas elem in partidos) 
                {
                    if (elem.idaOvuelta == "IDA")
                    {
                       partido = getById(elem.id);

                        if (posicionLlave == 1)
                        {
                            partido.idEquipo1 = equipo;
                        }
                        else
                        if (posicionLlave == 2) 
                        {
                               partido.idEquipo2 = equipo;
                        }
                        save(partido);
                    }
                    if (elem.idaOvuelta == "VUELTA")
                    {
                        partido = getById(elem.id);

                        if (posicionLlave == 1)
                        {
                            partido.idEquipo2 = equipo;
                        }
                        else
                        if (posicionLlave == 2)
                        {
                            partido.idEquipo1 = equipo;
                        }
                        save(partido);
                        
                    }
                }
                result = true;
            }

            return result;
        }
        public int marcadorPorequipo(int equipoID, int Jornada)
        {
            var result = 0;
            EquipoRepository equipol = new EquipoRepository();
            List<PartidosJornadas> partidos = new List<PartidosJornadas>();
            PartidosJornadas partido = new PartidosJornadas();
            PartidosJornadas partido1 = new PartidosJornadas();
            PartidosJornadas partido2 = new PartidosJornadas();

            partidos = partidosPorJonadaID(Jornada);


            if (partidos.Count != 0)
            {
                foreach (PartidosJornadas elem in partidos)
                {
                    if (elem.idaOvuelta == "IDA") 
                    { 
                        partido1 = porIDyEquipo1(elem.id, equipoID);
                        partido2 = porIDyEquipo2(elem.id, equipoID);

                        if (partido1 != null)
                        {
                            result = result + partido1.marcadorEquipo1;
                        }
                        if (partido2 != null)
                        {
                            result = result + partido2.marcadorEquipo2;
                        }

                    }

                    if (elem.idaOvuelta == "VUELTA")
                    {
                        partido1 = porIDyEquipo1(elem.id, equipoID);
                        partido2 = porIDyEquipo2(elem.id, equipoID);

                        if (partido1 != null)
                        {
                            result = result + partido1.marcadorEquipo1;
                        }
                        if (partido2 != null)
                        {
                            result = result + partido2.marcadorEquipo2;
                        }

                    }
                }
            }

            return result;
        }

        public bool save(PartidosJornadas partidosJornadas)
        {
            bool result = false;

            PartidosJornadas partidosUpdate = getById(partidosJornadas.id);
               
                _session.Update(partidosUpdate);
                _session.Flush();
                result = true;


            return result;
        }
       
        public bool guardarDatosTablaGeneral()
        {
            bool result = false;
            EquipoRepository equipol = new EquipoRepository();
            List<Equipo> equipos = equipol.getAll();
            List<Equipo> tabla = new List<Equipo>();
                

            var numero = 0;
            var golesAfavorlocal = 0;
            var golesAfavorvisitante = 0;
            var golesEncontra1 = 0;
            var golesEncontra2 = 0;

            foreach (Equipo elem in equipos)
            {
                var partidosPorequipo = partidosConEstadofinalizado(elem.id);
                if (partidosPorequipo != null)
                    elem.juegosJugados = partidosPorequipo.Count();

                var partidosganados = partidosGanados(elem.id);
                if (partidosganados != null)
                    elem.juegosGanados = partidosganados.Count();

                var partidosempatados = partidosEmpatados(elem.id);
                if (partidosempatados != null)
                    elem.juegosEmpatados = partidosempatados.Count();

                var partidosperdidos = partidosPerdidos(elem.id);
                if (partidosperdidos != null)
                    elem.juegosPerdidos = partidosperdidos.Count();


                List<PartidosJornadas> local = partidosConGolesAfavorEquipo1(elem.id);
                List<PartidosJornadas> visitante = partidosConGolesAfavorEquipo2(elem.id);

                foreach (PartidosJornadas partido1 in local)
                {
                    if (local != null)
                    {

                        golesAfavorlocal += partido1.marcadorEquipo1;
                    }
                }
                foreach (PartidosJornadas partido2 in visitante)
                {
                    if (visitante != null)
                    {

                        golesAfavorvisitante += partido2.marcadorEquipo2;
                    }
                }

                foreach (PartidosJornadas partidoUno in local)
                {
                    if (local != null)
                    {

                        golesEncontra1 += partidoUno.marcadorEquipo2;
                    }
                }
                foreach (PartidosJornadas partidoDos in visitante)
                {
                    if (visitante != null)
                    {

                        golesEncontra2 += partidoDos.marcadorEquipo1;
                    }
                }


                elem.golesAFavor = golesAfavorlocal + golesAfavorvisitante;
                elem.golesEnContra = golesEncontra1 + golesEncontra2;


                elem.diferenciaDeGoles = elem.golesAFavor - elem.golesEnContra;
                var puntos = elem.juegosGanados * 3 + elem.juegosEmpatados * 1 + elem.ptsExtrasOAmosnetacion;

                elem.puntos = puntos;
                
                equipol.save(elem.id);
                tabla.Add(elem);

                golesAfavorlocal = 0;
                golesAfavorvisitante = 0;
                golesEncontra1 = 0;
                golesEncontra2 = 0;
            }
            var tablageneral = tabla.OrderByDescending(x => x.puntos).ThenByDescending(x => x.juegosJugados).ThenByDescending(x => x.diferenciaDeGoles);

            foreach (Equipo elem in tablageneral)
            {
                numero++;
                elem.numero = numero;
                //equipol.save(elem.id);

            }


            return result;
        }

        public double DiferenciaTiempo( DateTime fecha1, DateTime fecha2)
        {
            TimeSpan result = fecha2.Subtract(fecha1);

             var segundos = Convert.ToDouble(result.TotalSeconds);
             

            return segundos;
        }

        public List<PartidosJornadas> getpartidosactualdeliguilla( DateTime diaJornada)
        {
            var diamas = diaJornada.AddDays(1);
            var diamenos = diaJornada.AddDays(-1);

            List<PartidosJornadas> partidos = _session.Query<PartidosJornadas>()
                    .Where(x => 
                    x.fechaHoraPartido.Date == diaJornada.Date ||
                    x.fechaHoraPartido.Date == diamas.Date ||
                    x.fechaHoraPartido.Date == diamenos.Date 
                    ).ToList();

            return partidos;
        }
        public List<PartidosJornadas> getPartidosDeLaJornadaPorDia(int idJornada, DateTime diaJornada, string periodo)
        {
            JornadasRepository jornadal = new JornadasRepository();
            var actual = jornadal.horaActual();
            List <PartidosJornadas>  partidos    = _session.Query<PartidosJornadas>()
                    .Where(x => x.fechaHoraPartido.Date == diaJornada.Date
                                && x.idJornada.id == idJornada).ToList();
            
            return partidos;
        }
        public List<DateTime> getDiasPartidoPorJornada(Jornadas jornada)
        {
            var projections = Projections.Distinct(Projections.ProjectionList()
                .Add(Projections.Property("fechaHoraPartido").As("fechaHoraPartido")));
            var diasJornada = _session.QueryOver<PartidosJornadas>()
                .Where(x => x.idJornada.id == jornada.id)
                .Select(projections)
                .List<DateTime>().ToList();

            return diasJornada;
        }
    }
}
