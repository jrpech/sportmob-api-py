using System;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;
using System.Text.Json.Serialization;

namespace dosxl.Models
{
    [Serializable]
    [DataContract]
    public class Equipo
    {
        [DataMember(Name = "ID")]
        public virtual int id { set; get; }

        [DataMember(Name = "nombreEquipo")]
        public virtual string nombreEquipo { set; get; }

        [DataMember(Name = "idGrupo")]
        public virtual int idGrupo { set; get; }

        [DataMember(Name = "fotoEquipo")]
        public virtual string fotoEquipo { set; get; }

        [DataMember(Name = "fotoUnifrome")]
        public virtual string fotoUniforme { set; get; }

        [DataMember(Name = "jugadoresPagados")]
        public virtual int jugadoresPagados { set; get; }

        [DataMember(Name = "jugadoresRegistrados")]
        public virtual int jugadoresRegistrados { set; get; }

        [DataMember(Name = "juegosJugados")]
        public virtual int juegosJugados { set; get; }

        [DataMember(Name = "juegosGanados")]
        public virtual int juegosGanados { set; get; }

        [DataMember(Name = "juegosEmpatados")]
        public virtual int juegosEmpatados { set; get; }

        [DataMember(Name = "juegosPerdidos")]
        public virtual int juegosPerdidos { set; get; }

        [DataMember(Name = "golesAFavor")]
        public virtual double golesAFavor { set; get; }

        [DataMember(Name = "golesEnContra")]
        public virtual double golesEnContra { set; get; }

        [DataMember(Name = "diferenciaDeGoles")]
        public virtual double diferenciaDeGoles { set; get; }

        [DataMember(Name = "puntos")]
        public virtual double puntos { set; get; }

        [DataMember(Name = "numero")]
        public virtual int numero { set; get; }

        [DataMember(Name = "capitan")]
        public virtual Jugador capitan { set; get; }

        [DataMember(Name = "grupo")]
        public virtual string grupo { set; get; }

        [DataMember(Name = "ptsExtrasOAmosnetacion")]
        public virtual double ptsExtrasOAmosnetacion { set; get; }

        [DataMember(Name = "eliminado")]
        public virtual bool eliminado { set; get; }

    }
}