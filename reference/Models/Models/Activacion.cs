using System;
namespace dosxl.Models.Models
{
    [Serializable()]
    public class Activacion
    {
        public virtual int ActivacionId { get; set; }
        public virtual string Llave { get; set; }
        public virtual string Email { get; set; }
        public virtual int UsuarioId { get; set; }
        public virtual DateTime FechaVencimiento { get; set; }
        public virtual DateTime FechaAlta { get; set; }
        public virtual bool Activado { get; set; }
    }
}
