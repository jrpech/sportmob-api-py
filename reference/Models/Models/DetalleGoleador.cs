using System;

namespace dosxl.Models.Models
{
    public class DetalleGoleador
    {
        public virtual int ID { set; get; }

        public virtual string nombre { set; get; }

        public virtual string apellido { set; get; }

        public virtual string fechaNacimiento { set; get; }

        public virtual double peso { set; get; }

        public virtual double altura { set; get; }

        public virtual string email { set; get; }

        public virtual string telefono { set; get; }

        public virtual string posicion { set; get; }

        public virtual string talla { set; get; }

        public virtual int noJugador { set; get; }

        public virtual string nombreJersy { set; get; }

        public virtual string foto { set; get; }

        public virtual int equipoID { set; get; }

        public virtual bool estado { set; get; }

        public virtual int codigoPostal { set; get; }

        public virtual DateTime fechaRegistro { set; get; }

        public virtual string nombreEquipo { set; get; }
       
        public virtual string logo { set; get; }

        public virtual int goles { set; get; }


        public object response (Jugador jugador , string nombreequipo, string logoequipo , int goles)
        {
            DetalleGoleador detalle = new DetalleGoleador();

            detalle.ID = jugador.id;
            detalle.nombre = jugador.nombre;
            detalle.apellido = jugador.apellido;
            detalle.fechaNacimiento = jugador.fechaNacimiento;
            detalle.peso = jugador.peso;
            detalle.altura = jugador.altura;
            detalle.email = jugador.email;
            detalle.telefono = jugador.telefono;
            detalle.posicion = jugador.posicion;
            detalle.talla = jugador.talla;
            detalle.noJugador = jugador.noJugador;
            detalle.nombreJersy = jugador.nombreJersy;
            detalle.foto = jugador.foto;
            detalle.equipoID = jugador.equipoID;
            detalle.estado = jugador.estado;
            detalle.codigoPostal = jugador.codigoPostal;
            detalle.fechaRegistro = jugador.fechaRegistro;
            detalle.nombreEquipo = nombreequipo;
            detalle.logo = logoequipo;
            detalle.goles = goles;

            return detalle;

        }

    }
}
