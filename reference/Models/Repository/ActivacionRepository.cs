using System;
using System.Collections.Generic;
using System.Linq;
using dosxl.Models.Models;
using dosxl.Utils;

namespace dosxl.Models.Repository
{
    internal class ActivacionRepository : RepositoryBase<Activacion>
    {
      public List<Activacion> GetAllActivacion()
        {
            List<Activacion> lsActivacion = new List<Activacion>();
            lsActivacion = _session.QueryOver<Activacion>().List().ToList();
            return lsActivacion;
        }
        
        public List<Activacion> GetAllActivacionActivadas()
        {
            List<Activacion> lsActivacion = new List<Activacion>();
            lsActivacion = _session.QueryOver<Activacion>().Where(f => f.Activado).List().ToList();
            return lsActivacion;
        }

        public Activacion GuardarActivacion(Activacion oActivacion)
        {
            _exito = false;
            _session.SaveOrUpdate(oActivacion);
            _session.Flush();
            _exito = false;
            return oActivacion;
        }

        public int GetUsuarioIDByLlaveActivacion(string key)
        {
            int iUsuario = 0;

            Activacion oAct = _session.Query<Activacion>().Where(x => x.Llave == key).FirstOrDefault();

            if (oAct != null)
                iUsuario = oAct.UsuarioId;

            return iUsuario;
        }

        public Activacion GetKeyByLlave(string key)
        {

            Activacion oAct = _session.Query<Activacion>().Where(x => x.Llave == key).FirstOrDefault();
            _session.Clear();
            return oAct;
        }
    }
}
