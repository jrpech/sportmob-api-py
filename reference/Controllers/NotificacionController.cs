using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Linq;
using System.Net.Http;
using System.Net;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.VisualBasic;
using NHibernate.Mapping;
using dosxl.Models;
using dosxl.Models.Repository;
using dosxl.Models.Request;
using dosxl.Models.Response;
using Microsoft.Extensions.Logging;
using Antlr.Runtime;
using Google.Protobuf.WellKnownTypes;
using System.Text.RegularExpressions;


namespace dosxl.Controllers
{
    //[Authorize]
    //[ApiController]
    //[Route("api/[controller]")]
    /*public class NotificacionController : BaseController
    {
        //[HttpPost]
        //[Route("save")]
        public IActionResult save(Notificacion notificacion)
        {
            try
            {
                NotificacionRepository rnotificacion = new NotificacionRepository();
                string Date = DateTime.Now.ToString("yyyy-MM-dd");
                notificacion.fechaNotificacion = DateTime.Parse(Date);
                notificacion.descripcion = DateTime.Parse(Date) + notificacion.descripcion;
                notificacion.usuario = usuarioIDLoggeado();
                rnotificacion.save(notificacion);

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


        //[HttpGet]
        //[Route("getNotificacion")]
        public IActionResult getNotificacion()
        {
            IActionResult response =
                Ok(new BaseResponse());

            try
            {
                NotificacionRepository rnotificacion = new NotificacionRepository();
                List<Notificacion> notificacion = rnotificacion.getAll(usuarioIDLoggeado());

                response = Ok(new BaseResponse
                { 
                    respuesta = "OK",
                    mensaje = "",
                    data = notificacion
                });
            }
            catch (Exception ex)
            {
                string errormensaje = ex.Message;

                if (ex.InnerException != null)
                {
                    errormensaje += ex.InnerException;
                }
                response = Ok(new BaseResponse
                {
                    respuesta = "ERROR",
                    mensaje = errormensaje,
                });
            }

            return response;
        }

        //[HttpPost]
        //[Route("NotificacionLeida")]
        public IActionResult marcarleido()
        {
            try
            {
                NotificacionRepository lnotificacion = new NotificacionRepository();
                Usuario loggeado = usuarioLoggeado();
                List<Notificacion> notificacion = lnotificacion.getAllcondominos(usuarioIDLoggeado());
                

                if (loggeado.origen == "ADMIN")
                {
                    

                }
                else if (loggeado.origen == "COND")
                {

                    foreach (Notificacion element in notificacion)
                    {
                        Console.Write($"{element} ");
                        if (element.leido == false) {
                            lnotificacion.actualizaleido(element.leido, usuarioIDLoggeado());

                        }   
                    }

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
    }*/
}