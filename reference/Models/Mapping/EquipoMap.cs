using System;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class EquipoMap : ClassMap<Equipo>
    {
        public EquipoMap()
        {
            Table("equipo");
            Id(x => x.id).GeneratedBy.Identity();
            Map(x => x.nombreEquipo);
            Map(x => x.idGrupo);
            Map(x => x.fotoEquipo);
            Map(x => x.fotoUniforme);
            Map(x => x.jugadoresPagados);
            Map(x => x.juegosJugados);
            Map(x => x.juegosGanados);
            Map(x => x.juegosEmpatados);
            Map(x => x.juegosPerdidos);
            Map(x => x.golesAFavor);
            Map(x => x.golesEnContra);
            Map(x => x.diferenciaDeGoles);
            Map(x => x.puntos);
            Map(x => x.numero);
            Map(x => x.ptsExtrasOAmosnetacion);
            Map(x => x.eliminado);

        }
    }
}