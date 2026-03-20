using System;
namespace dosxl.Models.Models
{
    public class Configuracion
    {
        public virtual string Clave { get; set; }
        public virtual string Descripcion { get; set; }
        public virtual string Tipo { get; set; }
        public virtual string Valor { get; set; }
        public virtual string Estado { get; set; }
    }
}
