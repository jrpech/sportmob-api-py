using System;
using FluentNHibernate.Cfg;
using Microsoft.Extensions.Configuration;
using NHibernate;
using NHibernate.Cache;

namespace dosxl.Utils
{
    public class ConnectionHelper
    {
        private static IConfiguration _config;
        private static object syncRoot = new Object();
        private static volatile ISessionFactory iSessionFactory;

        public static ISession GetConnection<T>(string Server, string DataBase, string Usuario, string Password)
        {
            _config = Utils.getConfiguration();

            string _connection_provider = string.Empty;
            string _dialect = string.Empty;
            string _connection_driver = string.Empty;
            string _connection_connection_string = "Server=[SERVER];DataBase=[DATABASE];uid=[USER];pwd=[PASSWORD]";
            string _show_sql = "false";
            string _showSql = string.Empty;
            string _generateStatistics = string.Empty;
            NHibernate.Cfg.Configuration nhibernateConfig = new NHibernate.Cfg.Configuration();

            _connection_connection_string = _connection_connection_string.Replace("[SERVER]", Server);
            _connection_connection_string = _connection_connection_string.Replace("[DATABASE]", DataBase);
            _connection_connection_string = _connection_connection_string.Replace("[USER]", Usuario);
            _connection_connection_string = _connection_connection_string.Replace("[PASSWORD]", Password);

            _dialect = _config["Db:dialect"];
            _connection_driver = _config["Db:connectionDriver"];
            _showSql = _config["Db:showSql"];
            _generateStatistics = _config["Db:generateStatistics"];

            if (!string.IsNullOrEmpty(_showSql))
                _show_sql = _showSql;

            if (string.IsNullOrEmpty(_generateStatistics))
                _generateStatistics = "false";



            if (string.IsNullOrEmpty(_dialect))
            {
                throw new Exception("The dialect has not been established");
            }

            nhibernateConfig.Properties[NHibernate.Cfg.Environment.Dialect] = _dialect;
            nhibernateConfig.Properties[NHibernate.Cfg.Environment.ConnectionString] = _connection_connection_string;
            nhibernateConfig.Properties[NHibernate.Cfg.Environment.GenerateStatistics] = _generateStatistics;
            nhibernateConfig.Properties[NHibernate.Cfg.Environment.ShowSql] = _show_sql;

            if (iSessionFactory == null)
            {
                lock (syncRoot)
                {
                    if (iSessionFactory == null)
                    {
                        iSessionFactory = Fluently.Configure(nhibernateConfig)
                            .Cache(c => c.UseQueryCache().ProviderClass<HashtableCacheProvider>())
                            .Mappings(m => m.FluentMappings.AddFromAssemblyOf<T>())
                            .BuildConfiguration()
                            .BuildSessionFactory();
                    }
                }
            }

            return iSessionFactory.OpenSession();
        }

    }
}
