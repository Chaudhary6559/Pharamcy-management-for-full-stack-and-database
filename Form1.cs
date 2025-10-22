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
    public partial class Form1 : Form
    {
        function fn = new function();
        string query;
        DataSet ds;
        public Form1()
        {
            InitializeComponent();
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            txtusername.Clear();
            txtpassward.Clear();
        }

        private void button2_Click(object sender, EventArgs e)
        {
           /* Administrator admin = new Administrator();
            admin.Show();
            this.Hide();*/
            query = "select * from users";
             ds = fn.getdata(query);
             if (ds.Tables[0].Rows.Count == 0)
             {
                 if(txtusername.Text=="root"&& txtpassward.Text=="root")
                 {
                     Administrator admin = new Administrator();
                     admin.Show();
                     this.Hide();
                 }
             }
             else
             {
                 query = "select * from users where username ='" + txtusername.Text + "'and pass ='" + txtpassward.Text + "'";
                 ds= fn.getdata(query);
                 if (ds.Tables[0].Rows.Count!= 0)
                 {
                     string role = ds.Tables[0].Rows[0][1].ToString();
                     if (role =="Administrator")
                     {
                         Administrator admin = new Administrator(txtusername.Text);
                         admin.Show();
                         this.Hide();
                     }
                     else if (role =="Pharmacist")
                     {
                         Pharmacist pharm = new Pharmacist();
                         pharm.Show();   
                         this.Hide();    
                     }
                 }
                 else
                {
                    MessageBox.Show("WRONG USERNAME OR PASSWARD","ERROR",MessageBoxButtons.OK,MessageBoxIcon.Error);
                }
             }



        }

        private void btnexit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void button2_Click_1(object sender, EventArgs e)
        {

        }

        private void txtusername_TextChanged(object sender, EventArgs e)
        {

        }

        private void guna2Button1_Click(object sender, EventArgs e)
        {
            Forgot_Passward fg = new Forgot_Passward();
            fg.Show();
        }

        private void guna2Button2_Click(object sender, EventArgs e)
        {
            project_by pb = new project_by();
            pb.Show();
            this.Hide();
        }
    }
}
