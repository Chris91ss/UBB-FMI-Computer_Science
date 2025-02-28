-- Drop dependent tables first (those with foreign keys)
IF OBJECT_ID('SalesDetails', 'U') IS NOT NULL
   DROP TABLE SalesDetails;
GO

IF OBJECT_ID('OrderDetails', 'U') IS NOT NULL
   DROP TABLE OrderDetails;
GO

IF OBJECT_ID('MaintenanceServices', 'U') IS NOT NULL
   DROP TABLE MaintenanceServices;
GO

-- Drop tables that reference Suppliers
IF OBJECT_ID('SupplierOrders', 'U') IS NOT NULL
   DROP TABLE SupplierOrders;
GO

-- Now drop the main tables
IF OBJECT_ID('Sales', 'U') IS NOT NULL
   DROP TABLE Sales;
GO

IF OBJECT_ID('Employees', 'U') IS NOT NULL
   DROP TABLE Employees;
GO

-- Drop the Suppliers table last, as it is referenced
IF OBJECT_ID('Suppliers', 'U') IS NOT NULL
   DROP TABLE Suppliers;
GO

IF OBJECT_ID('Motorcycles', 'U') IS NOT NULL
   DROP TABLE Motorcycles;
GO

IF OBJECT_ID('Customers', 'U') IS NOT NULL
   DROP TABLE Customers;
GO

IF OBJECT_ID('Dealerships', 'U') IS NOT NULL
   DROP TABLE Dealerships;
GO

-- Now recreate the tables

-- Motorcycles Table
CREATE TABLE Motorcycles (
    MotorcycleID INT PRIMARY KEY IDENTITY(1,1),
    Model NVARCHAR(100),
    Brand NVARCHAR(100),
    EngineCapacity DECIMAL(10,2),
    Price DECIMAL(10,2),
    Year INT,
    StockQuantity INT
);

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Email NVARCHAR(100),
    Phone NVARCHAR(20),
    Address NVARCHAR(200)
);

-- Dealerships Table
CREATE TABLE Dealerships (
    DealershipID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100),
    Location NVARCHAR(200),
    ContactNumber NVARCHAR(20)
);

-- Employees Table
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Position NVARCHAR(50),
    Salary DECIMAL(10,2),
    DealershipID INT,
    FOREIGN KEY (DealershipID) REFERENCES Dealerships(DealershipID)
);

-- Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY IDENTITY(1,1),
    SupplierName NVARCHAR(100),
    ContactNumber NVARCHAR(20),
    Email NVARCHAR(100),
    Address NVARCHAR(200)
);

-- Sales Table
CREATE TABLE Sales (
    SaleID INT PRIMARY KEY IDENTITY(1,1),
    SaleDate DATE,
    TotalAmount DECIMAL(10,2),
    CustomerID INT,
    DealershipID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (DealershipID) REFERENCES Dealerships(DealershipID)
);

-- SalesDetails Table 
CREATE TABLE SalesDetails (
    SaleDetailID INT PRIMARY KEY IDENTITY(1,1),
    SaleID INT,
    MotorcycleID INT,
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    FOREIGN KEY (SaleID) REFERENCES Sales(SaleID),
    FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID)
);

-- SupplierOrders Table
CREATE TABLE SupplierOrders (
    SupplierOrderID INT PRIMARY KEY IDENTITY(1,1),
    OrderDate DATE,
    SupplierID INT,
    DealershipID INT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID),
    FOREIGN KEY (DealershipID) REFERENCES Dealerships(DealershipID)
);

-- OrderDetails Table 
CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY IDENTITY(1,1),
    SupplierOrderID INT,
    MotorcycleID INT,
    Quantity INT,
    PricePerUnit DECIMAL(10,2),
    FOREIGN KEY (SupplierOrderID) REFERENCES SupplierOrders(SupplierOrderID),
    FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID)
);

-- MaintenanceServices Table
CREATE TABLE MaintenanceServices (
    ServiceID INT PRIMARY KEY IDENTITY(1,1),
    ServiceType NVARCHAR(100),	
    ServiceDate DATE,
    MotorcycleID INT,
    EmployeeID INT,
    ServiceCost DECIMAL(10,2),
    FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

