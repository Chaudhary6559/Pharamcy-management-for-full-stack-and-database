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
    public partial class UC_P_AddMedicine : UserControl
    {
        function fn = new function();
        string query;

        public UC_P_AddMedicine()
        {
            InitializeComponent();
        }

        private void btnADD_Click(object sender, EventArgs e)
        {
            if(txtMediID.Text!=""&&txtMediName.Text!=""&&txtMediNumber.Text!=""&&txtquantity.Text!=""&&txtPricePerUnit.Text!="")
            {
                string mid =txtMediID.Text;
                string mname=txtMediName.Text;
                string mnumber = txtMediNumber.Text;
                string mdate = txtManifacturingDate.Text;   
                string edate = txtExpireDate.Text;  
                Int64 quantity=Int64.Parse(txtquantity.Text);
                Int64 Perunit = Int64.Parse(txtPricePerUnit.Text);

                query = "insert into medic (mid,mname,mnumber,mDate,eDate,quantity,Perunit)values ('"+mid+ "','"+mname+ "','"+mnumber+ "','"+mdate+ "','"+edate+ "','"+quantity+ "','"+Perunit+"')";
                fn.setData(query, "Medicine Added To Database");
            }
            else
            {
                MessageBox.Show("Enter all Data","Information",MessageBoxButtons.OK,MessageBoxIcon.Warning);
            }
        }

        private void btnReset_Click(object sender, EventArgs e)
        {
            clearAll();
        }
        public void clearAll()
        {
            txtMediID.Clear();
            txtMediName.Clear();
            txtMediNumber.Clear();
            txtManifacturingDate.ResetText();
            txtExpireDate.ResetText();
            txtquantity.Clear();
            txtPricePerUnit.Clear();
        }

        private void UC_P_AddMedicine_Load(object sender, EventArgs e)
        {

        }
    }
}
