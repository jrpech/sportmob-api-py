using dosxl.Utils;
using FluentNHibernate.Conventions;
using NHibernate.Criterion;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace dosxl.Models.Repository
{
    public class JugadorRepository : RepositoryBase<Jugador>
    {
        public Jugador getById(int id)
        {
            return _session.Query<Jugador>().Where(x =>
                      x.id == id).FirstOrDefault();
        }
        public Jugador getbyCapitanEquipo(int id)
        {
            return _session.Query<Jugador>().Where(x =>
                      x.equipoID == id && x.esCapitan == true).FirstOrDefault();
        }
        public List<Jugador> getAll()
        {
            return _session.Query<Jugador>().ToList();
        }

        public bool noJugadorValido( int equipoID,int noJugador)
        {
            Jugador jugadorUsandoNumero = _session.Query<Jugador>().Where(x => x.noJugador == noJugador && x.equipoID == equipoID).FirstOrDefault();

            if(jugadorUsandoNumero != null)
            {
                throw new Exception("El numero de playera " + noJugador +" lo tiene "+ jugadorUsandoNumero.nombreJersy );
            }

            return true;
        }

        public Jugador ultimoid()
        {
            var lastID = _session.CreateCriteria(typeof(Jugador))
                .SetProjection(Projections.Max("id")).UniqueResult();
            int idjugador = int.Parse(lastID.ToString());

            return _session.Query<Jugador>().Where(x => x.id == idjugador).FirstOrDefault();
        }

        public bool save(Jugador jugador)
        {
            bool result = false;
            JugadorRepository ljugador = new JugadorRepository();

            var lastID = _session.CreateCriteria(typeof(Jugador))
                .SetProjection(Projections.Max("id")).UniqueResult();

            if (jugador.id == 0)
            {
                noJugadorValido(jugador.equipoID,jugador.noJugador);

                if (lastID == null)
                    jugador.id = 1;
                else
                    jugador.id = int.Parse(lastID.ToString()) + 1;

                jugador.foto = ljugador.SaveImageBase64(jugador.foto, jugador.id, "FotoJugador_");
                _session.Save(jugador);
                _session.Flush();
            }
            else
            {
                Jugador jugadorSaved = getById(jugador.id);
                jugadorSaved.nombre = jugador.nombre;
                jugadorSaved.apellido = jugador.apellido;
                jugadorSaved.fechaNacimiento = jugador.fechaNacimiento;
                jugadorSaved.peso = jugador.peso;
                jugadorSaved.altura = jugador.altura;
                jugadorSaved.email = jugador.email;
                jugadorSaved.telefono = jugador.telefono;
                jugadorSaved.posicion = jugador.posicion;
                jugadorSaved.talla = jugador.talla;
                jugadorSaved.noJugador = jugador.noJugador;
                jugadorSaved.nombreJersy = jugador.nombreJersy;
                jugadorSaved.equipoID = jugador.equipoID;
                if(jugador.foto.IsNotEmpty())
                 jugadorSaved.foto = ljugador.SaveImageBase64(jugador.foto, jugador.id, "FotoJugador_");
                jugadorSaved.codigoPostal = jugador.codigoPostal;

                _session.Update(jugadorSaved);
                _session.Flush();
                result = true;

            }

            return result;
        }
        
        public List<Jugador> getPorjugador(int equipoID)
        {
            return _session.Query<Jugador>().Where(
                   x => x.equipoID == equipoID && x.estado == false).OrderBy(x=> x.noJugador).ToList();
        }
       
        public bool elminar(int id)
        {
            bool result = false;

            Jugador jugadorDelet = getById(id);
            jugadorDelet.estado = true;
            _session.SaveOrUpdate(jugadorDelet);
            _session.Flush();

            return result;
        }
        public string SaveImageBase64(string base64img, int id, string texto)
        {

            string _Success = "";
            try
            {
                var folderName = Path.Combine("Resources", "images");
                var folderPath = Path.Combine(Directory.GetCurrentDirectory(), folderName);
                if (!System.IO.Directory.Exists(folderPath))
                {
                    System.IO.Directory.CreateDirectory(folderPath);
                }
                //crear nombre de la imagen
                string imageName = texto + id + ".png";
                System.IO.File.WriteAllBytes(Path.Combine(folderPath, imageName), Convert.FromBase64String(base64img));
                string dirrecion = imageName;
                _Success = dirrecion;

            }
            catch (Exception ex)
            {
                _Success = "Error: " + ex.Message;
            }
            return _Success;
        }
    }
}
