using System;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class NotificacionMap : ClassMap<Notificacion>
    {
        public NotificacionMap()
        {
            Table("notificacion");
            Id(x => x.id).GeneratedBy.Identity();
            Map(x => x.titulo);
            Map(x => x.descripcion);
            Map(x => x.leido); 
            Map(x => x.usuario);
            Map(x => x.fechaNotificacion);
        }
    }
}
