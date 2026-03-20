using dosxl.Models.Models;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class EventosPartidoMap : ClassMap<EventosPartido>
    {
        public EventosPartidoMap()
        {
            Table("eventospartido");
            Id(x => x.id).GeneratedBy.Assigned();
            References(x => x.idPartido).Column("idPartido");
            References(x => x.idEquipo).Column("idEquipo");
            References(x => x.idjugador).Column("idjugador");
            Map(x => x.evento);
            Map(x => x.fechaHora);
            Map(x => x.minuto);
            Map(x => x.estadoPartido);
            Map(x => x.descripcion);

        }
    }
}
