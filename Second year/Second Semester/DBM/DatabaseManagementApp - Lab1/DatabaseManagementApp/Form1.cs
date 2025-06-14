using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;

namespace DatabaseManagementApp
{
    public partial class Form1 : Form
    {
        // Connection string from App.config
        private string connectionString =
            ConfigurationManager.ConnectionStrings["MyDbConnection"].ConnectionString;

        // ADO.NET objects
        private SqlConnection conn;
        private SqlDataAdapter daDealerships, daEmployees;
        private SqlCommandBuilder cbEmployees;
        private DataSet ds;

        // BindingSource objects to link each grid
        private BindingSource bsDealerships = new BindingSource();
        private BindingSource bsEmployees = new BindingSource();

        public Form1()
        {
            InitializeComponent();
            conn = new SqlConnection(connectionString);
            LoadData();
            SetupDataBinding();
        }

        /// <summary>
        /// Loads data from both Dealerships and Employees into a DataSet,
        /// creates a DataRelation, and ensures the primary keys are recognized.
        /// Also sets up a custom InsertCommand for Employees to retrieve the generated identity.
        /// </summary>
        private void LoadData()
        {
            try
            {
                ds = new DataSet();

                // 1) Dealerships (Parent)
                daDealerships = new SqlDataAdapter("SELECT * FROM Dealerships", conn);
                daDealerships.MissingSchemaAction = MissingSchemaAction.AddWithKey;
                daDealerships.Fill(ds, "Dealerships");

                // 2) Employees (Child)
                daEmployees = new SqlDataAdapter("SELECT * FROM Employees", conn);
                daEmployees.MissingSchemaAction = MissingSchemaAction.AddWithKey;

                // Auto-generate UPDATE/DELETE via SqlCommandBuilder
                cbEmployees = new SqlCommandBuilder(daEmployees);

                // Custom InsertCommand to retrieve identity via SCOPE_IDENTITY()
                SqlCommand insertCmd = new SqlCommand(@"
                    INSERT INTO Employees (FirstName, LastName, Position, Salary, DealershipID)
                    VALUES (@FirstName, @LastName, @Position, @Salary, @DealershipID);
                    SELECT CAST(SCOPE_IDENTITY() AS int);", conn);

                insertCmd.Parameters.Add("@FirstName", SqlDbType.NVarChar, 50, "FirstName");
                insertCmd.Parameters.Add("@LastName", SqlDbType.NVarChar, 50, "LastName");
                insertCmd.Parameters.Add("@Position", SqlDbType.NVarChar, 50, "Position");
                insertCmd.Parameters.Add("@Salary", SqlDbType.Decimal, 0, "Salary");
                insertCmd.Parameters.Add("@DealershipID", SqlDbType.Int, 0, "DealershipID");

                // Tell ADO.NET to apply the returned identity to the DataRow
                insertCmd.UpdatedRowSource = UpdateRowSource.FirstReturnedRecord;
                daEmployees.InsertCommand = insertCmd;

                // Fill the Employees table
                daEmployees.Fill(ds, "Employees");

                // Allow EmployeeID to be null in the DataSet so we can add a row without providing it
                ds.Tables["Employees"].Columns["EmployeeID"].AllowDBNull = true;

                // 3) Create DataRelation (Dealerships -> Employees)
                DataRelation relation = new DataRelation("Dealership_Employees",
                    ds.Tables["Dealerships"].Columns["DealershipID"],
                    ds.Tables["Employees"].Columns["DealershipID"]);
                ds.Relations.Add(relation);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading data: " + ex.Message);
            }
        }

        /// <summary>
        /// Binds the DataSet tables to two BindingSource objects,
        /// then assigns those BindingSources to the two DataGridViews.
        /// </summary>
        private void SetupDataBinding()
        {
            try
            {
                // Parent: Dealerships
                bsDealerships.DataSource = ds;
                bsDealerships.DataMember = "Dealerships";

                // Child: Employees (filtered via the DataRelation)
                bsEmployees.DataSource = bsDealerships;
                bsEmployees.DataMember = "Dealership_Employees";

                // Assign to the DataGridViews
                dataGridViewDealerships.DataSource = bsDealerships;
                dataGridViewEmployees.DataSource = bsEmployees;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error setting up data binding: " + ex.Message);
            }
        }

        /// <summary>
        /// Adds a new (in-memory) Employee row for the currently selected Dealership.
        /// User must click "Update Employees" to commit changes to DB.
        /// </summary>
        private void btnAddEmployee_Click(object sender, EventArgs e)
        {
            try
            {
                // Create a new row in the child BindingSource.
                DataRowView newRowView = (DataRowView)bsEmployees.AddNew();

                // Provide some defaults
                newRowView["FirstName"] = "New";
                newRowView["LastName"] = "Employee";
                newRowView["Position"] = "Position";
                newRowView["Salary"] = 0;
                // Link to the current Dealership
                newRowView["DealershipID"] = ((DataRowView)bsDealerships.Current)["DealershipID"];

                // Finalize
                bsEmployees.EndEdit();
                MessageBox.Show("New employee added in-memory. Click 'Update Employees' to save.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error adding new employee: " + ex.Message);
            }
        }

        /// <summary>
        /// Deletes the currently selected Employee from the DataSet (in-memory).
        /// User must click "Update Employees" to finalize deletion in the DB.
        /// </summary>
        private void btnDeleteEmployee_Click(object sender, EventArgs e)
        {
            try
            {
                if (bsEmployees.Current != null)
                {
                    bsEmployees.RemoveCurrent();
                    MessageBox.Show("Employee removed in-memory. Click 'Update Employees' to finalize.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error deleting employee: " + ex.Message);
            }
        }

        /// <summary>
        /// Commits any (Add, Update, Delete) changes to the DB.
        /// </summary>
        private void btnUpdateEmployees_Click(object sender, EventArgs e)
        {
            try
            {
                bsEmployees.EndEdit();
                daEmployees.Update(ds, "Employees");
                MessageBox.Show("Employees updated successfully!");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error updating employees: " + ex.Message);
            }
        }
    }
}
