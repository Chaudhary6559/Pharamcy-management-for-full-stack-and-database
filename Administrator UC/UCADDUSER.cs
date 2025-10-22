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
    public partial class UCADDUSER : UserControl
    {
        function fn = new function();
        String query;
        
        public UCADDUSER()
        {
            InitializeComponent();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void UCADDUSER_Load(object sender, EventArgs e)
        {

        }

        private void txtsignup_Click(object sender, EventArgs e)
        {
            String role = txtuserrole.Text;
            String name = txtusername.Text;
            String dob = txtDOB.Text;
            Int64 mobile = Int64.Parse(txtmobilenumber.Text);
            String Email = txtemail.Text;
            String Username = txtusername.Text;
            String Passward = txtpassward.Text;

            try
            {
                query = "insert into users(userRole,name,dob,mobile,email,username,pass)values('"+role+"','"+name+"','"+dob+"','"+mobile+"','"+Email+"','"+Username+"','"+Passward+"')";
                fn.setData(query, "Sign Up Successful");
            }
            catch(Exception)
            {
                MessageBox.Show("Username Already Exists","Error",MessageBoxButtons.OK,MessageBoxIcon.Error);
            }
        }

        private void btnreset_Click(object sender, EventArgs e)
        { 
        
            txtname.Clear();
            txtDOB.ResetText();
            txtmobilenumber.Clear();
            txtemail.Clear();
            txtusername.Clear();    
            txtpassward.Clear();
            txtuserrole.SelectedIndex = -1;
        }

        private void txtusername_TextChanged(object sender, EventArgs e)
        {
            query = "select * from users where username='" + txtusername.Text + "'";
            DataSet ds = fn.getdata(query);
            if (ds.Tables[0].Rows.Count==0)
            {
                pictureBox1.ImageLocation = @"D:\\C# Pharmacy Management System\\Pharmacy Management System in C#\\DS\yes.png";
            }
            else
            {
                pictureBox1.ImageLocation = @"D:\\C# Pharmacy Management System\\Pharmacy Management System in C#\\DS\no.png";
            }
        }
    }
}
