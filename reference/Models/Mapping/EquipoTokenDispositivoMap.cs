using dosxl.Models.Models;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class EquipoTokenDispositivoMap : ClassMap<EquipoTokenDispositivo>
    {
        public EquipoTokenDispositivoMap()
        {
            Table("equipotokendispositivo");
            Id(x => x.id).GeneratedBy.Identity();
            Map(x => x.token);
            Map(x => x.equipoID);
            Map(x => x.fechaRegistro);
            Map(x => x.partidoIniciado);
            Map(x => x.finPrimerTiempo);
            Map(x => x.inicioSegundoTiempo);
            Map(x => x.finPartido);
            Map(x => x.gol);
            Map(x => x.tarjetaAmarrilla);
            Map(x => x.tarjetaRoja);


        }
    }
}
