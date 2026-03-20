using dosxl.Utils;
using NHibernate.Criterion;
using System.Collections.Generic;
using System.Linq;

namespace dosxl.Models.Repository
{
    public class TorneoRepository : RepositoryBase<Torneo>
    {
        public Torneo getById(int id)
        {
            return _session.Query<Torneo>().Where(x =>
                      x.id == id).FirstOrDefault();
        }
        public List<Torneo> getAll()
        {
            return _session.Query<Torneo>().ToList();
        }
        
        public List<Grupo> getPorToneo(int torneoID)
        {
            return _session.Query<Grupo>().Where(
                   x => x.torneoID == torneoID).ToList();
        }
        public Torneo ultimoid()
        {
            var lastID = _session.CreateCriteria(typeof(Torneo))
                .SetProjection(Projections.Max("id")).UniqueResult();
            int idtorneo = int.Parse(lastID.ToString());

            return _session.Query<Torneo>().Where(x => x.id == idtorneo).FirstOrDefault();
        }
        public bool save(Torneo torneo)
        {
            bool result = false;
            JugadorRepository ljugador = new JugadorRepository();

            if (torneo.id == 0)
            {
                var torneoid = ultimoid();
                torneo.foto = ljugador.SaveImageBase64(torneo.foto, torneoid.id + 1, "Fototorneo_");
                _session.Save(torneo);
                _session.Flush();

            }
            else
            {
                
                Torneo torneoSaved= getById(torneo.id);
                torneoSaved.nombre = torneo.nombre;
                torneoSaved.noJornadas = torneo.noJornadas;
                torneoSaved.noGrupos = torneo.noGrupos;
                torneoSaved.equiposPorgrupo = torneo.equiposPorgrupo;
                torneoSaved.diasJuego = torneo.diasJuego;
                torneoSaved.fechaInicio = torneo.fechaInicio;
                torneoSaved.fechaFin = torneo.fechaFin;
                torneoSaved.preventa = torneo.preventa;
                torneoSaved.venta = torneo.venta;
                torneoSaved.finPreventa = torneo.finPreventa;
                if (string.IsNullOrEmpty(torneo.foto))
                    torneoSaved.foto = ljugador.SaveImageBase64(torneo.foto, torneo.id, "Fototorneo_");
                torneoSaved.imc = torneo.imc;
                torneoSaved.pmr = torneo.pmr;
                torneoSaved.requisitoFAT = torneo.requisitoFAT;

                _session.Update(torneoSaved);
                _session.Flush();
                result = true;

            }

            return result;
        }

    }
}
