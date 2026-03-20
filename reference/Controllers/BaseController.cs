using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using dosxl.Models;
using dosxl.Models.Repository;

namespace dosxl.Controllers
{
    [Authorize]
    [Route("api/[controller]")]
    public class BaseController : Controller
    {
        internal int usuarioIDLoggeado()
        {
            //Se obtiene el ID del vendedor Logueado
            var user = User.FindFirst("id").Value;

            return int.Parse(user);
        }

        internal Usuario usuarioLoggeado()
        {
            var user = User.FindFirst("id").Value;

            UsuarioRepository rlogueado = new UsuarioRepository();
            Usuario logueado = rlogueado.getid(int.Parse(user));
            //int.Parse(user);
            return logueado;
        }
    }
}
