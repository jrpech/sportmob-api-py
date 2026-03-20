using System;
using System.Runtime.Serialization;

namespace dosxl.Models
{
    [Serializable]
    [DataContract]
    public class Notificacion
    {
        [DataMember(Name = "id")]
        public virtual int id { get; set; }

        [DataMember(Name = "titulo")]
        public virtual string titulo { get; set; }

        [DataMember(Name = "descripcion")]
        public virtual string descripcion { get; set; }

        [DataMember(Name = "leido")]
        public virtual bool leido { get; set; }

        [DataMember(Name = "usuario")]
        public virtual int usuario { get; set; }

        [DataMember(Name = "fechaNotificacion")]
        public virtual  DateTime fechaNotificacion { get; set; }

        public Notificacion()
        {
            fechaNotificacion = DateTime.Now;
            leido = false;
            id = 0;
        }
    }
}
