using dosxl.Models.Models;
using FluentNHibernate.Mapping;

namespace dosxl.Models.Mapping
{
    public class JornadasMap : ClassMap<Jornadas>
    {
        public JornadasMap()
        {
            Table("jornadas");
            Id(x => x.id).GeneratedBy.Assigned();
            Map(x => x.nombre);
            Map(x => x.fechaInicio);
            Map(x => x.fechaFin);
            Map(x => x.tipoJornada);
            Map(x => x.nombreLiguilla);
            Map(x => x.etapaLiguilla);
            Map(x => x.llaveLiguilla);
            Map(x => x.posicionLlave);
            Map(x => x.siguienteJornada);

        }
    }
}
