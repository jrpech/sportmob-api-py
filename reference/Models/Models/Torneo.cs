using System;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;

namespace dosxl.Models
{
    [Serializable]
    [DataContract]
    public class Torneo
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }

        [DataMember(Name = "nombre")]
        public virtual string nombre { set; get; }

        [DataMember(Name = "noJornadas")]
        public virtual int noJornadas { set; get; }

        [DataMember(Name = "noGrupos")]
        public virtual int noGrupos { set; get; }

        [DataMember(Name = "equiposPorgrupo")]
        public virtual int equiposPorgrupo { set; get; }

        [DataMember(Name = "diasJuego")]
        public virtual string diasJuego { set; get; }

        [DataMember(Name = "fechaInicio")]
        public virtual string fechaInicio { set; get; }

        [DataMember(Name = "fechaFin")]
        public virtual string fechaFin { set; get; }

        [DataMember(Name = "preventa")]
        public virtual double preventa { set; get; }

        [DataMember(Name = "venta")]
        public virtual double venta { set; get; }

        [DataMember(Name = "finPreventa")]
        public virtual string finPreventa { set; get; }

        [DataMember(Name = "foto")]
        public virtual string foto { set; get; }

        [DataMember(Name = "imc")]
        public virtual double imc { set; get; }

        [DataMember(Name = "pmr")]
        public virtual double pmr { set; get; }

        [DataMember(Name = "requisitoFAT")]
        public virtual int requisitoFAT { set; get; }

        [DataMember(Name = "liguilla")]
        public virtual bool liguilla { set; get; }
    }
}
