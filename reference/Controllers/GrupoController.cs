using dosxl.Models.Repository;
using dosxl.Models.Response;
using dosxl.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System;
using Microsoft.AspNetCore.Authorization;

namespace dosxl.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class GrupoController : BaseController
    {
        [HttpGet]
        [AllowAnonymous]
        [Route("ObtenerGrupos")]
        public IActionResult getGrupos()
        {
            try
            {
                GrupoRepository lgrupo = new GrupoRepository();
                List<Grupo> grupo = lgrupo.getAll();
                
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
