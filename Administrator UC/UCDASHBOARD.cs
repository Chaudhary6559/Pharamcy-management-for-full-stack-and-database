using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PHARMACY_1.Administrator_UC
{
    public partial class UCDASHBOARD : UserControl
    {
        function fn = new function();
        string query;
        DataSet ds;

        public UCDASHBOARD()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void UCDASHBOARD_Load(object sender, EventArgs e)
        {
            query = "select count(userRole) from users where userRole ='Administrator'";
            ds = fn.getdata(query);
            setLabel(ds, Adminlabel);
            query = "select count(userRole) from users where userRole ='Pharmacist'";
            ds = fn.getdata(query);
            setLabel(ds, Pharlabel);
        }
        private void setLabel(DataSet ds,Label lbl) 
        {
            if (ds.Tables[0].Rows.Count != 0)
            {
                lbl.Text = ds.Tables[0].Rows[0][0].ToString();
            }
            else
            {
                lbl.Text = "0";
            }
        }

        private void btnsync_Click(object sender, EventArgs e)
        {
            UCDASHBOARD_Load(this, null);
        }
    }

}
