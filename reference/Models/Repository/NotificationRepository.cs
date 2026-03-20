using System;
using System.Collections.Generic;
using System.Linq;
using dosxl.Models.Models;
using dosxl.Utils;

namespace dosxl.Models.Repository
{
    public class NotificacionRepository : RepositoryBase<Notificacion>
    {
        public Notificacion getById(int id)
        {
            return _session.Query<Notificacion>().Where(x => x.id == id).FirstOrDefault();
        }

        public List<Notificacion> getAll(int Usuario)
        {
           
            return _session.Query<Notificacion>().Where(x => x.usuario == Usuario).ToList();

        }

        public List<Notificacion> getAllcondominos(int Usuario)
        {

            return _session.Query<Notificacion>().Where(x => x.usuario == Usuario).ToList();

        }

        public bool save(Notificacion notificacion)
        {
            bool result = false;

            if (notificacion.id == 0)
            {
                _session.Save(notificacion);
                _session.Flush();
            }
            else
            {
                Notificacion notificationSaved = getById(notificacion.id);
                notificationSaved.descripcion = notificacion.descripcion;
                _session.Save(notificationSaved);
                _session.Flush();
                result = true;
            }

            return result;
        }

        public void actualizaleido(bool leido, int usuarioid)
        {
            Notificacion leer = _session.Query<Notificacion>().Where(x => x.leido == leido && x.usuario== usuarioid).FirstOrDefault();
            leer.leido = true;
            _session.SaveOrUpdate(leer);
            _session.Flush();
        }


        public void crearNotifcaciondelpartido(EventosPartido evento)
        {
            NotificacionRepository rNotificacion = new NotificacionRepository();
            JornadasRepository jornadal = new JornadasRepository();
            PartidosRepository partidol = new PartidosRepository();
            TokenDispositivoRepository rTokens = new TokenDispositivoRepository();
            JugadorRepository jugadorl = new JugadorRepository();
            EquipoRepository equipol = new EquipoRepository();

            List<EquipoTokenDispositivo> tokens = new List<EquipoTokenDispositivo>();
            PartidosJornadas partido = new PartidosJornadas();
            Notificacion oNotificacion = new Notificacion();
            Jugador jugador = new Jugador();
            Equipo equipo = new Equipo();

            var actual = jornadal.horaActual();
            var tokensall = rTokens.getAlltokens();

            partido = partidol.getByIdPartido(evento.idPartido.id);

            if (evento.evento == "GOL" || evento.evento == "AMARILLA" || evento.evento == "ROJA") { 
               jugador = jugadorl.getById(evento.idjugador.id);
               equipo = equipol.getEquipoPorId(evento.idEquipo.id);
            }

            oNotificacion.fechaNotificacion = actual;
            switch (evento.evento)
            {
                case "INICIADO":
                    tokens = tokensall.Where(x=>( x.equipoID == partido.idEquipo1.id || x.equipoID == partido.idEquipo2.id) & x.partidoIniciado == true).ToList();
                  
                    oNotificacion.titulo = "Partido Iniciado";
                    oNotificacion.descripcion = "El partido de: " + partido.idEquipo1.nombreEquipo +" vs " + partido.idEquipo2.nombreEquipo +" ha iniciado";
                    break;

                case "PRIMER TIEMPO":
                    tokens = tokensall.Where(x => (x.equipoID == partido.idEquipo1.id || x.equipoID == partido.idEquipo2.id) & x.finPrimerTiempo == true).ToList();

                    oNotificacion.titulo = "Fin del  Primer Tiempo";
                    oNotificacion.descripcion = "Fin del primer tiempo del partido: " + partido.idEquipo1.nombreEquipo + " vs " + partido.idEquipo2.nombreEquipo;
                    break;

                case "SEGUNDO TIEMPO":
                    tokens = tokensall.Where(x => (x.equipoID == partido.idEquipo1.id || x.equipoID == partido.idEquipo2.id) & x.inicioSegundoTiempo == true).ToList();

                    oNotificacion.titulo = "Segundo Tiempo";
                    oNotificacion.descripcion = "Inicio del segundo tiempo del partido de: " + partido.idEquipo1.nombreEquipo + " vs " + partido.idEquipo2.nombreEquipo;
                    break;

                case "FINALIZADO":
                    tokens = tokensall.Where(x => (x.equipoID == partido.idEquipo1.id || x.equipoID == partido.idEquipo2.id) & x.finPartido == true).ToList();

                    oNotificacion.titulo = "Fin del Partido ";
                    oNotificacion.descripcion = "El partido de: " + partido.idEquipo1.nombreEquipo + " vs " + partido.idEquipo2.nombreEquipo +" ha concluido";
                    break;

                case "GOL":
                    tokens = tokensall.Where(x => (x.equipoID == partido.idEquipo1.id || x.equipoID == partido.idEquipo2.id) & x.gol == true).ToList();

                    oNotificacion.titulo = "GOL!!!";
                    oNotificacion.descripcion = "Gol de: "+ jugador.nombreJersy + " del equipo "+ equipo.nombreEquipo;
                    break;

                case "AMARILLA":
                    tokens = tokensall.Where(x => (x.equipoID == partido.idEquipo1.id || x.equipoID == partido.idEquipo2.id) & x.tarjetaAmarrilla == true).ToList();

                    oNotificacion.titulo = "Tarjeta Amarrilla";
                    oNotificacion.descripcion = "Amarrilla para : " + jugador.nombreJersy+ " del equipo " + equipo.nombreEquipo;
                    break;

                case "ROJA":
                    tokens = tokensall.Where(x => (x.equipoID == partido.idEquipo1.id || x.equipoID == partido.idEquipo2.id) & x.tarjetaRoja == true).ToList();

                    oNotificacion.titulo = "Tarjeta Roja";
                    oNotificacion.descripcion = "Jugador expulsado: " + jugador.nombreJersy + " del equipo " + equipo.nombreEquipo;
                    break;


            }
            
            rNotificacion.save(oNotificacion);

            try
            {
               if(tokens.Count > 0)
               Utils.Utils.sendPushNotification(oNotificacion, tokens);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}