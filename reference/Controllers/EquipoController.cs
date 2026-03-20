using dosxl.Models.Repository;
using dosxl.Models.Response;
using dosxl.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System;
using FluentNHibernate.Testing.Values;
using dosxl.Models.Request;
using Microsoft.AspNetCore.Authorization;
using System.Linq;

namespace dosxl.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class EquipoController : BaseController
    {

        [HttpPost]
        [Route("registrarPago")]
        public IActionResult registrarPago(PagoRequest pago)
        {
            try
            {
                EquipoRepository equipoRepository = new EquipoRepository();
                equipoRepository.registrarPago(pago);

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "Pago registrado correctamente",

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
        [Route("EquiposPorGrupo")]
        public IActionResult getEquipos(int? grupoID)
        {
            try
            {
                EquipoRepository lequipo = new EquipoRepository();
                JugadorRepository jugadoresControler = new JugadorRepository();
                List<Equipo> equipos = new List<Equipo>();
                List<Equipo> equiposConnumero = new List<Equipo>();

                var numero = 0;

                if (grupoID != null)
                {
                    equipos = lequipo.getPorGrupo(grupoID.Value);
                }
                else 
                {
                    equipos = lequipo.getAll();
                }


                foreach (Equipo equipo in equipos)
                {
                    List<Jugador> jugadores = jugadoresControler.getPorjugador(equipo.id);

                    if(jugadores != null)
                    {
                        equipo.jugadoresRegistrados = jugadores.Count;
                    }
                }

                var tablageneralporGrupo = equipos.OrderByDescending(x => x.puntos).ThenByDescending(x => x.juegosJugados).ThenByDescending(x => x.diferenciaDeGoles);

                foreach (Equipo elem in tablageneralporGrupo)
                {
                    numero++;
                    elem.numero = numero;
                    equiposConnumero.Add(elem);

                }
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = equiposConnumero

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
