using System;
namespace dosxl.Models.Response
{
    public class BaseResponse
    {


        public virtual string respuesta { get; set; }
        public virtual string mensaje { get; set; }
        public virtual object data { get; set; }

        public BaseResponse()
        {
            respuesta = "error";
            mensaje = "Mensaje de error inicial";
          
        }
    }
}
