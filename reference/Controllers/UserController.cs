using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using dosxl.Models.Repository;
using dosxl.Models;
using dosxl.Models.Request;
using dosxl.Models.Response;
using MySql.Data.MySqlClient;
using Microsoft.AspNetCore.Hosting.Server;
using NHibernate.Event.Default;
using Microsoft.AspNetCore.Http;
using PagedList;
using NHibernate.SqlCommand;
using FluentNHibernate.Testing.Values;
using dosxl.Models.Models;
using System.Text.Json.Nodes;
using Newtonsoft.Json;
using System.Text.Json.Serialization;
using NHibernate.Dialect.Function;
using NHibernate.Mapping;

namespace dosxl.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UserController : BaseController
    {
        [HttpPost]
        [AllowAnonymous]
        [Route("cambiarContrasena")]
        public IActionResult cambiarContrasena([FromBody] CambiarContrasenaRequest request)
        {
            UsuarioRepository rUsuario = new UsuarioRepository();
            UsuarioRepository lusuario = new UsuarioRepository();

            var usuarioToken = rUsuario.getUsuarioToken(request.token);
            if (usuarioToken != null)
            {
                Usuario oUsuario_ = rUsuario.getid(usuarioToken.UsuarioId);
                oUsuario_.contrasenia = request.contrasena;
                lusuario.save(oUsuario_);
                
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "Contraseña actualizada correctamente"
                });
            }
            else
            {
                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "Token no valido"
                });
            }

        }

        [HttpPost]
        [AllowAnonymous]
        [Route("solicitaCambioContrasena")]
        public IActionResult solicitaCambioContrasena(string usuario)
        {
            try
            {
                Activacion activacion = new Activacion();
                ActivacionRepository rActivacion = new ActivacionRepository();
                ConfiguracionRepository rConfiguracion = new ConfiguracionRepository();
                Usuario oUsuario_ = new Usuario();
                UsuarioRepository rUsuario = new UsuarioRepository();

                oUsuario_ = rUsuario.getUsuarioByEmail(usuario);

                if (oUsuario_ == null)
                {
                    throw new Exception("Usuario No Existente");
                }

                string usuarioID = oUsuario_.id.ToString();
                int usuarioIDNumero = oUsuario_.id;
                string tokenActivacion = Utils.Utils.doKeyActivation(usuarioID, usuario);
                DateTime fechaActual = DateTime.Now;
                DateTime fechaActualMasCincoDias = fechaActual.AddDays(5);

                activacion = Utils.Utils.estableceObjetoActivacion(tokenActivacion, usuario, usuarioIDNumero, fechaActualMasCincoDias, fechaActual);
                rActivacion.GuardarActivacion(activacion);
                //rActivacion._session.Transaction.Commit();

                //ENVIAR EMAIL
                Configuracion oConfiguracion = rConfiguracion.GetByClave("PLANTILLA_RECUPERAR");
                Configuracion oConfiguracionURL = rConfiguracion.GetByClave("URL_RECUPERAR_CONTRASENA");
                Configuracion oConfiguracionAsunto = rConfiguracion.GetByClave("ASUNTO_RECUPERAR");

                string nombreUsuario = oUsuario_.nombre;
                string urlDeBaseDeDatos = oConfiguracionURL.Valor;
                string urlMasToken = String.Concat(urlDeBaseDeDatos, tokenActivacion);
                string asunto = oConfiguracionAsunto.Valor;
                string cuerpoMensajeDefault = oConfiguracion.Valor;

                string cuerpoMensajeAEnviar = cuerpoMensajeDefault.Replace("[USUARIO]", nombreUsuario).Replace("[URL]", urlMasToken);

                List<string> listaCorreo = new List<string>();
                listaCorreo.Add(usuario);
                var mensaje = Utils.Utils.CreateBody(cuerpoMensajeAEnviar);
                Utils.Utils.EnviarCorreo(listaCorreo, asunto, mensaje, true);

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "Se envió un correo para poder realizar el cambio de contraseña"
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

        [AllowAnonymous]
        [HttpPost]
        [Route("GenerarUsuario")]
        public IActionResult usuario(Usuario usuario)
        {

            try
            {
                UsuarioRepository lusuario = new UsuarioRepository();
                Usuario user = lusuario.getBycorreo(usuario.correo);
                
                if (user == null)
                {
                    if (usuario.origen == "APP")
                    {

                        lusuario.save(usuario);
                        return Ok(new BaseResponse
                        {
                            respuesta = "OK",
                            mensaje = "El registro fue exitoso, por favor vaya" +
                                            " a su correo para verificar su " +
                                         "cuenta y pueda acceder a la aplicación",

                        });

                    }
                    else
                    {

                        if (lusuario.validarRegistro(usuario) == false)
                        {
                            lusuario.save(usuario);
                            usuario.token = lusuario.token(usuario.correo);

                        }
                        else
                        {
                            lusuario.save(usuario);
                            usuario.token = lusuario.token(usuario.correo);
                            return Ok(new BaseResponse
                            {
                                respuesta = "OK",
                                mensaje = "Faltan datos requeridos",
                                data = usuario
                            });
                        }

                    }

                }
                else
                {
                    if (usuario.origen != "APP")
                    {
                        if (lusuario.validarusuarioexistente(usuario) != false)
                        {
                            lusuario.update(usuario);
                            usuario.token = lusuario.token(usuario.correo);
                        }
                        else
                            lusuario.update(usuario);
                        usuario.token = lusuario.token(usuario.correo);
                    }
                    else
                    {
                        return Ok(new BaseResponse
                        {
                            respuesta = "ERROR",
                            mensaje = "El usuario ya se encuentra registrado",

                        });
                    }
                }

                return Ok(new BaseResponse
                {
                    respuesta = "OK",
                    mensaje = "",
                    data = usuario

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
        [Route("EliminarUsuario")]
        public IActionResult Eliminar(int id)
        {
            try
            {
                UsuarioRepository lusuario = new UsuarioRepository();

                lusuario.elminar(id);

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
