USE MotorcycleDealershipDB;
GO

--Motorcycles: Has a single-column primary key (MotorcycleID) and no foreign keys.
--Employees: Has a single-column primary key (EmployeeID) and at least one foreign key (to Dealerships).
--MotorcycleInventory: Has a multi-column primary key (MotorcycleID, InventoryDate).
---------------------------------------------------------------
-- STEP 1: Adjust foreign keys for MaintenanceServices → Employees with ON DELETE CASCADE
-- Ensures deleting an Employee also deletes related MaintenanceServices rows.
---------------------------------------------------------------
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_MaintenanceServices_Employees')
BEGIN
    ALTER TABLE MaintenanceServices DROP CONSTRAINT FK_MaintenanceServices_Employees;
END

IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name LIKE 'FK__Maintenan__Emplo__%')
BEGIN
    DECLARE @OldEmpFK NVARCHAR(128);
    SELECT TOP 1 @OldEmpFK = name FROM sys.foreign_keys WHERE name LIKE 'FK__Maintenan__Emplo__%';
    IF @OldEmpFK IS NOT NULL
        EXEC('ALTER TABLE MaintenanceServices DROP CONSTRAINT ' + @OldEmpFK);
END

ALTER TABLE MaintenanceServices
ADD CONSTRAINT FK_MaintenanceServices_Employees
FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
ON DELETE CASCADE;
GO

---------------------------------------------------------------
-- STEP 2: Adjust foreign keys referencing Motorcycles with ON DELETE CASCADE
-- This simplifies deletion of data related to Motorcycles.
-- Applies to MaintenanceServices, SalesDetails, OrderDetails, MotorcycleInventory
---------------------------------------------------------------

-- MaintenanceServices → Motorcycles
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_MaintenanceServices_Motorcycles')
BEGIN
    ALTER TABLE MaintenanceServices DROP CONSTRAINT FK_MaintenanceServices_Motorcycles;
END

IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name LIKE 'FK__Maintenan__Motor__%')
BEGIN
    DECLARE @OldMSFK NVARCHAR(128);
    SELECT TOP 1 @OldMSFK = name FROM sys.foreign_keys WHERE name LIKE 'FK__Maintenan__Motor__%';
    IF @OldMSFK IS NOT NULL
        EXEC('ALTER TABLE MaintenanceServices DROP CONSTRAINT ' + @OldMSFK);
END

ALTER TABLE MaintenanceServices
ADD CONSTRAINT FK_MaintenanceServices_Motorcycles
FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID)
ON DELETE CASCADE;
GO

-- SalesDetails → Motorcycles
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_SalesDetails_Motorcycles')
BEGIN
    ALTER TABLE SalesDetails DROP CONSTRAINT FK_SalesDetails_Motorcycles;
END

IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name LIKE 'FK__SalesDeta__Motor__%')
BEGIN
    DECLARE @OldSDFK NVARCHAR(128);
    SELECT TOP 1 @OldSDFK = name FROM sys.foreign_keys WHERE name LIKE 'FK__SalesDeta__Motor__%';
    IF @OldSDFK IS NOT NULL
        EXEC('ALTER TABLE SalesDetails DROP CONSTRAINT ' + @OldSDFK);
END

ALTER TABLE SalesDetails
ADD CONSTRAINT FK_SalesDetails_Motorcycles
FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID)
ON DELETE CASCADE;
GO

-- OrderDetails → Motorcycles
IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_OrderDetails_Motorcycles')
BEGIN
    ALTER TABLE OrderDetails DROP CONSTRAINT FK_OrderDetails_Motorcycles;
END

IF EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name LIKE 'FK__OrderDeta__Motor__%')
BEGIN
    DECLARE @OldODFK NVARCHAR(128);
    SELECT TOP 1 @OldODFK = name FROM sys.foreign_keys WHERE name LIKE 'FK__OrderDeta__Motor__%';
    IF @OldODFK IS NOT NULL
        EXEC('ALTER TABLE OrderDetails DROP CONSTRAINT ' + @OldODFK);
END

ALTER TABLE OrderDetails
ADD CONSTRAINT FK_OrderDetails_Motorcycles
FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID)
ON DELETE CASCADE;
GO

