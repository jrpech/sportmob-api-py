using dosxl.Models.Request;
using dosxl.Utils;
using System.Collections.Generic;
using System.Linq;

namespace dosxl.Models.Repository
{
    public class EquipoRepository : RepositoryBase<Equipo>
    {
        public List<Equipo> getAll()
        {
            return _session.Query<Equipo>().ToList();
        }
        public List<Equipo> getPorGrupo(int grupoID)
        {
            return _session.Query<Equipo>().Where(
                   x => x.idGrupo == grupoID ).ToList();
        }
        
        public Equipo getEquipoPorId(int equipoID)
        {
            return _session.Query<Equipo>().Where(
                   x => x.id == equipoID).FirstOrDefault();
        }
        public void registrarPago(PagoRequest pago)
        {
            Equipo equipo = _session.Query<Equipo>().Where(
                   x => x.id == pago.equipoID).FirstOrDefault();

            equipo.jugadoresPagados += pago.noJugadoresPagar;
            _session.SaveOrUpdate(equipo);
            _session.Flush();
            _session.Clear();
        }

        public bool save( int partidoID)
        {
            bool result = false;

            Equipo equipoupdate = getEquipoPorId(partidoID);
            _session.Update(equipoupdate);
            _session.Flush();

            return result;
        }
        public bool cambiaestadoequipo(int equipoID)
        {
            bool result = false;

            Equipo equipoupdate = getEquipoPorId(equipoID);
            equipoupdate.eliminado = true;
            _session.Update(equipoupdate);
            _session.Flush();

            return result;
        }
    }
}
