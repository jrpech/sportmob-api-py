using System;
using FluentNHibernate.Mapping;
using dosxl.Models.Models;

namespace dosxl.Models.Mapping
{
    class ConfiguracionMap : ClassMap<Configuracion>
    {
        public ConfiguracionMap()
        {
            
            Id(x => x.Clave).GeneratedBy.Assigned();
            Map(x => x.Descripcion);
            Map(x => x.Tipo);
            Map(x => x.Valor);
            Map(x => x.Estado);
        }
    }
}