-- MotorcycleInventory (multi-column PK) → Motorcycles (no need to pre-drop since we recreate table)
IF OBJECT_ID('MotorcycleInventory', 'U') IS NOT NULL
    DROP TABLE MotorcycleInventory;
GO

CREATE TABLE MotorcycleInventory (
    MotorcycleID INT NOT NULL,
    InventoryDate DATE NOT NULL,
    StockLevel INT NOT NULL,
    -- Multi-column PK requirement:
    CONSTRAINT PK_MotorcycleInventory PRIMARY KEY (MotorcycleID, InventoryDate),
    FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID) ON DELETE CASCADE
);
GO

---------------------------------------------------------------
-- STEP 3: Create required Views:
-- 1) vw_Motorcycles: SELECT from one table (Motorcycles)
-- 2) vw_EmployeeDealership: JOIN between Employees & Dealerships
-- 3) vw_MotorcycleSalesSummary: GROUP BY, multiple JOINs (Motorcycles, SalesDetails, Sales)
---------------------------------------------------------------
IF OBJECT_ID('vw_Motorcycles', 'V') IS NOT NULL
    DROP VIEW vw_Motorcycles;
GO

CREATE VIEW vw_Motorcycles AS
SELECT MotorcycleID, Model, Brand, EngineCapacity, Price, Year, StockQuantity
FROM Motorcycles;
GO

IF OBJECT_ID('vw_EmployeeDealership', 'V') IS NOT NULL
    DROP VIEW vw_EmployeeDealership;
GO

CREATE VIEW vw_EmployeeDealership AS
SELECT E.EmployeeID, E.FirstName, E.LastName, E.Position, E.Salary, D.Name AS DealershipName, D.Location
FROM Employees E
JOIN Dealerships D ON E.DealershipID = D.DealershipID;
GO

IF OBJECT_ID('vw_MotorcycleSalesSummary', 'V') IS NOT NULL
    DROP VIEW vw_MotorcycleSalesSummary;
GO

CREATE VIEW vw_MotorcycleSalesSummary AS
SELECT M.Brand,
       COUNT(SD.SaleDetailID) AS TotalSalesRecords,
       SUM(SD.Quantity) AS TotalQtySold,
       AVG(SD.UnitPrice) AS AvgPriceSold
FROM Motorcycles M
JOIN SalesDetails SD ON M.MotorcycleID = SD.MotorcycleID
JOIN Sales S ON S.SaleID = SD.SaleID
GROUP BY M.Brand;
GO

---------------------------------------------------------------
-- STEP 4: Insert Tables into [Tables] if not present
-- These entries define which tables can be part of tests.
-- Motorcycles (one-column PK, no FK)
-- Employees (one-column PK, has FK)
-- MotorcycleInventory (multi-column PK)
-- MaintenanceServices, Sales, SalesDetails, OrderDetails also included.
---------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [Tables] WHERE [Name] = 'Motorcycles')
    INSERT INTO [Tables]([Name]) VALUES('Motorcycles');

IF NOT EXISTS (SELECT 1 FROM [Tables] WHERE [Name] = 'Employees')
    INSERT INTO [Tables]([Name]) VALUES('Employees');

IF NOT EXISTS (SELECT 1 FROM [Tables] WHERE [Name] = 'MotorcycleInventory')
    INSERT INTO [Tables]([Name]) VALUES('MotorcycleInventory');

IF NOT EXISTS (SELECT 1 FROM [Tables] WHERE [Name] = 'MaintenanceServices')
    INSERT INTO [Tables]([Name]) VALUES('MaintenanceServices');

IF NOT EXISTS (SELECT 1 FROM [Tables] WHERE [Name] = 'Sales')
    INSERT INTO [Tables]([Name]) VALUES('Sales');

IF NOT EXISTS (SELECT 1 FROM [Tables] WHERE [Name] = 'SalesDetails')
    INSERT INTO [Tables]([Name]) VALUES('SalesDetails');

IF NOT EXISTS (SELECT 1 FROM [Tables] WHERE [Name] = 'OrderDetails')
    INSERT INTO [Tables]([Name]) VALUES('OrderDetails');

