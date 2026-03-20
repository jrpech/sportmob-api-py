using System;
using System.Collections.Generic;

namespace dosxl.Models.Models
{
    
     public class liguilla
     {
         public Etapas octavos { get; set; }
         public Etapas cuartos { get; set; }
         public EtapasSemifinal semifinal { get; set; }
         public Partido final { get; set; }
         public Partido tercerLugar { get; set; }

        public liguilla()
        {
            octavos = new Etapas();
            cuartos = new Etapas();
            semifinal = new EtapasSemifinal();
            final = new Partido();
            tercerLugar = new Partido();

        }
    }
    public class Etapas
    {
        public List<Partido> llave1 { get; set; }
        public List<Partido> llave2 { get; set; }

        public Etapas()
        {
            llave1 = new List<Partido>();
            llave2 = new List<Partido>();
        }
    }
    public class EtapasSemifinal
    {
        public Partido llave1 { get; set; }
        public Partido llave2 { get; set; }

        public EtapasSemifinal()
        {
            llave1 = new Partido();
            llave2 = new Partido();
        }
    }

    public class Partido
    {
        public Equipo equipo1 { get; set; }
        public Equipo equipo2 { get; set; }
        public string marcadorGlobal { get; set; }
        public string marcadorIda { get; set; }
        public string marcadorVuelta { get; set; }
        public DateTime fechaHoraIda { get; set; }
        public DateTime fechaHoraVuelta { get; set; }
        public string estadoPartidoIda { get; set; }
        public string estadoPartidoVuelta { get; set; }
        public int idPartidoIda { get; set; }
        public int idPartidoVuelta { get; set; }
        public string lugarPartidoIda { get; set; }
        public string lugarPartidoVuelta { get; set; }
        public string horaIda { get; set; }
        public string horaVuelta { get; set; }
        public string tandaPenales { get; set; }

    }

}
