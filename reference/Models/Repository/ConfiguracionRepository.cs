using System;
using System.Linq;
using dosxl.Models.Models;
using dosxl.Utils;

namespace dosxl.Models.Repository
{
    internal class ConfiguracionRepository : RepositoryBase<Configuracion>
    {
        public Configuracion GetByClave(string clave)
        {
            return _session.Query<Configuracion>().Where(x => x.Clave == clave).FirstOrDefault();
        }
    }
}