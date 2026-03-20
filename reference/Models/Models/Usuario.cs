using System;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;

namespace dosxl.Models
{
    [Serializable]
    [DataContract]
    public class Usuario
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }
        
        [DataMember(Name = "nombre")]
        public virtual string nombre { set; get; }

        [DataMember(Name = "apellidos")]
        public virtual string apellido { set; get; }
       
        [DataMember(Name = "correo")]
        public virtual string correo { set; get; }

        [DataMember(Name = "contrasenia")]
        public virtual string contrasenia { set; get; }

        [DataMember(Name = "telefono")]
        public virtual string telefono { set; get; }

        [DataMember(Name = "estado")]
        public virtual string estado { set; get; }

        [DataMember(Name = "foto")]
        public virtual string foto { set; get; }

        [DataMember(Name = "token")]
        public virtual string token { set; get; }

        [DataMember(Name = "origen")]
        public virtual string origen { set; get; }

        public Usuario()
        {

        }
    }
}
