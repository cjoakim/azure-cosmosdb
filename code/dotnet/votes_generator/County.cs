using System;

namespace votes_generator
{

    public class County
    {
        public string state      { get; set; }
        public string name       { get; set; }
        public int    population { get; set; }
        public double statePct   { get; set; }
        public double rangeMin   { get; set; }
        public double rangeMax   { get; set; }

        public County()
        {
           
        }
    }
}