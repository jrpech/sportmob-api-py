using System.Runtime.Serialization;
using System;
using System.Collections.Generic;

namespace dosxl.Models.Models
{
    [Serializable]
    [DataContract]
    public class Dias
    {
        public string  fechaNombre { get; set; }
        public DateTime fecha { get; set; }
        public IEnumerable<PartidosJornadas> partidos { get; set; }
    }
}
