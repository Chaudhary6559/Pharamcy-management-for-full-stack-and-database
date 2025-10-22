using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Configuration;
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
            string connectionString = ConfigurationManager.ConnectionStrings["PharmacyDb"]?.ConnectionString;
            if (string.IsNullOrWhiteSpace(connectionString))
            {
                throw new InvalidOperationException("Missing connection string 'PharmacyDb' in App.config.");
            }
            SqlConnection con = new SqlConnection(connectionString);
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
