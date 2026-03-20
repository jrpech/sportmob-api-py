using System;
namespace dosxl.Models.Models
{
    public class TokenDispositivo
    {
        public virtual int id { get; set; }
        public virtual int usuarioID { get; set; }
        public virtual string token { get; set; }
        public virtual DateTime fechaRegistro { get; set; }

        public TokenDispositivo()
        {
        }
    }
}
