using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using dosxl.Models;
using dosxl.Models.Models;
using dosxl.Models.Repository;
using dosxl.Models.Request;
using dosxl.Models.Response;

namespace dosxl.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class LoginController : ControllerBase
    {

        [HttpPost]
        [Route("auth")]
        [AllowAnonymous]
        public IActionResult Login(LoginRequest login)
        {
            IActionResult response =
                Ok(new BaseResponse());

            try
            {
                Usuario user = AuthenticateUser(login);
                  if (user != null)
                    {
                        user.token = Utils.Utils.generateJWTToken(user.id, user.nombre, user.correo);
                        response = Ok(new
                            BaseResponse
                        {
                            respuesta = "OK",
                            mensaje = "",
                            data = user

                        });
                    }
                         
                    else
                        throw new Exception("Usuario y/o contraseña invalidos");

        }
            catch(Exception ex)
            {
                string errormensaje = ex.Message;

                if (ex.InnerException != null)
                {
                    errormensaje += ex.InnerException;        
                }
                response = Ok(new BaseResponse {
                    respuesta = "ERROR",
                    mensaje = errormensaje,
                });
            }

            return response;
        }

        Usuario AuthenticateUser(LoginRequest credenciales)
        { 
            UsuarioRepository rUsuario = new UsuarioRepository();
            Usuario usuario = rUsuario.login(credenciales.usuario, credenciales.contrasena);
            return usuario;
        }
         
    }
}
