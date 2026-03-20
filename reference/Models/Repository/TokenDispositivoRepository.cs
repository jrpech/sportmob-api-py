using System;
using System.Collections.Generic;
using System.Linq;
using dosxl.Models.Models;
using dosxl.Models.Request;
using dosxl.Utils;

namespace dosxl.Models.Repository
{
    public class TokenDispositivoRepository : RepositoryBase<TokenDispositivo>
    {
        public void save(int usuarioID, string token)
        {
            TokenDispositivo tokenExistente = _session.Query<TokenDispositivo>().Where(x => x.token == token && x.usuarioID == usuarioID).FirstOrDefault();

            if(tokenExistente == null)
            {
                TokenDispositivo tokenNuevo = new TokenDispositivo();
                tokenNuevo.token = token;
                tokenNuevo.usuarioID = usuarioID;
                tokenNuevo.fechaRegistro = DateTime.Now;
                _session.Save(tokenNuevo);
                _session.Flush();
            }
        }

        public void saveTokenequipofavorito(EquipoFavoritoRequest dato)
        {
            EquipoTokenDispositivo tokenExistente = _session.Query<EquipoTokenDispositivo>().Where(x => x.token == dato.token).FirstOrDefault();
            JornadasRepository jornadal = new JornadasRepository();
            var actual = jornadal.horaActual();

            if (tokenExistente == null)
            {
                EquipoTokenDispositivo tokenNuevo = new EquipoTokenDispositivo();
                tokenNuevo.token = dato.token;
                tokenNuevo.equipoID = dato.equipo;
                tokenNuevo.fechaRegistro = actual;
                tokenNuevo.partidoIniciado = true;
                tokenNuevo.finPrimerTiempo = true;
                tokenNuevo.inicioSegundoTiempo = true;
                tokenNuevo.finPartido = true;
                tokenNuevo.gol = true;
                tokenNuevo.tarjetaAmarrilla = true;
                tokenNuevo.tarjetaRoja = true;

                _session.Save(tokenNuevo);
                _session.Flush();
            }
             else 
             {
                EquipoTokenDispositivo update = getPortokenEquipofavorito(dato.token);
                update.equipoID = dato.equipo;
                _session.SaveOrUpdate(update);
                _session.Flush();
            }
        }
        public void ConfigurarNotificacionTokenequipofavorito(EquipoTokenDispositivo configuracion)
        {
            EquipoTokenDispositivo tokenExistente = _session.Query<EquipoTokenDispositivo>().Where(x => x.token == configuracion.token).FirstOrDefault();
            
            if (tokenExistente != null)
            {
                EquipoTokenDispositivo update = getPortokenEquipofavorito(configuracion.token);

                update.partidoIniciado = configuracion.partidoIniciado;
                update.finPrimerTiempo = configuracion.finPrimerTiempo;
                update.inicioSegundoTiempo = configuracion.inicioSegundoTiempo;
                update.finPartido = configuracion.finPartido;
                update.gol = configuracion.gol;
                update.tarjetaAmarrilla = configuracion.tarjetaAmarrilla;
                update.tarjetaRoja = configuracion.tarjetaRoja;

                _session.SaveOrUpdate(update);
                _session.Flush();
 
            }
        }
        public List<TokenDispositivo> getTokensPorUsuario(int usuarioID)
        {
            return _session.Query<TokenDispositivo>().Where(x => x.usuarioID == usuarioID).ToList();
        }
        public TokenDispositivo getToken(string token)
        {
            return _session.Query<TokenDispositivo>().Where(x => x.token == token).FirstOrDefault();
        }

        public EquipoTokenDispositivo getPortokenEquipofavorito(string token)
        {
            return _session.Query<EquipoTokenDispositivo>().Where(x => x.token == token).FirstOrDefault();
        }
        public bool elminar(int id, string token)
        {
            bool result = false;

            TokenDispositivo categoriaSaved = getById(id, token);
            _session.Delete(categoriaSaved);
            _session.Flush();

            return result;
        }

        public TokenDispositivo getById(int id , string token)
        {
            return _session.Query<TokenDispositivo>().Where(x => x.id == id && x.token == token).FirstOrDefault();
        }
        public List<EquipoTokenDispositivo> getAlltokens()
        {
            return _session.Query<EquipoTokenDispositivo>().ToList();
        }
    }
}
