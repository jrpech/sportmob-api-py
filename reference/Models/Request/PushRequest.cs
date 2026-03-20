using System;
namespace dosxl.Models.Request
{
    public class PushRequest
    {
        public virtual Notification notification { get; set; }
        public virtual string to { get; set; }

        public PushRequest()
        {
            notification = new Notification();
        }
    }

    public class Notification
    {
        public virtual string body { get; set; }
        public virtual string icon { get; set; }
        public virtual string title { get; set; }
        public virtual string id { get; set; }
    }
}
