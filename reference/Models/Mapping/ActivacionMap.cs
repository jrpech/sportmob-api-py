using System;
using FluentNHibernate.Mapping;
using dosxl.Models.Models;

namespace dosxl.Models.Mapping
{
    public class ActivacionMap : ClassMap<Activacion>
    {
        public ActivacionMap()
        {
            Id(x => x.ActivacionId).GeneratedBy.Identity();
            Map(x => x.Llave);
            Map(x => x.Email);
            Map(x => x.UsuarioId);
            Map(x => x.FechaVencimiento);
            Map(x => x.FechaAlta);
            Map(x => x.Activado);

        }
    }
}