---------------------------------------------------------------
-- STEP 5: Insert Views into [Views] if not present
-- Defines which views can be tested.
-- vw_Motorcycles (one table)
-- vw_EmployeeDealership (JOIN)
-- vw_MotorcycleSalesSummary (GROUP BY + JOIN)
---------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [Views] WHERE [Name] = 'vw_Motorcycles')
    INSERT INTO [Views]([Name]) VALUES('vw_Motorcycles');

IF NOT EXISTS (SELECT 1 FROM [Views] WHERE [Name] = 'vw_EmployeeDealership')
    INSERT INTO [Views]([Name]) VALUES('vw_EmployeeDealership');

IF NOT EXISTS (SELECT 1 FROM [Views] WHERE [Name] = 'vw_MotorcycleSalesSummary')
    INSERT INTO [Views]([Name]) VALUES('vw_MotorcycleSalesSummary');

---------------------------------------------------------------
-- STEP 6: Create/Update a Test scenario: "PerformanceTest1"
-- A Test specifies which tables and views to test, order and NoOfRows.
--
-- We define the order:
-- MaintenanceServices (pos 1), SalesDetails (2), OrderDetails (3), Employees (4),
-- MotorcycleInventory (5), Sales (6), Motorcycles (7)
--
-- We attach 3 views to this test as per requirement.
---------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [Tests] WHERE [Name] = 'PerformanceTest1')
    INSERT INTO [Tests]([Name]) VALUES('PerformanceTest1');

DECLARE @TestID INT;
SELECT @TestID = TestID FROM [Tests] WHERE [Name] = 'PerformanceTest1';

DECLARE @MotorcyclesID INT = (SELECT TableID FROM [Tables] WHERE [Name] = 'Motorcycles');
DECLARE @EmployeesID INT = (SELECT TableID FROM [Tables] WHERE [Name] = 'Employees');
DECLARE @MotorcycleInvID INT = (SELECT TableID FROM [Tables] WHERE [Name] = 'MotorcycleInventory');
DECLARE @MaintServicesID INT = (SELECT TableID FROM [Tables] WHERE [Name] = 'MaintenanceServices');
DECLARE @SalesID INT = (SELECT TableID FROM [Tables] WHERE [Name] = 'Sales');
DECLARE @SalesDetailsID INT = (SELECT TableID FROM [Tables] WHERE [Name] = 'SalesDetails');
DECLARE @OrderDetailsID INT = (SELECT TableID FROM [Tables] WHERE [Name] = 'OrderDetails');

IF NOT EXISTS (SELECT 1 FROM TestTables WHERE TestID=@TestID AND TableID=@MaintServicesID)
    INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES(@TestID, @MaintServicesID, 5, 1);

IF NOT EXISTS (SELECT 1 FROM TestTables WHERE TestID=@TestID AND TableID=@SalesDetailsID)
    INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES(@TestID, @SalesDetailsID, 5, 2);

IF NOT EXISTS (SELECT 1 FROM TestTables WHERE TestID=@TestID AND TableID=@OrderDetailsID)
    INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES(@TestID, @OrderDetailsID, 5, 3);

IF NOT EXISTS (SELECT 1 FROM TestTables WHERE TestID=@TestID AND TableID=@EmployeesID)
    INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES(@TestID, @EmployeesID, 5, 4);

IF NOT EXISTS (SELECT 1 FROM TestTables WHERE TestID=@TestID AND TableID=@MotorcycleInvID)
    INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES(@TestID, @MotorcycleInvID, 5, 5);

IF NOT EXISTS (SELECT 1 FROM TestTables WHERE TestID=@TestID AND TableID=@SalesID)
    INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES(@TestID, @SalesID, 5, 6);

IF NOT EXISTS (SELECT 1 FROM TestTables WHERE TestID=@TestID AND TableID=@MotorcyclesID)
    INSERT INTO TestTables(TestID, TableID, NoOfRows, Position) VALUES(@TestID, @MotorcyclesID, 5, 7);

