using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PHARMACY_1.PharmacistUC
{
    public partial class UC_P_MediValidCheck : UserControl
    {
        function fn = new function();
        string query;

        public UC_P_MediValidCheck()
        {
            InitializeComponent();
        }

        private void txtcheck_SelectedIndexChanged(object sender, EventArgs e)
        {
            if(txtcheck.SelectedIndex == 0)
            {
                query = "select*from medic where eDate >= getdate()";
                DataSet ds=fn.getdata(query);
                guna2DataGridView1.DataSource = ds.Tables[0];
                set.Text = "Valid Medicines";
                set.ForeColor = Color.Black;

            }
            else if(txtcheck.SelectedIndex == 1)
            {
                query = "select * from medic where eDate <=getdate()";
                DataSet ds = fn.getdata(query);
                guna2DataGridView1.DataSource= ds.Tables[0];
                set.Text = "Expired Medicines";
                set.ForeColor= Color.Red;
            }
            else if(txtcheck.SelectedIndex ==2)
            {
                query = "select * from medic";
                DataSet ds =fn.getdata(query);
                guna2DataGridView1.DataSource = ds.Tables[0];
                set.Text = "All Medicines";
                set.ForeColor= Color.Black;
            }
        }

        private void UC_P_MediValidCheck_Load(object sender, EventArgs e)
        {
            set.Text = "";

        }
    }
}
