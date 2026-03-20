using dosxl.Models.Repository;
using dosxl.Models.Response;
using dosxl.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System;
using dosxl.Models.Models;
using NHibernate.Persister.Entity;
using System.Linq;
using NHibernate;
using dosxl.Models.Request;
using System.Data;
using System.Xml.Linq;
using NHibernate.Linq;
using System.Collections;
using Microsoft.AspNetCore.Authorization;
using Antlr.Runtime.Misc;
using Google.Protobuf.WellKnownTypes;
using System.Runtime.Intrinsics.Arm;
using Ubiety.Dns.Core;
using Microsoft.AspNetCore.Identity;
using NHibernate.Mapping;
using Org.BouncyCastle.Asn1;

namespace dosxl.Controllers
{
    [ApiController]
    [Route("api/liga2xl/[controller]")]
    public class API_APP_Liga2XLController : BaseController
    {
        [HttpPost]
        [Route("Evento/GuardarEvento")]
        public IActionResult save(EventosPartido evento)
        {
            try
            {
                EventosPartidoRepository eventol = new EventosPartidoRepository();
                PartidosRepository partidol = new PartidosRepository();
                JugadorRepository jugadorl = new JugadorRepository();
                NotificacionRepository notificacionl = new NotificacionRepository();

                PartidosJornadas partido1 = new PartidosJornadas();
                PartidosJornadas partido2 = new PartidosJornadas();
                PartidosJornadas partido = new PartidosJornadas();

                partido = partidol.getByIdPartido(evento.idPartido.id);

                if (partido.estadoPartido == "INICIADO")
                    evento.estadoPartido = "INICIADO";
                if (partido.estadoPartido == "SEGUNDO TIEMPO")
                    evento.estadoPartido = "SEGUNDO TIEMPO";

                eventol.save(evento);

                if (evento.idPartido != null && evento.idEquipo != null){ 
                partido1 = partidol.porIDyEquipo1(evento.idPartido.id, evento.idEquipo.id);

                partido2 = partidol.porIDyEquipo2(evento.idPartido.id, evento.idEquipo.id);
                }

                switch (evento.evento)
                {
                    case "GOL":

                        notificacionl.crearNotifcaciondelpartido(evento);
                        if (partido1 != null)
                        {
                            partido1.marcadorEquipo1++;
                            partidol.save(partido1);
                        }
                        if (partido2 != null)
                        {
                            partido2.marcadorEquipo2++;
                            partidol.save(partido2);
                        }

                        var jugador = jugadorl.getById(evento.idjugador.id);

                        evento.descripcion = eventol.minutodelevento(evento.minuto) + "´ " + jugador.nombreJersy + " " + "(" + partido.marcadorEquipo1 + "-" + partido.marcadorEquipo2 + ")";

                        eventol.save(evento);
                        break;

                    case "AMARILLA":
                        notificacionl.crearNotifcaciondelpartido(evento);
                        break;

                    case "ROJA":
                        notificacionl.crearNotifcaciondelpartido(evento);
                        break;

                    case "ANULAR GOL":

                        var ultimoGol = eventol.ultimoGolPorEquipo(evento.idPartido.id, evento.idEquipo.id);

                        if (partido1 != null)
                        {
                            if (partido1.marcadorEquipo1 != 0)
                                partido1.marcadorEquipo1--;
                            partidol.save(partido1);
                        }
                        if (partido2 != null)
                        {
                            if (partido2.marcadorEquipo2 != 0)
                                partido2.marcadorEquipo2--;
                            partidol.save(partido2);
                        }
                        if (ultimoGol != null)
                            eventol.elminarEvento(ultimoGol.id);
                        break;

                    case "ANULAR AMARILLA":

                        var targetaAmarrilla = eventol.TargetaAmarillaPorEquipo(evento.idPartido.id, evento.idEquipo.id);
                        if (targetaAmarrilla != null)
                            eventol.elminarEvento(targetaAmarrilla.id);
                        break;

                    case "ANULAR ROJA":

                        var targetaRoja = eventol.TargetaRojaPorEquipo(evento.idPartido.id, evento.idEquipo.id);
                        if (targetaRoja != null)
                            eventol.elminarEvento(targetaRoja.id);
                        break;

                    case "ANULAR FALTA":

                        var falta = eventol.faltaPorEquipo(evento.idPartido.id, evento.idEquipo.id);
                        if (falta != null)
                            eventol.elminarEvento(falta.id);

                        break;

                }

                 return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = ""

                });

            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpPost]
        [Route("Partido/EstadoDelPartido")]
        public IActionResult editarestado(int? idPartido , string? estatusPartido, bool noActualizar )
        {
            try
            {
                PartidosRepository partidol = new PartidosRepository();
                EventosPartidoRepository eventol = new EventosPartidoRepository();
                JornadasRepository jornadal = new JornadasRepository();
                PartidosJornadas partido = new PartidosJornadas();
                Jornadas jornada = new Jornadas();
                ContadorEvento evento = new ContadorEvento();
                EventosPartido eventos = new EventosPartido();
                NotificacionRepository notificacionl = new NotificacionRepository();

                var actual = jornadal.horaActual();
                var estatusContinuar = estatusPartido;
                 

                if (idPartido != null && estatusPartido !=null) {

                    partido = partidol.getById(idPartido.Value);
                    partido.estadoPartido = estatusPartido;
                    
                    if (estatusPartido == "CONTINUAR INICIADO") 
                    {
                       partido.estadoPartido = "INICIADO" ;
                       estatusContinuar = "INICIADO";
                    }
                    if (estatusPartido == "CONTINUAR SEGUNDO TIEMPO") 
                    {
                        partido.estadoPartido = "SEGUNDO TIEMPO";
                        estatusContinuar = "SEGUNDO TIEMPO";
                    }

                    partidol.save(partido);

                    if (noActualizar == true) {
                    switch (estatusPartido)
                    {
                        case "INICIADO":
                            partido.fechaHoraInicioPartido = actual;
                            partidol.save(partido);
                            eventos.idPartido = partido; 
                            eventos.evento = "INICIADO";
                            eventol.saveEventoParaestadosdepartdo(eventos);
                            notificacionl.crearNotifcaciondelpartido(eventos);

                            break;
                        case "PRIMER TIEMPO":
                            partido.fechaHoraFinPrimerTiempo = actual;
                            partidol.save(partido);
                            eventos.idPartido = partido;
                            eventos.evento = "PRIMER TIEMPO";
                            eventol.saveEventoParaestadosdepartdo(eventos);
                            notificacionl.crearNotifcaciondelpartido(eventos);

                            break;
                        case "SEGUNDO TIEMPO":
                            partido.fechaHoraInicioSegundoTiempo = actual;
                            partidol.save(partido);
                            eventos.idPartido = partido;
                            eventos.evento = "SEGUNDO TIEMPO";
                            eventol.saveEventoParaestadosdepartdo(eventos);
                            notificacionl.crearNotifcaciondelpartido(eventos);

                            break;
                        case "FINALIZADO":
                            partido.fechaHoraFinPartido = actual;
                            partidol.save(partido);
                            eventos.idPartido = partido;
                            eventos.evento = "FINALIZADO";
                            eventol.saveEventoParaestadosdepartdo(eventos);
                            notificacionl.crearNotifcaciondelpartido(eventos);

                            break;
                        case "PAUSA INICIADO":
                            partido.fechaHoraPausa = actual;
                            partidol.save(partido);
                            break;
                        case "PAUSA SEGUNDO TIEMPO":
                           partido.fechaHoraPausa = actual;
                           partidol.save(partido);
                            break;
                       case "CONTINUAR INICIADO":
                            partido.pausaAcumuladaPrimerTiempo = partido.pausaAcumuladaPrimerTiempo + partidol.DiferenciaTiempo(partido.fechaHoraPausa, actual);
                            partidol.save(partido);
                            break;
                       case "CONTINUAR SEGUNDO TIEMPO":
                            partido.pausaAcumuladaSegundoTiempo = partido.pausaAcumuladaSegundoTiempo + partidol.DiferenciaTiempo(partido.fechaHoraPausa, actual);
                            partidol.save(partido);
                            break;
                       case "PENALES":
                            
                            eventos.idPartido = partido;
                            eventos.evento = "SEGUNDO TIEMPO FINALIZADO";
                            eventol.saveEventoPenales(eventos);

                            eventos.id = 0;
                            eventos.evento = "PENALES";
                            eventol.saveEventoPenales(eventos);
                            break;
                        }
                    }
                    
                    var  golesEquipo1 =eventol.listaGolesPorEquipo(partido.id , partido.idEquipo1.id);
                    var  golesEquipo2 = eventol.listaGolesPorEquipo(partido.id, partido.idEquipo2.id);
                    var targetasRojasEquipo1 = eventol.listatargetaRojaPorEquipo(partido.id, partido.idEquipo1.id);
                    var targetasRojasEquipo2 = eventol.listatargetaRojaPorEquipo(partido.id, partido.idEquipo2.id);
                    var targetasAmarillaEquipo1 = eventol.listatargetaAmarrllaPorEquipo(partido.id, partido.idEquipo1.id);
                    var targetasAmarillaEquipo2 = eventol.listatargetaAmarrllaPorEquipo(partido.id, partido.idEquipo2.id);
                    var faltasEquipo1 = eventol.listafaltaPorEquipo(partido.id, partido.idEquipo1.id, estatusContinuar); ;
                    var faltasEquipo2 = eventol.listafaltaPorEquipo(partido.id, partido.idEquipo2.id, estatusContinuar); 

                    if (golesEquipo1 != null)
                        evento.golesEquipo1 = golesEquipo1.Count();
                    if (golesEquipo2 != null)
                        evento.golesEquipo2 = golesEquipo2.Count();

                    if (targetasAmarillaEquipo1 != null)
                        evento.amarillaEquipo1 = targetasAmarillaEquipo1.Count();
                    if (targetasAmarillaEquipo2 != null)
                        evento.amarillaEquipo2 = targetasAmarillaEquipo2.Count();

                    if (targetasRojasEquipo1 != null)
                        evento.rojasEquipo1 = targetasRojasEquipo1.Count();
                    if (targetasRojasEquipo2 != null)
                        evento.rojasEquipo2 = targetasRojasEquipo2.Count();

                    if (faltasEquipo1 != null)
                        evento.faltasEquipo1 = faltasEquipo1.Count();
                    if (faltasEquipo2 != null)
                        evento.faltasEquipo2 = faltasEquipo2.Count();

                    evento.pausaAcumuladaPrimerTiempo = partido.pausaAcumuladaPrimerTiempo;
                    evento.pausaAcumuladaSegundoTiempo = partido.pausaAcumuladaSegundoTiempo;

                    var penalesequipo1 = eventol.penalesAnotados(partido.id, partido.idEquipo1.id);
                    var penalesequipo2 = eventol.penalesAnotados(partido.id, partido.idEquipo2.id);
                    var penalesfalladosequipo1 = eventol.penalesfallados(partido.id, partido.idEquipo1.id);
                    var penalesfalladosequipo2 = eventol.penalesfallados(partido.id, partido.idEquipo2.id);

                    if (!String.IsNullOrEmpty(partido.tipoPartido))
                        evento.modo = partido.tipoPartido;

                    if (!String.IsNullOrEmpty(partido.idaOvuelta))
                        evento.etapa = partido.idaOvuelta;

                        jornada = jornadal.getById(partido.idJornada.id);

                    if (jornada != null) 
                    {
                        evento.estadoJornada = jornada.etapaLiguilla;
                        evento.marcadorGlobalEquipo1 = partidol.marcadorPorequipo(partido.idEquipo1.id, jornada.id);
                        evento.marcadorGlobalEquipo2 = partidol.marcadorPorequipo(partido.idEquipo2.id, jornada.id);
                    }

                    if (penalesequipo1 != null)
                        evento.penalesAnotadosEquipo1 = penalesequipo1.Count();

                    if (penalesequipo2 != null)
                        evento.penalesAnotadosEquipo2 = penalesequipo2.Count();

                    if (penalesfalladosequipo1 != null)
                        evento.penalesFalladosEquipo1 = penalesfalladosequipo1.Count();

                    if (penalesfalladosequipo2 != null)
                        evento.penalesFalladosEquipo2 = penalesfalladosequipo2.Count();


                }
                
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = evento

                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Partido/DetallePartido")]
        public IActionResult detallePartido(int? partidoID)
        {
            try
            {
                PartidosRepository partidosl = new PartidosRepository();
                PartidosJornadas partidos = new PartidosJornadas();

                if (partidoID != null) {

                    partidos = partidosl.getByIdPartido(partidoID.Value);
                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = partidos

                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Evento/EventosPorPartido")]
        public IActionResult eventoPartido(int? partidoID)
        {
            try
            {
                EventosPartidoRepository eventol = new EventosPartidoRepository();
                PartidosRepository partidol = new PartidosRepository();
                List<EventosPartido> evento = new List<EventosPartido>();
                PartidosJornadas partido = new PartidosJornadas();
                List<EventosPartido> eventosinalgunosestado = new List<EventosPartido>();
                List<EventosPartido> eventosconestadosnomoestrados = new List<EventosPartido>();
                PartidosJornadas partido1 = new PartidosJornadas();
                PartidosJornadas partido2 = new PartidosJornadas();
                var marcador1 = 0;
                var marcador2 = 0;

                if (partidoID != null)
                {
                    partido = partidol.getById(partidoID.Value);
                    evento = eventol.ListarEventoPorPartido(partidoID.Value);

                    foreach (EventosPartido elem in evento) {

                        if ((elem.evento == "ANULAR GOL") || (elem.evento == "ANULAR AMARRILLA") || (elem.evento == "ANULAR ROJA") || (elem.evento == "ANULAR FALTA") || (elem.evento == "FALTA"))
                        {
                            eventosconestadosnomoestrados.Add(elem);
                        }
                        else { 
                              if (partido.estadoPartido == "FINALIZADO")
                               {
                                    if (elem.evento =="GOL") 
                                    {
                                        if (elem.idPartido != null && elem.idEquipo != null)
                                        {
                                           partido1 = partidol.porIDyEquipo1(elem.idPartido.id, elem.idEquipo.id);
                                            
                                           partido2 = partidol.porIDyEquipo2(elem.idPartido.id, elem.idEquipo.id);
                                         }
                                           if (partido1 != null) 
                                                   marcador1 ++;
                                           if (partido2 != null)
                                                    marcador2++;
                                       
                                       elem.descripcion = eventol.minutodelevento(elem.minuto) +"´ " + elem.idjugador.nombreJersy + " " + "(" + marcador1 + "-" + marcador2+ ")";
                                       
                                    }
                                     else 
                                       elem.descripcion = eventol.descripcionDelEvento(elem);
                              }
                               else   
                               { 
                                 if (elem.evento != "GOL")
                                 elem.descripcion = eventol.descripcionDelEvento(elem);
                                
                                eventol.save(elem);

                               }
                            eventosinalgunosestado.Add(elem);
                        }   
                    }
                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = eventosinalgunosestado

                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpPost]
        [Route("Jornada/EditarJornada")]
        public IActionResult editar(Jornadas jornada)
        {
            try
            {
                JornadasRepository jornadal = new JornadasRepository();

                jornadal.save(jornada);

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = ""

                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Jornada/ListarPartidosPorJornada")]
        public IActionResult listarjornada( string? periodo)
        {
            try
            {
                PartidosRepository partidosl = new PartidosRepository();
                JornadasRepository jornadal = new JornadasRepository();
                List<Jornadas> jornadaActual = jornadal.actual();

                List<Dias> dias = new List<Dias>();
                List<JornadaVista> jornadasVista = new List<JornadaVista>();
                List<PartidosJornadas> partidos = new List<PartidosJornadas>();
                List<Jornadas> jornadaPasadoproximo = new List<Jornadas>();
                IOrderedEnumerable<JornadaVista> ordenada;

                if (periodo == "PASADO")
                       jornadaPasadoproximo = jornadal.pasado(jornadaActual);
                    if (periodo == "PROXIMO")
                        jornadaPasadoproximo = jornadal.proximos(jornadaActual);
                    if (periodo == "ACTUAL")
                         jornadaPasadoproximo = jornadal.actual();

                foreach (Jornadas elem in jornadaPasadoproximo)
                        {
                        List<DateTime> diasJornada = partidosl.getDiasPartidoPorJornada(elem);
                        JornadaVista vistaJornada = new JornadaVista()
                            {
                                id = elem.id,
                                nombre = elem.nombre,
                                fechaInicio = elem.fechaInicio,
                                fechaFin = elem.fechaFin
                                
                            };
                            List<DateTime> fechas = partidosl.getDiasPartidoPorJornada(elem);
                            foreach (DateTime fecha in fechas)
                            {
                                Dias partidosPorDia = new Dias();
                                partidosPorDia.fechaNombre = fecha.ToString("dd/MM/yyyy");
                                partidosPorDia.fecha = fecha.Date;
                                
                                partidosPorDia.partidos = partidosl.getPartidosDeLaJornadaPorDia(elem.id, fecha, periodo);
                                 if (periodo != "ACTUAL")
                                 vistaJornada.dias.Add(partidosPorDia);
                                 else
                                 dias.Add(partidosPorDia);
                            }
                                if (periodo == "ACTUAL") 
                                {
                                 
                                 var partidosfinalizados = dias[0].partidos.Where(x=> x.estadoPartido =="POR JUGAR");
                                 
                                       if ( partidosfinalizados.Count() == 0)         
                                        {
                                         IEnumerable los = dias.OrderByDescending(x => x.fecha);

                                            foreach (Dias ele in los)
                                            vistaJornada.dias.Add(ele);
                                        }
                                         else
                                         {
                                           foreach (Dias ele in dias)
                                             vistaJornada.dias.Add(ele);
                                         }
                                  jornadasVista.Add(vistaJornada);
                                   
                                }
                              else 
                               jornadasVista.Add(vistaJornada);
                         
                        }

                      if (periodo != "PASADO")
                          ordenada = jornadasVista.OrderBy(x => x.fechaFin);
                       else
                          ordenada = jornadasVista.OrderByDescending(x => x.fechaFin);
                     
                
                      
                    return Ok(new BaseResponse
                    {
                        respuesta = "OK",
                        mensaje = "",
                        data = ordenada

                    });
                

            }
            
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Jornada/ListarPartidosPorEquipo")]
        public IActionResult listarpatidosporequipo(int? equipoID, string? periodo)
        {
            try
            {
                PartidosRepository partidol = new PartidosRepository();
                List<PartidosJornadas> partidos = new List<PartidosJornadas>();
         

                if (equipoID != null && periodo != null)
                {
                    if (periodo == "PASADO")
                        partidos = partidol.partidosConEstadoFinalizadoPartidosPorEquipo(equipoID.Value);
                    else
                        partidos = partidol.partidosConEstadoPorJugar(equipoID.Value);

                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = partidos

                });


            }

            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Jornada/ListarJornadas")]
            public IActionResult listarjornadas()
            {
                try
                {
                    JornadasRepository jornadal = new JornadasRepository();
                    List<Jornadas> jornada = jornadal.getAll();

                    return Ok(new BaseResponse
                    {
                        respuesta = "OK",
                        mensaje = "",
                        data = jornada

                    });
                }
                catch (Exception ex)
                {
                    return Ok(new BaseResponse
                    {
                        respuesta = "ERROR",
                        mensaje = ex.Message
                    });
                }
            }

        [HttpGet]
        [AllowAnonymous]
        [Route("Equipo/TablaGeneral")]
        public IActionResult tablageneral()
        {
            try
            {
                EquipoRepository equipol = new EquipoRepository();
                PartidosRepository partidosl = new PartidosRepository();
                List<Equipo> equipos = equipol.getAll();
                List<Equipo> tabla = new List<Equipo>();

                var numero = 0;
                
                partidosl.guardarDatosTablaGeneral();

                foreach (Equipo elem in equipos)
                    tabla.Add(elem);

                var tablageneral = tabla.OrderByDescending(x => x.puntos).ThenByDescending(x => x.juegosJugados).ThenByDescending(x=> x.diferenciaDeGoles);

                foreach (Equipo elem in tablageneral) 
                {
                    numero++;
                    elem.numero = numero;
                    
                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = tablageneral

                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Equipo/TablaGeneralPorGrupos")]
        public IActionResult tablageneralPorgrupo()
        {
            try
            {
                PartidosRepository partidosl = new PartidosRepository();
                GrupoRepository lgrupo = new GrupoRepository();
                EquipoRepository equipol = new EquipoRepository();

                List<Grupo> grupo = new List<Grupo>();
                List<Grupo> grupoconequiposnumerados = new List<Grupo>();
                List<Equipo> equipostotales = new List<Equipo>();
               

                partidosl.guardarDatosTablaGeneral();
                grupo = lgrupo.getAll();

                foreach (Grupo ele in grupo){
                    List<Equipo> equiposordenados = new List<Equipo>();
                    var numero = 0;

                    Grupo prueba = new Grupo() {
                          id = ele.id,
                          nombre = ele.nombre,
                          noEquipos = ele.noEquipos,
                          torneoID = ele.torneoID
                     };
                   

                    equipostotales = equipol.getPorGrupo(ele.id);
                 
                    var tablageneral = equipostotales.OrderByDescending(x => x.puntos).ThenByDescending(x=>x.diferenciaDeGoles);
                    
                    foreach (Equipo elems in tablageneral)
                    {
                        numero++;
                        elems.numero = numero;
                        equipol.save(elems.id);
                        equiposordenados.Add(elems);
                    }

                    
                    prueba.equipos = equiposordenados;
                    grupoconequiposnumerados.Add(prueba);

                }
             
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = grupoconequiposnumerados

                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Equipo/DetalleEquipo")]
        public IActionResult detalle( int? id )
        {
            try
            {
                EquipoRepository equipol = new EquipoRepository();
                JugadorRepository jugadorl = new JugadorRepository();
                GrupoRepository grupol = new GrupoRepository();

                Equipo equipo = new Equipo();
                Jugador capitan = new Jugador();
                Grupo grupo = new Grupo();

                if (id != null) {
                      capitan = jugadorl.getbyCapitanEquipo(id.Value);
                      equipo = equipol.getEquipoPorId(id.Value);
                      grupo = grupol.getById(equipo.idGrupo);

                    if (capitan != null) 
                        equipo.capitan = capitan;
                    if (grupo != null)
                        equipo.grupo = grupo.nombre;

                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = equipo

                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("Jugador/ListaGoleadores")]
        public IActionResult goleadorl()
        {
            try
            {
                EventosPartidoRepository eventol = new EventosPartidoRepository();
                List<EventosPartido> evento = eventol.eventoGol();
                
                List<Goleadores> goleadores = new List<Goleadores>();
                Goleadores goleador = new Goleadores();

                foreach (EventosPartido elem in evento)
                {
                    var totaldegoles = eventol.golPorjugador(elem.idjugador.id);

                    goleador = new Goleadores()
                    {
                        id = elem.idjugador.id,
                        nombre = elem.idjugador.nombre,
                        foto = elem.idjugador.foto,
                        equipo = elem.idEquipo.nombreEquipo,
                        goles = totaldegoles.Count()
                    };

                    goleadores.Add(goleador);
                }
               
                var lista =  goleadores.DistinctBy(i => i.id);
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = lista.OrderByDescending(x=> x.goles)
                }); 
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.ToString()
                });
            }
        }
        
        [HttpGet]
        [AllowAnonymous]
        [Route("Jugador/DetalleGoleador")]
        public IActionResult detallegoleador(int? id)
        {
            try
            {
                JugadorRepository jugadorl = new JugadorRepository();
                EquipoRepository equipol = new EquipoRepository();
                JornadasRepository jornadasl = new JornadasRepository();
                EventosPartidoRepository eventol = new EventosPartidoRepository();


                Equipo equipo = new Equipo();
                Jugador jugador = new Jugador();
                List<EventosPartido> totalgoles = new List<EventosPartido>();
                var fechaactual = jornadasl.horaActual();
                int goles = 0;



                if (id != null) {
                    totalgoles = eventol.golPorjugador(id.Value);
                    jugador = jugadorl.getById(id.Value);
                    equipo = equipol.getEquipoPorId(jugador.equipoID);
                }
                if (totalgoles != null) 
                    goles = totalgoles.Count();

                var detallegoleador = new DetalleGoleador().response(jugador, equipo.nombreEquipo, equipo.fotoEquipo,goles );
                
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = detallegoleador
                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }


        [HttpGet]
        [AllowAnonymous]
        [Route("Alineacion/AlineacionPorPartido")]
        public IActionResult alineacion(int? partidoID)
        {
            try
            {
                JugadorRepository jugadorl = new JugadorRepository();
                PartidosRepository partidol = new PartidosRepository();

                List<Jugador> jugadoresEquipo1 = new List<Jugador>();
                List<Jugador> jugadoresEquipo2 = new List<Jugador>();
                PartidosJornadas partido = new PartidosJornadas();
              
                if (partidoID != null) { 
                partido = partidol.getById(partidoID.Value);
              
                if (partido.idEquipo1 != null)
                    jugadoresEquipo1 = jugadorl.getPorjugador(partido.idEquipo1.id);
                if (partido.idEquipo2 != null)
                    jugadoresEquipo2 = jugadorl.getPorjugador(partido.idEquipo2.id);

                    jugadoresEquipo1.AddRange(jugadoresEquipo2);
                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = jugadoresEquipo1
                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }
        
        [HttpGet]
        [AllowAnonymous]
        [Route("Equipo/ListarConfiguracionEquipoVavorito")]
        public IActionResult Configuracionequipofavorito(string token)
        {
            try
            {
                TokenDispositivoRepository rToken = new TokenDispositivoRepository();
                EquipoTokenDispositivo datosConfiguracion = new EquipoTokenDispositivo();

                datosConfiguracion = rToken.getPortokenEquipofavorito(token);

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = datosConfiguracion
                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpPost]
        [AllowAnonymous]
        [Route("Equipo/GuardarTokenPorEquipoFavorito")]
        public IActionResult equipofavorito(EquipoFavoritoRequest datosEquipo)
        {
            try
            {
                TokenDispositivoRepository rToken = new TokenDispositivoRepository();

                rToken.saveTokenequipofavorito(datosEquipo);

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = ""
                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpPost]
        [AllowAnonymous]
        [Route("Equipo/ConfigurarNotificacionesEquipoVavorito")]
        public IActionResult configurarequipofavorito(EquipoTokenDispositivo datosusuariotoken)
        {
            try
            {
                TokenDispositivoRepository rToken = new TokenDispositivoRepository();

                rToken.ConfigurarNotificacionTokenequipofavorito(datosusuariotoken);

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = ""
                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        
        [HttpGet]
        [AllowAnonymous]
        [Route("liguilla/listarPartidosLiguilla")]
        public IActionResult listarliguillaA(string liguillaNombre)
        {
            try
            {
                PartidosRepository partidol = new PartidosRepository();
                JornadasRepository jonadal = new JornadasRepository();
                List<Jornadas> jornadas = new List<Jornadas>();
             
                liguilla liguilla = new liguilla();
                List<PartidosJornadas> partidos = new List<PartidosJornadas>();
                Partido partido = new Partido();

                //octavos
                jornadas = jonadal.getAllJornadasPorNombreYetapa(liguillaNombre, "OCTAVOS");
                
                foreach (Jornadas elem in jornadas)
                {
                    if (elem.llaveLiguilla ==  1) 
                    {
                        partidos = partidol.partidosPorLiguilla( elem.id);
                        partido = partidol.crearPartidoLiguilla(partidos,elem.siguienteJornada);
                        liguilla.octavos.llave1.Add(partido);
                    }
                    if (elem.llaveLiguilla == 2)
                    {
                        partidos = partidol.partidosPorLiguilla( elem.id);
                        partido = partidol.crearPartidoLiguilla(partidos, elem.siguienteJornada);
                        liguilla.octavos.llave2.Add(partido);
                    }
             
                }

                //cuartos
                jornadas = jonadal.getAllJornadasPorNombreYetapa(liguillaNombre, "CUARTOS");

                foreach (Jornadas elem in jornadas)
                {
                    if (elem.llaveLiguilla == 1)
                    {
                        partidos = partidol.partidosPorLiguilla(elem.id);
                        partido = partidol.crearPartidoLiguilla(partidos, elem.siguienteJornada);
                        liguilla.cuartos.llave1.Add(partido);
                    }
                    if (elem.llaveLiguilla == 2)
                    {
                        partidos = partidol.partidosPorLiguilla(elem.id);
                        partido = partidol.crearPartidoLiguilla(partidos, elem.siguienteJornada);
                        liguilla.cuartos.llave2.Add(partido);
                    }

                }

                //semi
                jornadas = jonadal.getAllJornadasPorNombreYetapa(liguillaNombre, "SEMIFINAL");

                    foreach (Jornadas elem in jornadas)
                    {
                        if (elem.llaveLiguilla == 1)
                        {
                            partidos = partidol.partidosPorLiguilla(elem.id);
                            partido = partidol.crearPartidoLiguilla(partidos, elem.siguienteJornada);
                            liguilla.semifinal.llave1 = partido;
                        }
                        if (elem.llaveLiguilla == 2)
                        {
                            partidos = partidol.partidosPorLiguilla(elem.id);
                            partido = partidol.crearPartidoLiguilla(partidos, elem.siguienteJornada);
                            liguilla.semifinal.llave2 = partido;
                        }

                    }
                
                //final
                jornadas = jonadal.getAllJornadasPorNombreYetapa(liguillaNombre, "FINAL");

                foreach (Jornadas elem in jornadas)
                {
                    
                  partidos = partidol.partidosPorLiguilla(elem.id);
                  partido = partidol.crearPartidoLiguilla(partidos, elem.siguienteJornada);
                  liguilla.final = partido;
                 
                }

                //tercer lugar
                jornadas = jonadal.getAllJornadasPorNombreYetapa(liguillaNombre, "TERCERLUGAR");

                foreach (Jornadas elem in jornadas)
                {

                    partidos = partidol.partidosPorLiguilla(elem.id);
                    partido = partidol.crearPartidoLiguilla(partidos, elem.siguienteJornada);
                    liguilla.tercerLugar = partido;

                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = liguilla
                });
            }
            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }

        [HttpGet]
        [AllowAnonymous]
        [Route("liguilla/ListarPartidosPorJornadaLiguilla")]
        public IActionResult partidosporjornadaliguilla()
        {
            try
            {
                PartidosRepository partidosl = new PartidosRepository();
                JornadasRepository jornadal = new JornadasRepository();
                Jornadas jornadaActual = new Jornadas();
                jornadaActual = jornadal.jornadaactualliguilla();

                List<Dias> dias = new List<Dias>();
                List<JornadaVista> jornadasVista = new List<JornadaVista>();
                List<PartidosJornadas> partidos = new List<PartidosJornadas>();
                var fechaaltual = jornadal.horaActual();

                if (jornadaActual != null) { 
                    JornadaVista vistaJornada = new JornadaVista()
                    {
                        id = jornadaActual.id,
                        nombre = jornadaActual.etapaLiguilla,
                        fechaInicio = jornadaActual.fechaInicio,
                        fechaFin = jornadaActual.fechaFin

                    };

                    List<DateTime> fechas = new List<DateTime>();
                     fechas.Add(fechaaltual);

                    foreach (DateTime fecha in fechas)
                    {
                        Dias partidosPorDia = new Dias();
                        partidosPorDia.fechaNombre = fecha.ToString("dd/MM/yyyy");
                        partidosPorDia.fecha = fecha.Date;

                        partidosPorDia.partidos = partidosl.getpartidosactualdeliguilla(fecha);
                        
                        vistaJornada.dias.Add(partidosPorDia);

                    }
                    
                    jornadasVista.Add(vistaJornada);

                }

                return Ok(new BaseResponse
                    {
                        respuesta = "OK",
                        mensaje = "",
                        data = jornadasVista

                    });


                
            }

            catch (Exception ex)
            {
                return Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = ex.Message
                });
            }
        }
    }
}