-- Associate Views with the Test
DECLARE @VwMotorcyclesID INT = (SELECT ViewID FROM [Views] WHERE [Name] = 'vw_Motorcycles');
DECLARE @VwEmpDealID INT = (SELECT ViewID FROM [Views] WHERE [Name] = 'vw_EmployeeDealership');
DECLARE @VwMSSumID INT = (SELECT ViewID FROM [Views] WHERE [Name] = 'vw_MotorcycleSalesSummary');

IF NOT EXISTS (SELECT 1 FROM TestViews WHERE TestID=@TestID AND ViewID=@VwMotorcyclesID)
    INSERT INTO TestViews(TestID, ViewID) VALUES(@TestID, @VwMotorcyclesID);

IF NOT EXISTS (SELECT 1 FROM TestViews WHERE TestID=@TestID AND ViewID=@VwEmpDealID)
    INSERT INTO TestViews(TestID, ViewID) VALUES(@TestID, @VwEmpDealID);

IF NOT EXISTS (SELECT 1 FROM TestViews WHERE TestID=@TestID AND ViewID=@VwMSSumID)
    INSERT INTO TestViews(TestID, ViewID) VALUES(@TestID, @VwMSSumID);

---------------------------------------------------------------
-- STEP 7: Stored Procedure: sp_RunTest @TestID
--
-- Procedure does:
-- 1) Creates a TestRun record (TestRuns)
-- 2) Deletes data from test tables in ascending Position order (TestTables)
-- 3) Inserts NoOfRows records into these tables in reverse order
-- 4) Evaluates test views (TestViews) and records performance (TestRunViews)
-- 5) Records insert performance data in TestRunTables
--
-- This meets the requirements of running a test and storing results.
---------------------------------------------------------------
IF OBJECT_ID('sp_RunTest', 'P') IS NOT NULL
    DROP PROCEDURE sp_RunTest;
GO

