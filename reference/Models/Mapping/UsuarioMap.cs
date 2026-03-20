using System;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class UsuarioMap : ClassMap<Usuario>
    {
        public UsuarioMap()
        {
            Table("usuario");
            Id(x => x.id).GeneratedBy.Assigned();
            Map(x => x.nombre);
            Map(x => x.apellido);
            Map(x => x.correo);
            Map(x => x.contrasenia);
            Map(x => x.telefono);
            Map(x => x.estado);
            Map(x => x.foto);
            Map(x => x.token);
            Map(x => x.origen);

        }
    }
}
