using System;
namespace dosxl.Models.Request
{
    public class CambiarContrasenaRequest
    {
        public virtual string token { get; set; }
        public virtual string contrasena { get; set; }
        public virtual string contrasena2 { get; set; }
    }
}
