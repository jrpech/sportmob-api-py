using System.Runtime.Serialization;
using System;
using System.Text.Json.Serialization;
using Org.BouncyCastle.Asn1.Cms;

namespace dosxl.Models.Models
{
    [Serializable]
    [DataContract]
    public class PartidosJornadas
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }

        [JsonPropertyName("jornada")]
        public virtual Jornadas idJornada { set; get; }

        [JsonPropertyName("equipo1")]
        public virtual Equipo? idEquipo1 { set; get; }

        [JsonPropertyName("equipo2")]
        public virtual Equipo? idEquipo2 { set; get; }

        [DataMember(Name = "fechaHoraPartido")]
        public virtual DateTime fechaHoraPartido { set; get; }

        [DataMember(Name = "lugar")]
        public virtual string lugar { set; get; }

        [DataMember(Name = "marcadorEquipo1")]
        public virtual int marcadorEquipo1 { set; get; }

        [DataMember(Name = "marcadorEquipo2")]
        public virtual int marcadorEquipo2 { set; get; }

        [DataMember(Name = "estadoPartido")]
        public virtual string estadoPartido { set; get; }

        [DataMember(Name = "hora")]
        public virtual string hora { set; get; }

        [DataMember(Name = "fechaHoraInicioPartido")]
        public virtual DateTime fechaHoraInicioPartido { set; get; }

        [DataMember(Name = "fechaHoraFinPrimerTiempo")]
        public virtual DateTime fechaHoraFinPrimerTiempo { set; get; }

        [DataMember(Name = "fechaHoraInicioSegundoTiempo")]
        public virtual DateTime fechaHoraInicioSegundoTiempo { set; get; }

        [DataMember(Name = "fechaHoraFinPartido")]
        public virtual DateTime fechaHoraFinPartido { set; get; }

        [DataMember(Name = "fechaHoraPausa")]
        public virtual DateTime fechaHoraPausa { set; get; }

        [DataMember(Name = "pausaAcumuladaPrimertiempo")]
        public virtual double pausaAcumuladaPrimerTiempo { set; get; }

        [DataMember(Name = "pausaAcumuladaSegundoTiempo")]
        public virtual double pausaAcumuladaSegundoTiempo { set; get; }

        [DataMember(Name = "tipoPartido")]
        public virtual string tipoPartido { set; get; }

        [DataMember(Name = "idaOvuelta")]
        public virtual string idaOvuelta { set; get; }

    }
}
