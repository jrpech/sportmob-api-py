using System.Runtime.Serialization;
using System;
using Newtonsoft.Json;
using System.Text.Json.Serialization;

namespace dosxl.Models.Models
{
    [Serializable]
    [DataContract]
    public class EventosPartido
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }
        
        [JsonPropertyName("partido")]
        public virtual PartidosJornadas idPartido { set; get; }

        [JsonPropertyName("equipo")]
        public virtual Equipo idEquipo { set; get; }

        [JsonPropertyName("jugador")]
        public virtual Jugador idjugador { set; get; }

        [DataMember(Name = "evento")]
        public virtual string evento { set; get; }

        [DataMember(Name = "fechaHora")]
        public virtual DateTime fechaHora { set; get; }

        [DataMember(Name = "minuto")]
        public virtual string minuto { set; get; }

        [DataMember(Name = "estadoPartido")]
        public virtual string estadoPartido { set; get; }

        [DataMember(Name = "descripcion")]
        public virtual string descripcion { set; get; }
    }
}
