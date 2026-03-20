using MySql.Data.MySqlClient;
using MySqlX.XDevAPI.Common;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using dosxl.Utils;
using System.ComponentModel.DataAnnotations;
using dosxl.Models.Models;

namespace dosxl.Models.Repository
{
    public class UsuarioRepository : RepositoryBase<Usuario>
    {
        public Usuario login(string usuario, string contrasena)
        {
            return _session.Query<Usuario>().Where(
                     x => x.correo == usuario
                     && x.contrasenia == contrasena).FirstOrDefault();
        }
        public Usuario usuarioporcorreo(string correo)
        {
            return _session.Query<Usuario>().Where(
                     x => x.correo == correo).FirstOrDefault();
        }
        public Usuario getById(int id)
        {
            return _session.Query<Usuario>().Where(x => 
                      x.id == id).FirstOrDefault();
        }
        public Usuario getBycorreo(string correo)
        {
            return _session.Query<Usuario>().Where(x =>
                      x.correo == correo).FirstOrDefault();
        }
        public Usuario getid(int id)
        {
            return _session.Query<Usuario>().Where(
                   x => x.id == id).FirstOrDefault();

        }

        public List<Usuario> getAllusuarios()
        {
            return _session.Query<Usuario>().ToList();
        }
      
        public bool save(Usuario usuario)
        {
            bool result = false;

            if (usuario.id == 0)
            {
                _session.Save(usuario);
                _session.Flush();

            }
            else
            {   
                
                Usuario userSaved = getById(usuario.id);
                _session.Save(userSaved);
                _session.Flush();
                result = true;
            }

            return result;
        }
        public bool elminar(int id)
        {
            bool result = false;

            Usuario userDelet = getById(id);
            _session.Delete(userDelet);
            _session.Flush();

            return result;
        }

        public Usuario getUsuarioByEmail(string correo)
        {
            return _session.Query<Usuario>().FirstOrDefault(x => 
                           x.correo == correo); 
        }

        public bool validarRegistro(Usuario usuario)
        {
            bool result;

            if (String.IsNullOrEmpty(usuario.nombre)
             || String.IsNullOrEmpty(usuario.apellido)
             || String.IsNullOrEmpty(usuario.correo)
             || String.IsNullOrEmpty(usuario.telefono)
             || String.IsNullOrEmpty(usuario.estado)
             || String.IsNullOrEmpty(usuario.origen)
             )
            {
                result = true;
            }
            else
            {
                result = false;
            }


            return result;
        }

        public bool validarusuarioexistente(Usuario usuario)
        {
            bool result;

            if (String.IsNullOrEmpty(usuario.nombre)
            || String.IsNullOrEmpty(usuario.apellido)
            || String.IsNullOrEmpty(usuario.correo)
            || String.IsNullOrEmpty(usuario.telefono)
            || String.IsNullOrEmpty(usuario.estado)
            )
            {
                result = true;
            }
            else
            {
                result = false;
            }


            return result;
        }


        public bool update(Usuario usuario)
        {
            bool result = false;
           
            Usuario userSaved = getBycorreo(usuario.correo);
            if (!String.IsNullOrEmpty(usuario.nombre))
                userSaved.nombre = usuario.nombre;
            if (!String.IsNullOrEmpty(usuario.apellido))
                userSaved.apellido = usuario.apellido;
            if (!String.IsNullOrEmpty(usuario.telefono)) 
                userSaved.telefono = usuario.telefono;
            if (!String.IsNullOrEmpty(usuario.estado))
                userSaved.estado = usuario.estado;
            
            _session.Update(userSaved);
            _session.Flush();

            return result;
            
        }
        public string token(string correo)
        {
           
            Usuario usuario = usuarioporcorreo(correo);
            var token = Utils.Utils.generateJWTToken(usuario.id, usuario.nombre, usuario.correo);

            return token;
        }
        public Activacion getUsuarioToken(string token)
        {
            return _session.Query<Activacion>().FirstOrDefault(x => x.Llave == token);
        }
    }
}
