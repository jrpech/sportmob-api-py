using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.Linq;
using System.Collections;

namespace dosxl.Models.Models
{
    [Serializable]
    [DataContract]
    public class JornadaVista
    {
        public int id { get; set; }
        public string nombre { get; set; }
        public DateTime fechaInicio { get; set; }
        public DateTime fechaFin { get; set; }
        public List<Dias> dias { get; set; }

       public  JornadaVista() {
            dias = new List<Dias>();
        }
    }
}
