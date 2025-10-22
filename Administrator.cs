using PHARMACY_1.Administrator_UC;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PHARMACY_1
{
    public partial class Administrator : Form
    {
        string user = "";
        public Administrator()
        {
            InitializeComponent();
        }
        public string ID
        { 
            get { return user.ToString(); }
        }
        public Administrator(string username)
        {
            InitializeComponent();
            userNAMELabel.Text = username;
            user = username;
            uC_ViewUser1.ID = ID;
            uC_Profile1.ID=ID;
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void panel2_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void btndashboard_Click(object sender, EventArgs e)
        {
            ucdashboard1.Visible = true;
            ucdashboard1.BringToFront();
        }

        private void guna2Button5_Click(object sender, EventArgs e)
        {
            Form1 fm = new Form1();
            fm.ShowDialog();
            this.Hide();
        }

        private void Administrator_Load(object sender, EventArgs e)
        {
            ucdashboard1.Visible=false;
            ucadduser1.Visible=false;
            uC_ViewUser1.Visible=false;
            uC_Profile1.Visible=false;
            btndashboard.PerformClick();



        }

        private void dtnadduser_Click(object sender, EventArgs e)
        {
            ucadduser1.Visible = true;  
            ucadduser1.BringToFront();  
        }

        private void ucadduser1_Load(object sender, EventArgs e)
        {

        }

        private void btnViewUser_Click(object sender, EventArgs e)
        {
            uC_ViewUser1.Visible = true;
            uC_ViewUser1.BringToFront();
        }

        private void btnProfile_Click(object sender, EventArgs e)
        {
            uC_Profile1.Visible = true;
            uC_Profile1.BringToFront();

        }
    }
}
