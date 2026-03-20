using System;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class GrupoMap : ClassMap<Grupo>
    {
        public GrupoMap()
        {
            Table("grupo");
            Id(x => x.id).GeneratedBy.Assigned();
            Map(x => x.nombre);
            Map(x => x.noEquipos);
            Map(x => x.torneoID);
            HasMany(x => x.equipos).Table("equipo").AsBag().KeyColumn("idGrupo").Cascade.AllDeleteOrphan().Inverse();
        }
    }
}