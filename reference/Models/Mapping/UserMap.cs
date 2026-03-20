using System;
using FluentNHibernate.Mapping;

namespace tamara_api.Models.Mapping
{
    public class UserMap : ClassMap<Horario>
    {
        public UserMap()
        {
            Table("User");
            Id(x => x.id).GeneratedBy.Identity();
            Map(x => x.name);
            Map(x => x.user);
            Map(x => x.password);
            Map(x => x.address);
            Map(x => x.phone);
            Map(x => x.picture);
            Map(x => x.type);
            Map(x => x.status);
            Map(x => x.token);
        }
    }
}
