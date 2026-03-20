using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Net.Mail;
using System.Security.Claims;
using System.Text;
using Google.Protobuf.WellKnownTypes;
using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json.Linq;
using dosxl.Models;
using dosxl.Models.Models;
using static System.Net.Mime.MediaTypeNames;


namespace dosxl.Utils
{
    public class Utils
    {
        public static IConfiguration getConfiguration()
        {
            IConfigurationBuilder configurationBuilder = new ConfigurationBuilder();
            configurationBuilder.AddJsonFile("appsettings.json");
            IConfiguration _config = configurationBuilder.Build();
            return _config;
        }

        public static string generateJWTToken(int id, string name, string user)
        {
            IConfiguration _config = getConfiguration();

            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:SecretKey"]));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

            var claims = new[]
            {
                new Claim(JwtRegisteredClaimNames.Sub, user),
                new Claim("fullName", name.ToString()),
                new Claim("usuario", user.ToString()),
                new Claim("id", id.ToString()),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
            };

            var token = new JwtSecurityToken(
                issuer: _config["Jwt:Issuer"],
                audience: _config["Jwt:Audience"],
                claims: claims,
                expires: DateTime.Now.AddMinutes(43200),
                signingCredentials: credentials
                );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public static string doKeyActivation(string key1, string key2)
        {
            string keyData = key1 + DateTime.Now.ToShortDateString() + "_" + DateTime.Now.TimeOfDay;
            Cifrado oCifrado = new Cifrado();
            string key = oCifrado.EncriptarSHA1(keyData, key2);
            return key;
        }

        ///Date: 22 Julio 2019
        ///Author: Christian Tuyub
        ///<summary>
        ///Metodo que se encarga de establecer el objeto activacion, el cual contiene entre otros aspectos, el token con el que el usuario tendra permiso de cambiar su contrasena extraviada.
        ///proporcionado.
        /// </summary>
        public static Activacion estableceObjetoActivacion(string tokenActivacion, string correo, int usuarioIDNumero, DateTime fechaActualMasCincoDias, DateTime fechaActual)
        {
            Activacion activacionTransaccion = new Activacion();

            activacionTransaccion.Llave = tokenActivacion;
            activacionTransaccion.Email = correo;
            activacionTransaccion.UsuarioId = usuarioIDNumero;
            activacionTransaccion.FechaVencimiento = fechaActualMasCincoDias;
            activacionTransaccion.FechaAlta = fechaActual;
            activacionTransaccion.Activado = true;

            return activacionTransaccion;
        }

        public static ConfigSMTP getConfiguracionesCorreoSalida()
        {
            IConfiguration _config = getConfiguration();

            //bool SSL = bool.Parse(_config["Mail:ssl"]);
            string Host = _config["Mail:host"];
            string Password = _config["Mail:password"];
            int Port = int.Parse(_config["Mail:port"]);
            string User = _config["Mail:user"];
            //editar
            ConfigSMTP oConfsmtp = new ConfigSMTP
            {
                ConfigSMTPID = 0,
                //EnableSSl = SSL,
                Host = Host,
                Password = Password,
                Port = Port,
                UseDefCred = true,
                Usuario = User
            };

            return oConfsmtp;
        }

        public static void EnviarCorreo(List<string> para, string asunto, string mensaje, bool eshtml = false)
        {
            ConfigSMTP oConfsmtp = getConfiguracionesCorreoSalida();
            MailMessage mail = new MailMessage();
            mail.From = new MailAddress(oConfsmtp.Usuario);
            para.ForEach(a => mail.To.Add(a));
            mail.Subject = asunto;
            mail.SubjectEncoding = Encoding.UTF8;
            mail.Body = mensaje;
            mail.BodyEncoding = Encoding.UTF8;
            mail.IsBodyHtml = eshtml;

            SmtpClient smtp = new SmtpClient();
            smtp.Host = oConfsmtp.Host;
            //smtp.EnableSsl = oConfsmtp.EnableSSl;
            smtp.UseDefaultCredentials = oConfsmtp.UseDefCred;
            smtp.Port = oConfsmtp.Port;
            smtp.UseDefaultCredentials = false;
            smtp.Credentials = new NetworkCredential(oConfsmtp.Usuario, oConfsmtp.Password);
            smtp.DeliveryMethod = SmtpDeliveryMethod.Network;

            smtp.Send(mail);
        }

        public static string CreateBody(string link)
        {
            string body = string.Empty;

            using (StreamReader reader = new StreamReader(("Rdesign/RecuperarContraseña.cshtml")))
            {
                body = reader.ReadToEnd();
            }

            //body = body.Replace("{femail}", usuario);
            body = body.Replace("{flink}", link);
            return body;
        }
        
        public static void sendPushNotification(Notificacion notificacion, List<EquipoTokenDispositivo> tokens)
        {
            IConfiguration _config = getConfiguration();

            string SenderId = _config["Push:googleSenderID"];
            string AuthToken = _config["Push:googleAuthToken"];
            string NombreApp = _config["Push:nombreApp"];

            foreach (EquipoTokenDispositivo token in tokens)
            {
                HttpClient client = new HttpClient();
                client.BaseAddress = new Uri("https://fcm.googleapis.com/");
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
                client.DefaultRequestHeaders.TryAddWithoutValidation("Authorization", "key=" + AuthToken);

                Models.Request.PushRequest request = new Models.Request.PushRequest();
                request.to = token.token;
                request.notification.title = notificacion.titulo;
                request.notification.body = notificacion.descripcion;

                HttpResponseMessage response = client.PostAsJsonAsync("fcm/send", request).Result;

                var jsonstring = response.Content.ReadAsStringAsync();
                JObject json = JObject.Parse(jsonstring.Result);

                Console.WriteLine(json);

                if (response.IsSuccessStatusCode)
                {
                    if (json.GetValue("success").ToString() != "1")
                    {

                    }
                }

                client.Dispose();
            }
        }
    }
}