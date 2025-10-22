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
    public partial class UC_P_ViewMedicine : UserControl
    {
        function fn = new function();
        string query;

        public UC_P_ViewMedicine()
        {
            InitializeComponent();
        }

        private void UC_P_ViewMedicine_Load(object sender, EventArgs e)
        {
            query = "select * from medic";
            setDataGridView(query);
        }

        private void txtsearch_TextChanged(object sender, EventArgs e)
        {
            query = "select * from medic where mname like '"+txtsearch.Text+"%'";
            setDataGridView(query);
        }
        private void setDataGridView(string query)
        {
            DataSet ds = fn.getdata(query);
            guna2DataGridView1.DataSource = ds.Tables[0];
        }
        string medicineId;
        private void guna2DataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                medicineId = guna2DataGridView1.Rows[e.RowIndex].Cells[1].Value.ToString();
            }
            catch 
            {

            }
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            if (MessageBox.Show("Are You Sure?", "Delete Conformation!", MessageBoxButtons.YesNo, MessageBoxIcon.Warning) == DialogResult.Yes)
            {
                query="delete from medic where mid = '"+medicineId+"'";
                fn.setData(query, "Medicine Records Deleted");
                UC_P_ViewMedicine_Load(this, null);
            }
        }

        private void btnsync_Click(object sender, EventArgs e)
        {
            UC_P_ViewMedicine_Load(this,null);
        }
    }
}
