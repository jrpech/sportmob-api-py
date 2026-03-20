using System;
namespace dosxl.Models.Request
{
    public class LoginRequest
    {
        public virtual string usuario { get; set; }
        public virtual string contrasena { get; set; }
        public virtual string tipo { get; set; }
    }
}
