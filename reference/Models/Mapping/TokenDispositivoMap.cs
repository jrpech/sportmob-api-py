using System;
using FluentNHibernate.Mapping;
using dosxl.Models.Models;

namespace dosxl.Models.Mapping
{
    public class TokenDispositivoMap : ClassMap<TokenDispositivo>
    {
        public TokenDispositivoMap()
        {
            Table("usuarioToken");
            Id(x => x.id).GeneratedBy.Identity();
            Map(x => x.usuarioID);
            Map(x => x.token);
            Map(x => x.fechaRegistro);
        }
    }
}
