using dosxl.Models.Models;
using dosxl.Utils;
using System.Collections.Generic;
using System.Linq;

namespace dosxl.Models.Repository
{
    public class GrupoRepository : RepositoryBase<Grupo>
    {
        public List<Grupo> getAll()
        {
            return _session.Query<Grupo>().ToList();
        }
        public Grupo getById(int id)
        {
            return _session.Query<Grupo>().Where(x =>
                      x.id == id).FirstOrDefault();
        }
    }
}
