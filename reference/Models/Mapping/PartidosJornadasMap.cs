using dosxl.Models.Models;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class PartidosJornadasMap : ClassMap<PartidosJornadas>
    {
        public PartidosJornadasMap()
        {
            Table("partidosjornadas");
            Id(x => x.id).GeneratedBy.Identity();
            References(x => x.idJornada).Column("idJornada");
            References(x => x.idEquipo1).Column("idEquipo1");
            References(x => x.idEquipo2).Column("idEquipo2");
            Map(x => x.fechaHoraPartido);
            Map(x => x.lugar);
            Map(x => x.marcadorEquipo1);
            Map(x => x.marcadorEquipo2);
            Map(x => x.estadoPartido);
            Map(x => x.hora);
            Map(x => x.fechaHoraInicioPartido);
            Map(x => x.fechaHoraFinPrimerTiempo);
            Map(x => x.fechaHoraInicioSegundoTiempo);
            Map(x => x.fechaHoraFinPartido);
            Map(x => x.fechaHoraPausa);
            Map(x => x.pausaAcumuladaPrimerTiempo);
            Map(x => x.pausaAcumuladaSegundoTiempo);
            Map(x => x.tipoPartido);
            Map(x => x.idaOvuelta);


        }
    }
}
