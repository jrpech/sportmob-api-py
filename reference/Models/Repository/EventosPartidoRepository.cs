using dosxl.Models.Models;
using dosxl.Utils;
using FluentNHibernate.Conventions;
using FluentNHibernate.Conventions.Inspections;
using NHibernate.Criterion;
using System;
using System.Collections.Generic;
using System.Linq;

namespace dosxl.Models.Repository
{
    public class EventosPartidoRepository : RepositoryBase<EventosPartido>
    {
        public List<EventosPartido> getAll()
        {
            return _session.Query<EventosPartido>().ToList();
        }
        public EventosPartido getById(int id)
        {
            return _session.Query<EventosPartido>().Where(x =>
                      x.id == id).FirstOrDefault();
        }
        public List<EventosPartido> ListarEventoPorPartido(int partidoID)
        {
            return _session.Query<EventosPartido>().Where(
                   x => x.idPartido.id == partidoID).ToList();
        }
        public EventosPartido ultimoid()
        {
            var lastID = _session.CreateCriteria(typeof(EventosPartido))
                .SetProjection(Projections.Max("id")).UniqueResult();
            int idevento = int.Parse(lastID.ToString());

            return _session.Query<EventosPartido>().Where(x => x.id == idevento).FirstOrDefault();
        }
        public List<EventosPartido> listaGolesPorEquipo(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "GOL"
                              && x.idEquipo.id == idequipo).ToList();
        }
        public List<EventosPartido> listatargetaRojaPorEquipo(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "ROJA"
                              && x.idEquipo.id == idequipo).ToList();
        }
        public List<EventosPartido> listatargetaAmarrllaPorEquipo(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "AMARILLA"
                              && x.idEquipo.id == idequipo).ToList();
        }

        public EventosPartido ultimoGolPorEquipo(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "GOL"
                              && x.idEquipo.id == idequipo)
                              .OrderByDescending(x => x.id)
                              .FirstOrDefault();
        }
        public EventosPartido TargetaRojaPorEquipo(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "ROJA"
                              && x.idEquipo.id == idequipo)
                              .OrderByDescending(x => x.id)
                              .FirstOrDefault();
        }
        public EventosPartido TargetaAmarillaPorEquipo(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "AMARILLA"
                              && x.idEquipo.id == idequipo)
                              .OrderByDescending(x => x.id)
                              .FirstOrDefault();
        }
        public EventosPartido faltaPorEquipo(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "FALTA"
                              && x.idEquipo.id == idequipo)
                              .OrderByDescending(x => x.id)
                              .FirstOrDefault();
        }
        public List<EventosPartido> listafaltaPorEquipo(int idpartido, int idequipo, string estadoPartidoEvento)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "FALTA"
                              && x.idEquipo.id == idequipo
                              && x.estadoPartido == estadoPartidoEvento).ToList();
        }
        public List<EventosPartido> penalesAnotados(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "PENAL ANOTADO"
                              && x.idEquipo.id == idequipo).ToList();
        }
        public List<EventosPartido> penalesfallados(int idpartido, int idequipo)
        {
            return _session.Query<EventosPartido>().Where(x => x.idPartido.id == idpartido
                              && x.evento == "PENAL FALLADO"
                              && x.idEquipo.id == idequipo).ToList();
        }
        public bool save(EventosPartido evento)
        {
            bool result = false;
            JornadasRepository jornadal = new JornadasRepository();
            var actual = jornadal.horaActual();

            var lastID = _session.CreateCriteria(typeof(EventosPartido))
                .SetProjection(Projections.Max("id")).UniqueResult();

            if (evento.id == 0)
            {

                if (lastID == null)
                    evento.id = 1;
                else
                    evento.id = int.Parse(lastID.ToString()) + 1;

                if(string.IsNullOrEmpty(evento.minuto))
                    evento.minuto = actual.ToString("hh:mm:ss");

                _session.Save(evento);
                _session.Flush();
            }
            else
            {
                EventosPartido eventoUpdate = getById(evento.id);
                eventoUpdate.evento = evento.evento;
                eventoUpdate.fechaHora = evento.fechaHora;
                eventoUpdate.minuto = evento.minuto;

                _session.Update(eventoUpdate);
                _session.Flush();
                result = true;

            }

            return result;
        }
        public bool saveEventoParaestadosdepartdo(EventosPartido evento)
        {
            bool result = false;
            JornadasRepository jornadal = new JornadasRepository();

            var actual = jornadal.horaActual();

            var lastID = _session.CreateCriteria(typeof(EventosPartido))
                .SetProjection(Projections.Max("id")).UniqueResult();

            if (evento.id == 0)
            {

                if (lastID == null)
                    evento.id = 1;
                else
                    evento.id = int.Parse(lastID.ToString()) + 1;


                evento.fechaHora = actual;
                evento.idEquipo = null;
                evento.idjugador = null;
                evento.minuto = actual.ToString("hh:mm:ss");
                _session.Save(evento);
                _session.Flush();
            }

            return result;
        }
        public bool saveEventoPenales(EventosPartido evento)
        {
            bool result = false;
            JornadasRepository jornadal = new JornadasRepository();

            var actual = jornadal.horaActual();

            var lastID = _session.CreateCriteria(typeof(EventosPartido))
                .SetProjection(Projections.Max("id")).UniqueResult();

            if (evento.id == 0)
            {

                if (lastID == null)
                    evento.id = 1;
                else
                    evento.id = int.Parse(lastID.ToString()) + 1;


                evento.fechaHora = actual;
                evento.idEquipo = null;
                evento.idjugador = null;
                evento.minuto = actual.ToString("hh:mm:ss");
                _session.Merge(evento);
                _session.Flush();
            }

            return result;
        }

        public bool elminarEvento(int id)
        {
            bool result = false;

            EventosPartido evento = getById(id);

            _session.Delete(evento);
            _session.Flush();

            return result;
        }

        public string minutodelevento(string minuto)
        {
            string str = minuto;
            string separator = ":";
            var tokens = str.Split(separator);
            var lis = tokens[1];

            if (lis == "00")
                lis = "1";
            else
                lis = lis.TrimStart(new Char[] { '0' });

            return lis;

        }
        public string  descripcionDelEvento(EventosPartido evento)
        {
            
            string str = evento.minuto;
            string separator = ":";
            var descripcionevento = "";
            var tokens = str.Split(separator);
            var lis = tokens[1];
            var eventotiempo = evento.fechaHora.ToString("HH:mm");

            if (lis == "00") 
                lis = "1";
            else
            lis = lis.TrimStart(new Char[] { '0' });

            if (evento.idjugador == null || evento.idjugador.id == 0)
                evento.idjugador = null;
                

            switch (evento.evento)
                {
                case "INICIADO":
                    descripcionevento = eventotiempo +"  PARTIDO" + " " + evento.evento;
                    break;
                case "PRIMER TIEMPO":
                    descripcionevento = eventotiempo + " " + evento.evento;

                    break;
                case "SEGUNDO TIEMPO":
                    descripcionevento = eventotiempo + " " + evento.evento;

                    break;
                case "FINALIZADO":
                    descripcionevento = eventotiempo +" FIN DEL PARTIDO";

                    break;
                case "GOL":
                    
                   descripcionevento = lis + "´ " + evento.idjugador.nombreJersy + " " + "(" + evento.idPartido.marcadorEquipo1 + "-" + evento.idPartido.marcadorEquipo2 + ")";

                    break;
                
                case "AMARILLA":
                    descripcionevento = lis + "´ " + evento.idjugador.nombreJersy;

                    break;
                case "ROJA":
                   descripcionevento = lis + "´ " + evento.idjugador.nombreJersy;

                    break;
                case "SEGUNDO TIEMPO FINALIZADO":
                    descripcionevento = eventotiempo +  " " + evento.evento;

                    break;

                case "PENALES":
                    descripcionevento = eventotiempo + " " + evento.evento;

                    break;
                case "PENAL ANOTADO":
                    descripcionevento =  evento.evento;

                    break;
                case "PENAL FALLADO":
                    descripcionevento =  evento.evento;

                    break;

            }
            
            return descripcionevento;
        }
        public List<EventosPartido> eventoGol()
        {
            return _session.Query<EventosPartido>().Where(x => x.evento == "GOL" && x.idPartido.tipoPartido == "REGULAR").ToList();
        }
        public List<EventosPartido> golPorjugador(int id)
        {
            return _session.Query<EventosPartido>().Where(x => x.evento == "GOL" && x.idjugador.id == id && x.idPartido.tipoPartido == "REGULAR").ToList();
        }
    }
}
