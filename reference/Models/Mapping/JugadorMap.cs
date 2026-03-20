using System;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class JugadorMap : ClassMap<Jugador>
    {
        public JugadorMap()
        {
            Table("jugador");
            Id(x => x.id).GeneratedBy.Assigned();
            Map(x => x.nombre);
            Map(x => x.apellido);
            Map(x => x.fechaNacimiento);
            Map(x => x.peso);
            Map(x => x.altura);
            Map(x => x.email);
            Map(x => x.telefono);
            Map(x => x.posicion);
            Map(x => x.talla);
            Map(x => x.noJugador);
            Map(x => x.nombreJersy);
            Map(x => x.foto);
            Map(x => x.equipoID);
            Map(x => x.estado);
            Map(x => x.codigoPostal);
            Map(x => x.fechaRegistro);
            Map(x => x.esCapitan);

        }
    }
}