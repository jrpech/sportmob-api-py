using dosxl.Models.Repository;
using dosxl.Models.Response;
using dosxl.Models;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using NHibernate.Mapping;
using NHibernate.Transform;
using Microsoft.AspNetCore.Authorization;

namespace dosxl.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class JugadorController : BaseController
    {
        [HttpPost]
        [Route("GenerarJugador")]
        public IActionResult save( Jugador jugador)
        {
            try
            {
                JugadorRepository ljugador = new JugadorRepository();
                JornadasRepository jornadas = new JornadasRepository();
                DateTime tiempo = jornadas.horaActual();
                jugador.fechaRegistro = tiempo;
                    ljugador.save(jugador);
                    if (jugador.id == 0)
                        jugador = ljugador.ultimoid();
                    else
                        jugador = ljugador.getById(jugador.id);


                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = jugador

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
        [Route("JugadoresPorEquipo")]
        public IActionResult getJugador(int? equipoID)
        {
            try
            {
                JugadorRepository ljugador = new JugadorRepository();
                List<Jugador> jugadores = new List<Jugador>();


                if (equipoID != null)
                {
                    jugadores = ljugador.getPorjugador(equipoID.Value);
                }
                else
                {
                    jugadores = ljugador.getAll();
                }
                    

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = jugadores

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
        [HttpDelete]
        [Route("EliminarJugador")]
        public IActionResult Eliminar(int id)
        {
            try
            {
                JugadorRepository ljugador = new JugadorRepository();
                ljugador.elminar(id);

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",


                }); ;
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
