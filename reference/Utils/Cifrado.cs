using System;
using System.Security.Cryptography;
using System.Text;

namespace dosxl.Utils
{
    class Cifrado
    {
        public string Llave { get; set; }

        /// <summary>
        /// The Login and the password must be given as concat string
        /// </summary>
        /// <param name="CadenaOriginal">clave</param>
        /// <returns>Base64</returns>
        public string EncriptarSHA1(string login, string passw)
        {
            string CadenaOriginal = login + passw;
            SHA1 _metodo = new SHA1CryptoServiceProvider();
            byte[] inputBytes = (new UnicodeEncoding()).GetBytes(CadenaOriginal);
            byte[] _hash = _metodo.ComputeHash(inputBytes);
            return Convert.ToBase64String(_hash);
        }
    }
}
