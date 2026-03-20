using System;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;

namespace dosxl.Models
{
    [Serializable]
    [DataContract]
    public class Jugador
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }

        [DataMember(Name = "nombre")]
        public virtual string nombre { set; get; }

        [DataMember(Name = "apellido")]
        public virtual string apellido { set; get; }

        [DataMember(Name = "fechaNacimiento")]
        public virtual string fechaNacimiento { set; get; }

        [DataMember(Name = "peso")]
        public virtual double peso { set; get; }

        [DataMember(Name = "altura")]
        public virtual double altura { set; get; }

        [DataMember(Name = "email")]
        public virtual string email { set; get; }

        [DataMember(Name = "telefono")]
        public virtual string telefono { set; get; }

        [DataMember(Name = "posicion")]
        public virtual string posicion { set; get; }

        [DataMember(Name = "talla")]
        public virtual string talla { set; get; }

        [DataMember(Name = "noJugador")]
        public virtual int noJugador { set; get; }

        [DataMember(Name = "nombreJersy")]
        public virtual string nombreJersy { set; get; }

        [DataMember(Name = "foto")]
        public virtual string foto { set; get; }

        [DataMember(Name = "equipoID")]
        public virtual int equipoID { set; get; }

        [DataMember(Name = "estado")]
        public virtual bool estado { set; get; }

        [DataMember(Name = "CodigoPostal")]
        public virtual int codigoPostal { set; get; }

        [DataMember(Name = "fechaRegistro")]
        public virtual DateTime fechaRegistro { set; get; }

        [DataMember(Name = "esCapitan")]
        public virtual bool esCapitan { set; get; }

    }
}