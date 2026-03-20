using System.Runtime.Serialization;
using System;
using Org.BouncyCastle.Asn1;

namespace dosxl.Models.Models
{
    [Serializable]
    [DataContract]
    public class ContadorEvento
    {
        public int golesEquipo1 { get; set; }
        public int golesEquipo2 { get; set; }
        public int amarillaEquipo1 { get; set; }
        public int amarillaEquipo2 { get; set; }
        public int rojasEquipo1 { get; set; }
        public int rojasEquipo2 { get; set; }
        public int faltasEquipo1 { get; set; }
        public int faltasEquipo2 { get; set; }
        public double pausaAcumuladaPrimerTiempo { get; set; }
        public double pausaAcumuladaSegundoTiempo { get; set; }
        //seccion liguilla
        public string modo { get; set; }
        public string etapa { get; set; }
        public string estadoJornada { get; set; }
        public int marcadorGlobalEquipo1 { get; set; }
        public int marcadorGlobalEquipo2 { get; set; }
        public int penalesAnotadosEquipo1 { get; set; }
        public int penalesAnotadosEquipo2 { get; set; }
        public int penalesFalladosEquipo1 { get; set; }
        public int penalesFalladosEquipo2 { get; set; }


    }
}
