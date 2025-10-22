using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace PHARMACY_1
{
    internal class function
    {
        protected SqlConnection getConnection()
        {
            SqlConnection con = new SqlConnection();
            con.ConnectionString = "data source = DESKTOP-LRSCS9D;database=DBMSPHARMA;integrated security=True";
            return con;    
        }
        public DataSet getdata(String query)

        {
            SqlConnection con = getConnection();    
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = con;
            cmd.CommandText = query;
            SqlDataAdapter da = new SqlDataAdapter(cmd);
            DataSet ds = new DataSet();
            da.Fill(ds);    
            return ds;
        }
        public void setData(String query,String msg)
        {
            SqlConnection con = getConnection(); 
            SqlCommand cmd = new SqlCommand();
            cmd.Connection = con;
            con.Open();
            cmd.CommandText = query;
            cmd.ExecuteNonQuery();
            con.Close();
            MessageBox.Show(msg,"information",MessageBoxButtons.OK,MessageBoxIcon.Information);   

        }
    }
}
