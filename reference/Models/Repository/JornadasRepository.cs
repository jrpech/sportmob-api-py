using dosxl.Models.Models;
using dosxl.Utils;
using FluentNHibernate.Conventions;
using NHibernate.Criterion;
using System;
using System.Collections.Generic;
using System.Linq;

namespace dosxl.Models.Repository
{
    public class JornadasRepository : RepositoryBase<Jornadas>
    {
            public List<Jornadas> getAll()
            {
                return _session.Query<Jornadas>().ToList();
            }
            public Jornadas getById(int id)
            {
                return _session.Query<Jornadas>().Where(x =>
                          x.id == id).FirstOrDefault();
            }
            public Jornadas ultimoid()
            {
                var lastID = _session.CreateCriteria(typeof(Jornadas))
                    .SetProjection(Projections.Max("id")).UniqueResult();
                int idjornada = int.Parse(lastID.ToString());

                return _session.Query<Jornadas>().Where(x => x.id == idjornada).FirstOrDefault();
            }

        public List<Jornadas> getAllJornadasPorNombreYetapa(string nombre , string etapa )
        {
            return _session.Query<Jornadas>().Where(x=> x.etapaLiguilla == etapa && x.nombreLiguilla == nombre && x.tipoJornada == "LIGUILLA" ).ToList();
        }
        public Jornadas byetapajornada(string etapa, string nombre)
        {
            return _session.Query<Jornadas>().Where(x => x.etapaLiguilla == etapa &&x.nombreLiguilla == nombre && x.tipoJornada == "LIGUILLA").FirstOrDefault();
        }
        public bool save(Jornadas jornada)
        {
            bool result = false;
            

            var lastID = _session.CreateCriteria(typeof(Jornadas))
                .SetProjection(Projections.Max("id")).UniqueResult();

            if (jornada.id == 0)
            {
                if (lastID == null)
                    jornada.id = 1;
                else
                    jornada.id = int.Parse(lastID.ToString()) + 1;

                _session.Save(jornada);
                _session.Flush();
            }
            else
            {
                Jornadas jornadaUpdate = getById(jornada.id);
                jornadaUpdate.nombre = jornada.nombre;
                jornadaUpdate.fechaInicio = jornada.fechaInicio;
                jornadaUpdate.fechaFin = jornada.fechaFin;

                _session.Update(jornadaUpdate);
                _session.Flush();
                result = true;

            }

            return result;
        }
        public Jornadas jornadaactualliguilla()
        {
            DateTime hora = horaActual();
            return _session.Query<Jornadas>().Where(x => hora.Date >= x.fechaInicio && hora.Date <= x.fechaFin && x.tipoJornada == "LIGUILLA").FirstOrDefault();
        }
        public List<Jornadas> actual()
        {
            DateTime hora = horaActual();
            return _session.Query<Jornadas>().Where(x =>  hora.Date >= x.fechaInicio &&  hora.Date <= x.fechaFin && x.tipoJornada != "LIGUILLA").ToList();
        }
        public List<Jornadas> pasado(List<Jornadas> jornadas)
        {
            var fechainicio = new DateTime();
            var fechafin = new DateTime();
            DateTime hora = horaActual();
            foreach (Jornadas jornada in jornadas) {
                fechainicio = jornada.fechaInicio;
                fechafin = jornada.fechaFin;

            }
            if (jornadas.Count == 0)
                fechainicio = hora;
            return _session.Query<Jornadas>().Where(x => x.fechaFin < fechainicio && x.tipoJornada != "LIGUILLA").ToList();
        }

        public List<Jornadas> proximos(List<Jornadas> jornadas)
        {
            var fechainicio = new DateTime();
            var fechafin = new DateTime();
            DateTime hora = horaActual();
            foreach (Jornadas jornada in jornadas)
            {
                fechainicio = jornada.fechaInicio;
                fechafin = jornada.fechaFin;

            }
            if (jornadas.Count == 0)
                fechafin = hora;
            return _session.Query<Jornadas>().Where(x => x.fechaInicio > fechafin && x.tipoJornada != "LIGUILLA").ToList();
        }
        public DateTime horaActual()
        {
            TimeZoneInfo horaMex = TimeZoneInfo.FindSystemTimeZoneById("Central Standard Time (Mexico)");

            DateTime hora = TimeZoneInfo.ConvertTime(DateTime.Now, horaMex);

            return hora;
        }
    }
}
