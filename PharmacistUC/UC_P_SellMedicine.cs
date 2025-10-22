using DGVPrinterHelper;
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
    public partial class UC_P_SellMedicine : UserControl
    {
        function fn = new function();
        string query;
        DataSet ds;

        public UC_P_SellMedicine()
        {
            InitializeComponent();
        }

        private void UC_P_SellMedicine_Load(object sender, EventArgs e)
        {
            listBoxMedicines.Items.Clear();
            query = "select mname from medic where eDate >= getdate() and quantity > 0";
            ds=fn.getdata(query);

            for(int i = 0; i < ds.Tables[0].Rows.Count;i++) 
            {
                listBoxMedicines.Items.Add(ds.Tables[0].Rows[i][0].ToString());
            }
        }

        private void btnsync_Click(object sender, EventArgs e)
        {
            UC_P_SellMedicine_Load(this, null);
        }

        private void txtSearchBox_TextChanged(object sender, EventArgs e)
        {
            listBoxMedicines.Items.Clear();
            query = "select mname from medic where mname like '" + txtSearchBox.Text + "%' and eDate >= getdate() and quantity > 0";
            ds = fn.getdata(query);
            for(int i = 0; i < ds.Tables[0].Rows.Count; i++)
            {
                listBoxMedicines.Items.Add(ds.Tables[0].Rows[i][0].ToString());
            }
        }

        private void listBoxMedicines_SelectedIndexChanged(object sender, EventArgs e)
        {
            txtnoofUnits.Clear();
            string name=listBoxMedicines.GetItemText(listBoxMedicines.SelectedItem);
            txtMedicineName.Text= name;
            query = "select mid,eDate,Perunit from medic where mname ='" + name + "'";
            ds=fn.getdata(query);
            txtMedicineID.Text = ds.Tables[0].Rows[0][0].ToString();
            txtExpDate.Text = ds.Tables[0].Rows[0][1].ToString();
            TxtpriceperUnit.Text = ds.Tables[0].Rows[0][2].ToString();

        }

        private void txtnoofUnits_TextChanged(object sender, EventArgs e)
        {
            if (txtnoofUnits.Text != "")
            {
                Int64 unitprice =Int64.Parse(TxtpriceperUnit.Text);
                Int64 noofunits = Int64.Parse(txtnoofUnits.Text);
                Int64 totalAmount = unitprice * noofunits;
                txtTotalPrice.Text = totalAmount.ToString();
            }
            else
            {
                txtTotalPrice.Clear();

            }
        }
        protected int n, totalAmount = 0;
        protected Int64 quantity, newQuantity;


        private void btnAddToCart_Click(object sender, EventArgs e)
        {
            if (txtMedicineID.Text != "")
            {
                query ="select quantity from medic where mid ='"+txtMedicineID.Text+"'";
                ds=fn.getdata(query);
                quantity = Int64.Parse(ds.Tables[0].Rows[0][0].ToString());
                newQuantity = quantity - Int64.Parse(txtnoofUnits.Text);
                if (newQuantity >= 0)
                {
                    n= guna2DataGridView1.Rows.Add();
                    guna2DataGridView1.Rows[n].Cells[0].Value = txtMedicineID.Text;
                    guna2DataGridView1.Rows[n].Cells[1].Value = txtMedicineName.Text;
                    guna2DataGridView1.Rows[n].Cells[2].Value =txtExpDate.Text;
                    guna2DataGridView1.Rows[n].Cells[3].Value =TxtpriceperUnit.Text;
                    guna2DataGridView1.Rows[n].Cells[4].Value = txtnoofUnits.Text;
                    guna2DataGridView1.Rows[n].Cells[5].Value =txtTotalPrice.Text;

                    totalAmount=totalAmount + int.Parse(txtTotalPrice.Text);
                    totalLabel.Text = "RS."+totalAmount.ToString();

                    query="update medic set quantity='"+newQuantity+"' where mid ='"+txtMedicineID.Text+"'";
                    fn.setData(query,"Medicine Added");
                }
                else
                {
                    MessageBox.Show("Medicine is Out of Stock.\n Only'" + quantity + "' Left", "Warning!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                clearAll();
                UC_P_SellMedicine_Load(this, null);

            }
            else
            {
                MessageBox.Show("Select Medicine First","INFORMATION !",MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            
        }
        int valueAmount;
        string valueid;
        protected Int64 noofUnits;


        private void guna2DataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                valueAmount = int.Parse(guna2DataGridView1.Rows[e.RowIndex].Cells[5].Value.ToString());
                valueid = guna2DataGridView1.Rows[e.RowIndex].Cells[0].Value.ToString();
                noofUnits = Int64.Parse(guna2DataGridView1.Rows[e.RowIndex].Cells[4].Value.ToString());
            }catch(Exception)
            {
                
            }

        }

       

        private void btnRemove_Click(object sender, EventArgs e)
        {
            if(valueid!=null)
            {
                try
                {
                    guna2DataGridView1.Rows.RemoveAt(this.guna2DataGridView1.SelectedRows[0].Index);
                }
                catch
                {

                }
                finally
                {
                    query = "select quantity from medic where mid = '" + valueid + "'";
                    ds = fn.getdata(query);
                    quantity = Int64.Parse(ds.Tables[0].Rows[0][0].ToString());
                    newQuantity = quantity + noofUnits;
                    query = "update medic set quantity ='" + newQuantity + "' where mid ='"+valueid+"'";
                    fn.setData(query, "Medicine Removed From The Cart.");
                    totalAmount = totalAmount - valueAmount;
                    totalLabel.Text = "RS." + totalAmount.ToString();

                }
                UC_P_SellMedicine_Load(this, null);
            }
        }

        private void guna2DataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void txtMedicineID_TextChanged(object sender, EventArgs e)
        {

        }

        private void btnpurchasePrint_Click(object sender, EventArgs e)
        {
            DGVPrinter print = new DVGPrinter();
            print.Title = " Medicine Bill";
            print.SubTitle = string.Format("Date:-{0}",DateTime.Now.Date);
            print.SubTitleFormatFlags = StringFormatFlags.LineLimit | StringFormatFlags.NoClip;
            print.PageNumbers = true;
            print.PageNumberInHeader = false;
            print.PorportionalColumns = true;
            print.HeaderCellAlignment = StringAlignment.Near;
            print.Footer="Total Payable Amount:"+totalLabel.Text;
            print.FooterSpacing = 15;
            print.PrintDataGridView(guna2DataGridView1);
            totalAmount = 0;
            totalLabel.Text = "RS.00";
            guna2DataGridView1.DataSource = null;
            guna2DataGridView1.Rows.Clear();


        }

        private void clearAll()
        {
            txtMedicineID.Clear();
            txtMedicineName.Clear();
            txtExpDate.ResetText();
            TxtpriceperUnit.Clear();
            txtnoofUnits.Clear();

        }
      
    }
}
