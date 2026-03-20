using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;

namespace dosxl.Models
{
    [Serializable]
    [DataContract]
    public class Grupo
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }

        [DataMember(Name = "nombre")]
        public virtual string nombre { set; get; }

        [DataMember(Name = "noEquipos")]
        public virtual int noEquipos { set; get; }

        [DataMember(Name = "tornoID")]
        public virtual int torneoID { set; get; }

        [DataMember(Name = "Equipos")]
        public virtual IList<Equipo> equipos { get; set; }

    }
}