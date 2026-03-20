using System;
namespace dosxl.Utils
{
    public class ConfigSMTP
    {
        public virtual bool EnableSSl { get; set; }
        //public virtual bool GoogleAuth { get; set; }
        public virtual string Host { get; set; }
        public virtual string Password { get; set; }
        public virtual int Port { get; set; }
        public virtual int ConfigSMTPID { get; set; }
        public virtual bool UseDefCred { get; set; }
        public virtual string Usuario { get; set; }
    }
}
