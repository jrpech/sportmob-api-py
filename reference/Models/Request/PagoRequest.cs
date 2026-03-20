using System;
namespace dosxl.Models.Request
{
    public class PagoRequest
    {
        public virtual int equipoID { get; set; }
        public virtual int noJugadoresPagar { get; set; }

        public PagoRequest()
        {
        }
    }
}
