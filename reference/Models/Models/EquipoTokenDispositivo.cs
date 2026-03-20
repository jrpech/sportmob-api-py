using System;

namespace dosxl.Models.Models
{
    public class EquipoTokenDispositivo
    {
        public virtual int id { get; set; }
        public virtual string token { get; set; }
        public virtual int equipoID { get; set; }
        public virtual DateTime fechaRegistro { get; set; }
        public virtual bool partidoIniciado { get; set; }
        public virtual bool finPrimerTiempo { get; set; }
        public virtual bool inicioSegundoTiempo { get; set; }
        public virtual bool finPartido { get; set; }
        public virtual bool gol { get; set; }
        public virtual bool tarjetaAmarrilla { get; set; }
        public virtual bool tarjetaRoja { get; set; }


        public EquipoTokenDispositivo()
        {
        }
    }

}
