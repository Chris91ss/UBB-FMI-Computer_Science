using System;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;

namespace DatabaseManagementApp
{
    public partial class Form1 : Form
    {
        // Read the database connection string from App.config.
        private string connectionString = ConfigurationManager.ConnectionStrings["MyDbConnection"].ConnectionString;
        private SqlConnection conn;

        // Core ADO.NET objects.
        private SqlDataAdapter daParent, daChild;
        private SqlCommandBuilder cbChild;
        private DataSet ds;

        // BindingSources to serve as data bridges.
        private BindingSource bsParent = new BindingSource();
        private BindingSource bsChild = new BindingSource();

        // Configuration-based values.
        private string parentQuery;
        private string childQuery;
        private string parentKey;
        private string childForeignKey;

        // Dynamically created UI controls.
        private DataGridView dgvParent;
        private DataGridView dgvChild;
        private Button btnAddChild;
        private Button btnDeleteChild;
        private Button btnUpdateChild;

        public Form1()
        {
            // Load scenario settings from configuration.
            string scenario = ConfigurationManager.AppSettings["CurrentScenario"];
            string caption = ConfigurationManager.AppSettings[scenario + ".Caption"];
            parentQuery = ConfigurationManager.AppSettings[scenario + ".ParentQuery"];
            childQuery = ConfigurationManager.AppSettings[scenario + ".ChildQuery"];
            parentKey = ConfigurationManager.AppSettings[scenario + ".ParentKey"];
            childForeignKey = ConfigurationManager.AppSettings[scenario + ".ChildForeignKey"];

            // Set form properties dynamically.
            this.Text = caption;
            this.Width = 800;
            this.Height = 600;

            conn = new SqlConnection(connectionString);

            // Dynamically create and arrange the UI controls.
            InitializeControls();

            // Load data into the DataSet.
            LoadData();

            // Bind the DataSet tables to the grid controls.
            SetupDataBinding();
        }

        /// <summary>
        /// Creates and adds the DataGridViews and buttons to the form.
        /// </summary>
        private void InitializeControls()
        {
            // Parent grid for the master table.
            dgvParent = new DataGridView
            {
                Dock = DockStyle.Top,
                Height = 250,
                ReadOnly = true,
                AutoGenerateColumns = true
            };

            // Child grid for the detail table.
            dgvChild = new DataGridView
            {
                Dock = DockStyle.Top,
                Height = 250,
                ReadOnly = false,
                AutoGenerateColumns = true
            };

            // Create buttons for performing data operations.
            btnAddChild = new Button { Text = "Add Child", Left = 10, Top = 520, Width = 100 };
            btnDeleteChild = new Button { Text = "Delete Child", Left = 120, Top = 520, Width = 100 };
            btnUpdateChild = new Button { Text = "Update Child", Left = 230, Top = 520, Width = 100 };

            // Attach event handlers for the button click events.
            btnAddChild.Click += BtnAddChild_Click;
            btnDeleteChild.Click += BtnDeleteChild_Click;
            btnUpdateChild.Click += BtnUpdateChild_Click;

            // Add the controls to the form.
            this.Controls.Add(dgvParent);
            this.Controls.Add(dgvChild);
            this.Controls.Add(btnAddChild);
            this.Controls.Add(btnDeleteChild);
            this.Controls.Add(btnUpdateChild);
        }

        /// <summary>
        /// Loads the parent and child data into a DataSet using the configured queries.
        /// </summary>
        private void LoadData()
        {
            try
            {
                ds = new DataSet();

                // Load Parent (master) table.
                daParent = new SqlDataAdapter(parentQuery, conn);
                daParent.MissingSchemaAction = MissingSchemaAction.AddWithKey;
                daParent.Fill(ds, "Parent");

                // Load Child (detail) table.
                daChild = new SqlDataAdapter(childQuery, conn);
                daChild.MissingSchemaAction = MissingSchemaAction.AddWithKey;

                // Automatically generate UPDATE and DELETE commands for the child table.
                cbChild = new SqlCommandBuilder(daChild);
                daChild.Fill(ds, "Child");

                // Create the DataRelation between the parent and child tables dynamically.
                DataRelation relation = new DataRelation("ParentChild",
                    ds.Tables["Parent"].Columns[parentKey],
                    ds.Tables["Child"].Columns[childForeignKey]);
                ds.Relations.Add(relation);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading data: " + ex.Message);
            }
        }

        /// <summary>
        /// Establishes the master-detail binding between the two DataGridViews.
        /// </summary>
        private void SetupDataBinding()
        {
            try
            {
                // Bind the parent DataGridView to the Parent table.
                bsParent.DataSource = ds;
                bsParent.DataMember = "Parent";

                // Bind the child DataGridView through the DataRelation, so that it shows only related detail records.
                bsChild.DataSource = bsParent;
                bsChild.DataMember = "ParentChild";

                dgvParent.DataSource = bsParent;
                dgvChild.DataSource = bsChild;
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error setting up data binding: " + ex.Message);
            }
        }

        /// <summary>
        /// Event handler: Adds a new child record for the currently selected parent.
        /// </summary>
        private void BtnAddChild_Click(object sender, EventArgs e)
        {
            try
            {
                DataRowView newRow = (DataRowView)bsChild.AddNew();
                // Set the foreign key to link the new child with the current parent.
                newRow[childForeignKey] = ((DataRowView)bsParent.Current)[parentKey];
                bsChild.EndEdit();
                MessageBox.Show("New child record added (in-memory). Click 'Update Child' to commit changes to the database.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error adding child record: " + ex.Message);
            }
        }

        /// <summary>
        /// Event handler: Deletes the selected child record.
        /// </summary>
        private void BtnDeleteChild_Click(object sender, EventArgs e)
        {
            try
            {
                if (bsChild.Current != null)
                {
                    bsChild.RemoveCurrent();
                    MessageBox.Show("Child record deleted (in-memory). Click 'Update Child' to persist changes.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error deleting child record: " + ex.Message);
            }
        }

        /// <summary>
        /// Event handler: Updates the changes made in the child table back to the database.
        /// </summary>
        private void BtnUpdateChild_Click(object sender, EventArgs e)
        {
            try
            {
                bsChild.EndEdit();
                daChild.Update(ds, "Child");
                MessageBox.Show("Child table updated successfully!");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error updating child table: " + ex.Message);
            }
        }
    }
}
