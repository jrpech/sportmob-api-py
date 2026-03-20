using System.Runtime.Serialization;
using System;
using System.Text.Json.Serialization;
using System.Collections.Generic;
using static System.Net.Mime.MediaTypeNames;
using NHibernate;

namespace dosxl.Models.Models
{
    [Serializable]
    [DataContract]
    public class Jornadas
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }

        [DataMember(Name = "nombre")]
        public virtual string nombre { set; get; }

        [DataMember(Name = "fechaInicio")]
        public virtual DateTime fechaInicio { set; get; }

        [DataMember(Name = "fechaFin")]
        public virtual DateTime fechaFin { set; get; }

        [DataMember(Name = "tipoJornada")]
        public virtual string tipoJornada { set; get; }

        [DataMember(Name = "nombreLiguilla")]
        public virtual string nombreLiguilla { set; get; }

        [DataMember(Name = "etapaLiguilla")]
        public virtual string etapaLiguilla { set; get; }

        [DataMember(Name = "llaveLiguilla")]
        public virtual int llaveLiguilla { set; get; }

        [DataMember(Name = "posicionLlave")]
        public virtual int posicionLlave { set; get; }

        [DataMember(Name = "siguienteJornada")]
        public virtual int siguienteJornada { set; get; }

    }
}
