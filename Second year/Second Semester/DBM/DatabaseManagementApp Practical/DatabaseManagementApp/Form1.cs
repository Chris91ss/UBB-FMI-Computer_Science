using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;

namespace DatabaseManagementApp
{
    public partial class Form1 : Form
    {
        private string connectionString =
            ConfigurationManager.ConnectionStrings["MyDbConnection"].ConnectionString;

        private SqlConnection conn;
        private SqlDataAdapter daCities, daBakeries;
        private SqlCommandBuilder cbBakeries;
        private DataSet ds;

        private BindingSource bsCities = new BindingSource();
        private BindingSource bsBakeries = new BindingSource();

        public Form1()
        {
            InitializeComponent();
            conn = new SqlConnection(connectionString);
            LoadData();
            SetupDataBinding();
        }

        private void LoadData()
        {
            try
            {
                ds = new DataSet();

                // 1. Load Cities (parent)
                daCities = new SqlDataAdapter("SELECT * FROM Cities", conn);
                daCities.MissingSchemaAction = MissingSchemaAction.AddWithKey;
                daCities.Fill(ds, "Cities");

                // 2. Load FavouriteBakeries (child)
                daBakeries = new SqlDataAdapter("SELECT * FROM FavouriteBakeries", conn);
                daBakeries.MissingSchemaAction = MissingSchemaAction.AddWithKey;

                // Custom InsertCommand
                SqlCommand insertCmd = new SqlCommand(@"
            INSERT INTO FavouriteBakeries (Name, StartupYear, NumberOfStars, CityID)
            VALUES (@Name, @StartupYear, @NumberOfStars, @CityID);
            SELECT CAST(SCOPE_IDENTITY() AS int);", conn);

                insertCmd.Parameters.Add("@Name", SqlDbType.NVarChar, 100, "Name");
                insertCmd.Parameters.Add("@StartupYear", SqlDbType.Int, 0, "StartupYear");
                insertCmd.Parameters.Add("@NumberOfStars", SqlDbType.Int, 0, "NumberOfStars");
                insertCmd.Parameters.Add("@CityID", SqlDbType.Int, 0, "CityID");
                insertCmd.UpdatedRowSource = UpdateRowSource.FirstReturnedRecord;
                daBakeries.InsertCommand = insertCmd;

                cbBakeries = new SqlCommandBuilder(daBakeries);
                daBakeries.UpdateCommand = cbBakeries.GetUpdateCommand();
                daBakeries.DeleteCommand = cbBakeries.GetDeleteCommand();

                daBakeries.Fill(ds, "FavouriteBakeries");

                ds.Tables["FavouriteBakeries"].Columns["BakeryID"].AllowDBNull = true;

                DataRelation rel = new DataRelation("City_Bakeries",
                    ds.Tables["Cities"].Columns["CityID"],
                    ds.Tables["FavouriteBakeries"].Columns["CityID"]);
                ds.Relations.Add(rel);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading data: " + ex.Message);
            }
        }


        private void SetupDataBinding()
        {
            try
            {
                bsCities.DataSource = ds;
                bsCities.DataMember = "Cities";

                bsBakeries.DataSource = bsCities;
                bsBakeries.DataMember = "City_Bakeries";

                dgvCities.DataSource = bsCities;
                dgvFavouriteBakeries.DataSource = bsBakeries;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error setting up data binding: " + ex.Message);
            }
        }

        private void btnAddEmployee_Click(object sender, EventArgs e)
        {
            try
            {
                // Ensure a city is selected
                if (bsCities.Current == null)
                {
                    MessageBox.Show("Please select a city first.");
                    return;
                }

                DataRowView newRowView = (DataRowView)bsBakeries.AddNew();
                newRowView["Name"] = "New Bakery";
                newRowView["StartupYear"] = DateTime.Now.Year;
                newRowView["NumberOfStars"] = 0;
                newRowView["CityID"] = ((DataRowView)bsCities.Current)["CityID"]; 

                bsBakeries.EndEdit();
                MessageBox.Show("New bakery added in-memory. Click 'Update' to save.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error adding new bakery: " + ex.Message);
            }
        }


        private void btnDeleteEmployee_Click(object sender, EventArgs e)
        {
            try
            {
                if (bsBakeries.Current != null)
                {
                    bsBakeries.RemoveCurrent();
                    MessageBox.Show("Bakery removed in-memory. Click 'Update' to finalize.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error deleting bakery: " + ex.Message);
            }
        }

        private void btnUpdateEmployees_Click(object sender, EventArgs e)
        {
            try
            {
                bsBakeries.EndEdit();
                daBakeries.Update(ds, "FavouriteBakeries");
                MessageBox.Show("Bakeries updated successfully!");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error updating bakeries: " + ex.Message);
            }
        }
    }
}
