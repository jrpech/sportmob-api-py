using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.Linq;

namespace dosxl.Models.Models
{
    [Serializable]
    [DataContract]
    public class Goleadores
    {
        public int id { get; set; }
        public string nombre { get; set; }
        public string foto { get; set; }
        public string equipo { get; set; }
        public int goles { get; set; }





    }
}
