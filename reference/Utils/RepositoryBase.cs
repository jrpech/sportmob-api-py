using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using Microsoft.Extensions.Configuration;
using NHibernate;

namespace dosxl.Utils
{
	public abstract class RepositoryBase<T>
	{
		public ISession _session;
		private IConfiguration _config;

		protected bool _exito;
		protected List<string> _errores;
		protected List<string> _mensajes;

		public bool Exito
		{
			get
			{
				return this._exito;
			}
		}

		public List<string> Errores
		{
			get
			{
				if (this._errores == null)
				{
					this._errores = new List<string>();
				}
				return this._errores;
			}
		}
		public List<string> Mensajes
		{
			get
			{
				if (this._mensajes == null)
				{
					this._mensajes = new List<string>();
				}
				return this._mensajes;
			}
			set
			{
				this._mensajes = value;
			}
		}

		public RepositoryBase()
		{
			try
			{
				this.Errores.Clear();
				this.Mensajes.Clear();
				if (_session == null || !_session.IsOpen)
					this._session = this.createContext(_session);
				this._exito = true;

			}
			catch (Exception innerException)
			{
				while (innerException.InnerException != null)
				{
					innerException = innerException.InnerException;
				}
				this.Errores.Add(innerException.Message);
				throw innerException;
			}
		}

		private ISession createContext(ISession Session)
		{
			ISession oSession;

			string server = string.Empty;
			string dataBase = string.Empty;
			string usuario = string.Empty;
			string password = string.Empty;

			_config = Utils.getConfiguration();

			server = _config["Db:server"];
			dataBase = _config["Db:dataBase"];
			usuario = _config["Db:usuario"];
			password = _config["Db:password"];

			if (string.IsNullOrEmpty(server) || string.IsNullOrEmpty(dataBase) || string.IsNullOrEmpty(usuario) || string.IsNullOrEmpty(password))
			{
				throw new Exception("Un valor de la cadena de conexión no está correctamente configurado");
			}

			oSession = ConnectionHelper.GetConnection<T>(server, dataBase, usuario, password);

			return oSession;
		}
	}
}
