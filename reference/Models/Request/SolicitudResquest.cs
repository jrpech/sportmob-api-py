using System;

namespace dosxl.Models.Request
{
    public class SolicitudResquest
    {
        public virtual DateTime fecha { get; set; }
        public virtual string hora { get; set; }
        public virtual int id { get; set; }
    }
}