CREATE PROCEDURE sp_RunTest @TestID INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @TestRunID INT;
    DECLARE @StartAt DATETIME = GETDATE();
    INSERT INTO TestRuns (Description, StartAt) VALUES ('Running test ' + CAST(@TestID AS VARCHAR(10)), @StartAt);
    SET @TestRunID = SCOPE_IDENTITY();

    BEGIN TRY
        DECLARE @TableListForDelete TABLE (TableID INT, NoOfRows INT, Position INT);
        INSERT INTO @TableListForDelete(TableID, NoOfRows, Position)
        SELECT TableID, NoOfRows, Position
        FROM TestTables
        WHERE TestID = @TestID
        ORDER BY Position;

        -- Delete in ascending Position
        DECLARE @DelTableID INT, @DelNoOfRows INT, @DelPos INT;
        DECLARE DelCursor CURSOR LOCAL FAST_FORWARD FOR
            SELECT TableID, NoOfRows, Position FROM @TableListForDelete ORDER BY Position;
        OPEN DelCursor;
        FETCH NEXT FROM DelCursor INTO @DelTableID, @DelNoOfRows, @DelPos;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            DECLARE @DelTableName NVARCHAR(50) = (SELECT [Name] FROM [Tables] WHERE TableID = @DelTableID);
            DECLARE @SQLDel NVARCHAR(MAX) = N'DELETE FROM ' + QUOTENAME(@DelTableName) + ';';
            EXEC (@SQLDel);
            FETCH NEXT FROM DelCursor INTO @DelTableID, @DelNoOfRows, @DelPos;
        END
        CLOSE DelCursor;
        DEALLOCATE DelCursor;

        -- Insert in reverse order
        DECLARE @TableListForInsert TABLE (TableID INT, NoOfRows INT, Position INT);
        INSERT INTO @TableListForInsert
        SELECT TableID, NoOfRows, Position FROM @TableListForDelete ORDER BY Position DESC;

        DECLARE @InsTableID INT, @InsNoOfRows INT, @InsPos INT;
        DECLARE InsertCursor CURSOR LOCAL FAST_FORWARD FOR
            SELECT TableID, NoOfRows, Position FROM @TableListForInsert ORDER BY Position DESC;
        OPEN InsertCursor;
        FETCH NEXT FROM InsertCursor INTO @InsTableID, @InsNoOfRows, @InsPos;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            DECLARE @InsTableName NVARCHAR(50) = (SELECT [Name] FROM [Tables] WHERE TableID = @InsTableID);
            DECLARE @InsertStart DATETIME = GETDATE();

            -- Insert dummy data per table
            IF @InsTableName = 'Motorcycles'
            BEGIN
                -- Single-column PK, no FK
                DECLARE @i INT = 1;
                WHILE @i <= @InsNoOfRows
                BEGIN
                    INSERT INTO Motorcycles (Model, Brand, EngineCapacity, Price, Year, StockQuantity)
                    VALUES ('TestModel'+CAST(@i AS VARCHAR(10)), 'TestBrand', 600, 10000, 2024, 10);
                    SET @i = @i + 1;
                END
            END
            ELSE IF @InsTableName = 'Employees'
            BEGIN
                -- Single-column PK with a FK to Dealerships
                DECLARE @j INT = 1;
                WHILE @j <= @InsNoOfRows
                BEGIN
                    INSERT INTO Employees (FirstName, LastName, Position, Salary, DealershipID)
                    VALUES ('TestF'+CAST(@j AS VARCHAR(10)), 'TestL', 'TestPos', 30000, 1);
                    SET @j = @j + 1;
                END
            END
            ELSE IF @InsTableName = 'MotorcycleInventory'
            BEGIN
                -- Multi-column PK table
                ;WITH CTE_TopMC AS (
                    SELECT TOP(@InsNoOfRows) MotorcycleID FROM Motorcycles ORDER BY MotorcycleID
                )
                INSERT INTO MotorcycleInventory(MotorcycleID, InventoryDate, StockLevel)
                SELECT MotorcycleID, CAST(GETDATE() AS DATE), 100 FROM CTE_TopMC;
            END
            ELSE IF @InsTableName = 'MaintenanceServices'
            BEGIN
                -- Depends on Motorcycles and Employees
                DECLARE @k INT = 1;
                DECLARE @SampleMotorcycleID_MS INT = (SELECT TOP 1 MotorcycleID FROM Motorcycles);
                DECLARE @SampleEmployeeID_MS INT = (SELECT TOP 1 EmployeeID FROM Employees);

                WHILE @k <= @InsNoOfRows
                BEGIN
                    INSERT INTO MaintenanceServices(ServiceType, ServiceDate, MotorcycleID, EmployeeID, ServiceCost)
                    VALUES('TestService', GETDATE(), @SampleMotorcycleID_MS, @SampleEmployeeID_MS, 100.00);
                    SET @k = @k + 1;
                END
            END
            ELSE IF @InsTableName = 'Sales'
            BEGIN
                -- Insert dummy sales
                DECLARE @x INT = 1;
                WHILE @x <= @InsNoOfRows
                BEGIN
                    INSERT INTO Sales (SaleDate, TotalAmount, CustomerID, DealershipID)
                    VALUES (GETDATE(), 15000, 1, 1);
                    SET @x = @x + 1;
                END
            END
            ELSE IF @InsTableName = 'SalesDetails'
            BEGIN
                -- References Sales and Motorcycles
                DECLARE @y INT = 1;
                DECLARE @SampleMotorcycleID_SD INT = (SELECT TOP 1 MotorcycleID FROM Motorcycles);
                DECLARE @SampleSaleID_SD INT = (SELECT TOP 1 SaleID FROM Sales);

                WHILE @y <= @InsNoOfRows
                BEGIN
                    INSERT INTO SalesDetails (SaleID, MotorcycleID, Quantity, UnitPrice)
                    VALUES(@SampleSaleID_SD, @SampleMotorcycleID_SD, 1, 10000.00);
                    SET @y = @y + 1;
                END
            END
            ELSE IF @InsTableName = 'OrderDetails'
            BEGIN
                -- References SupplierOrders and Motorcycles
                DECLARE @z INT = 1;
                DECLARE @SampleMotorcycleID_OD INT = (SELECT TOP 1 MotorcycleID FROM Motorcycles);
                DECLARE @SampleSupplierOrderID INT = (SELECT TOP 1 SupplierOrderID FROM SupplierOrders);

                IF @SampleSupplierOrderID IS NULL
                BEGIN
                    -- Insert a SupplierOrder if none exists
                    INSERT INTO SupplierOrders (OrderDate, SupplierID, DealershipID) VALUES (GETDATE(), 1, 1);
                    SET @SampleSupplierOrderID = SCOPE_IDENTITY();
                END

                WHILE @z <= @InsNoOfRows
                BEGIN
                    INSERT INTO OrderDetails (SupplierOrderID, MotorcycleID, Quantity, PricePerUnit)
                    VALUES(@SampleSupplierOrderID, @SampleMotorcycleID_OD, 1, 9000.00);
                    SET @z = @z + 1;
                END
            END

            DECLARE @InsertEnd DATETIME = GETDATE();
            INSERT INTO TestRunTables(TestRunID, TableID, StartAt, EndAt)
            VALUES(@TestRunID, @InsTableID, @InsertStart, @InsertEnd);

            FETCH NEXT FROM InsertCursor INTO @InsTableID, @InsNoOfRows, @InsPos;
        END

        CLOSE InsertCursor;
        DEALLOCATE InsertCursor;

        -- Evaluate views (3 views) and record performance
        DECLARE @ViewCursor CURSOR;
        DECLARE @ViewID INT;
        DECLARE @ViewName NVARCHAR(50);
        SET @ViewCursor = CURSOR LOCAL FAST_FORWARD FOR
            SELECT V.ViewID, V.Name
            FROM TestViews TV
            JOIN Views V ON TV.ViewID = V.ViewID
            WHERE TV.TestID = @TestID;

        OPEN @ViewCursor;
        FETCH NEXT FROM @ViewCursor INTO @ViewID, @ViewName;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            DECLARE @ViewStart DATETIME = GETDATE();
            DECLARE @ViewSQL NVARCHAR(MAX) = N'SELECT * FROM ' + QUOTENAME(@ViewName) + ';';
            EXEC (@ViewSQL);
            DECLARE @ViewEnd DATETIME = GETDATE();

            INSERT INTO TestRunViews(TestRunID, ViewID, StartAt, EndAt)
            VALUES(@TestRunID, @ViewID, @ViewStart, @ViewEnd);

            FETCH NEXT FROM @ViewCursor INTO @ViewID, @ViewName;
        END

        CLOSE @ViewCursor;
        DEALLOCATE @ViewCursor;

        -- Finish test run
        UPDATE TestRuns SET EndAt = GETDATE() WHERE TestRunID = @TestRunID;

        DECLARE @RunStart DATETIME, @RunEnd DATETIME;
        SELECT @RunStart=StartAt, @RunEnd=EndAt FROM TestRuns WHERE TestRunID=@TestRunID;
        PRINT 'Test run completed successfully. TestRunID=' + CAST(@TestRunID AS VARCHAR(10));
        PRINT 'Test run started at ' + CAST(@RunStart AS VARCHAR(30)) + ' and ended at ' + CAST(@RunEnd AS VARCHAR(30)) + '.';

    END TRY
    BEGIN CATCH
        PRINT 'Error running the test. Check messages for details.';
        UPDATE TestRuns SET EndAt = GETDATE() WHERE TestRunID = @TestRunID;
        THROW;
    END CATCH
END;
GO

---------------------------------------------------------------
-- STEP 8: Example Execution
-- Run the test and verify performance data captured.
---------------------------------------------------------------
DECLARE @TestIDRun INT;
SELECT @TestIDRun = TestID FROM Tests WHERE Name = 'PerformanceTest1';

EXEC sp_RunTest @TestIDRun;

---------------------------------------------------------------
-- STEP 9: Check results stored in TestRuns, TestRunTables, TestRunViews
---------------------------------------------------------------
SELECT * FROM TestRuns WHERE TestRunID = (SELECT MAX(TestRunID) FROM TestRuns);
SELECT * FROM TestRunTables WHERE TestRunID = (SELECT MAX(TestRunID) FROM TestRuns);
SELECT * FROM TestRunViews WHERE TestRunID = (SELECT MAX(TestRunID) FROM TestRuns);
