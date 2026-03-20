using dosxl.Models.Repository;
using dosxl.Models.Response;
using dosxl.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System;
using Microsoft.AspNetCore.Authorization;
using System.Linq;
using NHibernate.Criterion;

namespace dosxl.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TorneoController : BaseController
    {

        [HttpPost]
        [Route("GenerarTorneo")]
        public IActionResult save(Torneo torneo)
        {
            try
            {
                JugadorRepository ljugador = new JugadorRepository();
                TorneoRepository ltorneo = new TorneoRepository();


                ltorneo.save(torneo);
                torneo = ltorneo.ultimoid();
               
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = torneo

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
        [Route("ObtenerTorneos")]
        public IActionResult getorneos()
        {
            try
            {
                TorneoRepository ltorneo = new TorneoRepository();
                List<Torneo> torneo = ltorneo.getAll();
                
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = torneo

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
        [Route("ObtenerTorneo")]
        public IActionResult getorneo()
        {
            try
            {
                TorneoRepository ltorneo = new TorneoRepository();
                Torneo torneo = new Torneo();

                torneo = ltorneo.ultimoid();


                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = torneo

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
        [Route("GruposYEquiposPortorneo")]
        public IActionResult getgruposEquipos(int? torneoID)
        {
            try
            {
                TorneoRepository ltorneo = new TorneoRepository();
                GrupoRepository lgrupo = new GrupoRepository();
                List<Grupo> grupo = new List<Grupo>();

                if (torneoID != null)
                {
                    grupo = ltorneo.getPorToneo(torneoID.Value);
                }
                else 
                {
                    grupo = lgrupo.getAll();
                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = grupo

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
