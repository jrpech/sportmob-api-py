using System;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class TorneoMap : ClassMap<Torneo>
    {
        public TorneoMap()
        {
            Table("torneo");
            Id(x => x.id).GeneratedBy.Assigned();
            Map(x => x.nombre);
            Map(x => x.noJornadas);
            Map(x => x.noGrupos);
            Map(x => x.equiposPorgrupo);
            Map(x => x.diasJuego);
            Map(x => x.fechaInicio);
            Map(x => x.fechaFin);
            Map(x => x.preventa);
            Map(x => x.venta);
            Map(x => x.finPreventa);
            Map(x => x.foto);
            Map(x => x.imc);
            Map(x => x.pmr);
            Map(x => x.requisitoFAT);
            Map(x => x.liguilla);

        }
    }
}