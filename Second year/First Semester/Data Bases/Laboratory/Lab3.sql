-- ============================================
-- 1. Modify the Type of a Column
-- ============================================

-- Stored procedure to modify the data type of EngineCapacity to INT
ALTER PROCEDURE sp_ModifyColumnType_EngineCapacity_ToInt
AS
BEGIN
    -- Check if the column EngineCapacity exists in the Motorcycles table
    IF EXISTS (
        SELECT 1 FROM sys.columns
        WHERE Name = N'EngineCapacity' AND Object_ID = Object_ID(N'Motorcycles')
    )
    BEGIN
        -- Alter the column EngineCapacity to INT data type
        ALTER TABLE Motorcycles
        ALTER COLUMN EngineCapacity INT;
        PRINT 'EngineCapacity data type has been changed to INT.';
    END
    ELSE
    BEGIN
        PRINT 'Column EngineCapacity does not exist in Motorcycles table.';
    END
END;
GO

-- Stored procedure to revert the data type of EngineCapacity back to DECIMAL(10,2)
ALTER PROCEDURE sp_Revert_ModifyColumnType_EngineCapacity
AS
BEGIN
    -- Check if the column EngineCapacity exists in the Motorcycles table
    IF EXISTS (
        SELECT 1 FROM sys.columns
        WHERE Name = N'EngineCapacity' AND Object_ID = Object_ID(N'Motorcycles')
    )
    BEGIN
        -- Alter the column EngineCapacity back to DECIMAL(10,2)
        ALTER TABLE Motorcycles
        ALTER COLUMN EngineCapacity DECIMAL(10,2);
        PRINT 'EngineCapacity data type has been reverted back to DECIMAL(10,2).';
    END
    ELSE
    BEGIN
        PRINT 'Column EngineCapacity does not exist in Motorcycles table.';
    END
END;
GO

-- ============================================
-- 2. Add / Remove a Column
-- ============================================

-- Stored procedure to add a new column Color to the Motorcycles table
ALTER PROCEDURE sp_AddColumn_Motorcycles_Color
AS
BEGIN
    -- Check if the column Color already exists
    IF NOT EXISTS (
        SELECT 1 FROM sys.columns
        WHERE Name = N'Color' AND Object_ID = Object_ID(N'Motorcycles')
    )
    BEGIN
        -- Add the new column Color of type NVARCHAR(50)
        ALTER TABLE Motorcycles
        ADD Color NVARCHAR(50);
        PRINT 'Column Color has been added to Motorcycles table.';
    END
    ELSE
    BEGIN
        PRINT 'Column Color already exists in Motorcycles table.';
    END
END;
GO

-- Stored procedure to remove the Color column from the Motorcycles table
ALTER PROCEDURE sp_RemoveColumn_Motorcycles_Color
AS
BEGIN
    -- Check if the column Color exists
    IF EXISTS (
        SELECT 1 FROM sys.columns
        WHERE Name = N'Color' AND Object_ID = Object_ID(N'Motorcycles')
    )
    BEGIN
        -- Drop the Color column
        ALTER TABLE Motorcycles
        DROP COLUMN Color;
        PRINT 'Column Color has been removed from Motorcycles table.';
    END
    ELSE
    BEGIN
        PRINT 'Column Color does not exist in Motorcycles table.';
    END
END;
GO

-- ============================================
-- 3. Add / Remove a DEFAULT Constraint
-- ============================================

-- Stored procedure to add a DEFAULT constraint to StockQuantity in Motorcycles
ALTER PROCEDURE sp_AddDefaultConstraint_StockQuantity
AS
BEGIN
    -- Check if the DEFAULT constraint already exists
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = Name
    FROM sys.default_constraints
    WHERE parent_object_id = OBJECT_ID(N'Motorcycles')
      AND parent_column_id = COLUMNPROPERTY(OBJECT_ID(N'Motorcycles'), 'StockQuantity', 'ColumnID');

    IF @ConstraintName IS NULL
    BEGIN
        -- Add the DEFAULT constraint DF_Motorcycles_StockQuantity with default value 0
        ALTER TABLE Motorcycles
        ADD CONSTRAINT DF_Motorcycles_StockQuantity DEFAULT 0 FOR StockQuantity;
        PRINT 'DEFAULT constraint DF_Motorcycles_StockQuantity has been added to StockQuantity.';
    END
    ELSE
    BEGIN
        PRINT 'DEFAULT constraint on StockQuantity already exists.';
    END
END;
GO

-- Stored procedure to remove the DEFAULT constraint from StockQuantity in Motorcycles
ALTER PROCEDURE sp_RemoveDefaultConstraint_StockQuantity
AS
BEGIN
    -- Find the name of the DEFAULT constraint
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = Name
    FROM sys.default_constraints
    WHERE parent_object_id = OBJECT_ID(N'Motorcycles')
      AND parent_column_id = COLUMNPROPERTY(OBJECT_ID(N'Motorcycles'), 'StockQuantity', 'ColumnID');

    IF @ConstraintName IS NOT NULL
    BEGIN
        -- Drop the DEFAULT constraint using dynamic SQL
        DECLARE @SQL NVARCHAR(500);
        SET @SQL = 'ALTER TABLE Motorcycles DROP CONSTRAINT ' + QUOTENAME(@ConstraintName) + ';';
        EXEC sp_executesql @SQL;
        PRINT 'DEFAULT constraint ' + @ConstraintName + ' has been dropped from StockQuantity.';
    END
    ELSE
    BEGIN
        PRINT 'No DEFAULT constraint found on StockQuantity.';
    END
END;
GO

-- ============================================
-- 4. Add / Remove a Foreign Key (Moved to Version 5)
-- ============================================

-- Stored procedure to remove the foreign key from MaintenanceServices to Motorcycles
ALTER PROCEDURE sp_RemoveForeignKey_MaintenanceServices_Motorcycles
AS
BEGIN
    -- Find the name of the foreign key constraint
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = fk.name
    FROM sys.foreign_keys fk
    WHERE fk.parent_object_id = OBJECT_ID(N'MaintenanceServices')
      AND fk.referenced_object_id = OBJECT_ID(N'Motorcycles')
      AND fk.name = 'FK_MaintenanceServices_Motorcycles';

    IF @ConstraintName IS NOT NULL
    BEGIN
        -- Drop the foreign key constraint using dynamic SQL
        DECLARE @SQL NVARCHAR(500);
        SET @SQL = 'ALTER TABLE MaintenanceServices DROP CONSTRAINT ' + QUOTENAME(@ConstraintName) + ';';
        EXEC sp_executesql @SQL;
        PRINT 'Foreign key constraint ' + @ConstraintName + ' has been dropped from MaintenanceServices.';
    END
    ELSE
    BEGIN
        PRINT 'Foreign key constraint FK_MaintenanceServices_Motorcycles does not exist.';
    END
END;
GO

-- Stored procedure to add the foreign key back to MaintenanceServices
ALTER PROCEDURE sp_AddForeignKey_MaintenanceServices_Motorcycles
AS
BEGIN
    -- Check if the foreign key constraint already exists
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = fk.name
    FROM sys.foreign_keys fk
    WHERE fk.parent_object_id = OBJECT_ID(N'MaintenanceServices')
      AND fk.referenced_object_id = OBJECT_ID(N'Motorcycles')
      AND fk.name = 'FK_MaintenanceServices_Motorcycles';

    IF @ConstraintName IS NULL
    BEGIN
        -- Add the foreign key constraint
        ALTER TABLE MaintenanceServices
        ADD CONSTRAINT FK_MaintenanceServices_Motorcycles
        FOREIGN KEY (MotorcycleID) REFERENCES Motorcycles(MotorcycleID);
        PRINT 'Foreign key constraint FK_MaintenanceServices_Motorcycles has been added to MaintenanceServices.';
    END
    ELSE
    BEGIN
        PRINT 'Foreign key constraint FK_MaintenanceServices_Motorcycles already exists.';
    END
END;
GO

-- ============================================
-- 5. Add / Remove a Primary Key (Moved to Version 6)
-- ============================================

-- Stored procedure to remove the primary key constraint from Motorcycles table
ALTER PROCEDURE sp_RemovePrimaryKey_Motorcycles
AS
BEGIN
    -- Find the name of the primary key constraint
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = Name
    FROM sys.key_constraints
    WHERE parent_object_id = OBJECT_ID(N'Motorcycles')
      AND type = 'PK';

    IF @ConstraintName IS NOT NULL
    BEGIN
        -- Drop the primary key constraint using dynamic SQL
        DECLARE @SQL NVARCHAR(500);
        SET @SQL = 'ALTER TABLE Motorcycles DROP CONSTRAINT ' + QUOTENAME(@ConstraintName) + ';';
        EXEC sp_executesql @SQL;
        PRINT 'Primary key constraint ' + @ConstraintName + ' has been dropped from Motorcycles table.';
    END
    ELSE
    BEGIN
        PRINT 'Primary key constraint does not exist on Motorcycles table.';
    END
END;
GO

-- Stored procedure to add the primary key constraint back to Motorcycles table
ALTER PROCEDURE sp_AddPrimaryKey_Motorcycles
AS
BEGIN
    -- Check if the primary key constraint already exists
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = Name
    FROM sys.key_constraints
    WHERE parent_object_id = OBJECT_ID(N'Motorcycles')
      AND type = 'PK';

    IF @ConstraintName IS NULL
    BEGIN
        -- Add the primary key constraint on MotorcycleID
        ALTER TABLE Motorcycles
        ADD CONSTRAINT PK_Motorcycles PRIMARY KEY (MotorcycleID);
        PRINT 'Primary key constraint PK_Motorcycles has been added to Motorcycles table.';
    END
    ELSE
    BEGIN
        PRINT 'Primary key constraint already exists on Motorcycles table.';
    END
END;
GO

-- ============================================
-- 6. Add / Remove a Candidate Key
-- ============================================

-- Stored procedure to add a unique constraint on Model and Brand in Motorcycles
ALTER PROCEDURE sp_AddCandidateKey_Motorcycles_ModelBrand
AS
BEGIN
    -- Check if the unique constraint already exists
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = Name
    FROM sys.key_constraints
    WHERE parent_object_id = OBJECT_ID(N'Motorcycles')
      AND type = 'UQ'
      AND Name = 'UQ_Motorcycles_Model_Brand';

    IF @ConstraintName IS NULL
    BEGIN
        -- Add the unique constraint UQ_Motorcycles_Model_Brand
        ALTER TABLE Motorcycles
        ADD CONSTRAINT UQ_Motorcycles_Model_Brand UNIQUE (Model, Brand);
        PRINT 'Unique constraint UQ_Motorcycles_Model_Brand has been added to Motorcycles table.';
    END
    ELSE
    BEGIN
        PRINT 'Unique constraint UQ_Motorcycles_Model_Brand already exists.';
    END
END;
GO

-- Stored procedure to remove the unique constraint from Model and Brand in Motorcycles
ALTER PROCEDURE sp_RemoveCandidateKey_Motorcycles_ModelBrand
AS
BEGIN
    -- Check if the unique constraint exists
    DECLARE @ConstraintName NVARCHAR(255);
    SELECT @ConstraintName = Name
    FROM sys.key_constraints
    WHERE parent_object_id = OBJECT_ID(N'Motorcycles')
          AND type = 'UQ'
          AND Name = 'UQ_Motorcycles_Model_Brand';

    IF @ConstraintName IS NOT NULL
    BEGIN
        -- Drop the unique constraint using dynamic SQL
        DECLARE @SQL NVARCHAR(500);
        SET @SQL = 'ALTER TABLE Motorcycles DROP CONSTRAINT ' + QUOTENAME(@ConstraintName) + ';';
        EXEC sp_executesql @SQL;
        PRINT 'Unique constraint ' + @ConstraintName + ' has been dropped from Motorcycles table.';
    END
    ELSE
    BEGIN
        PRINT 'Unique constraint UQ_Motorcycles_Model_Brand does not exist.';
    END
END;
GO

-- ============================================
-- 7. Create / Drop a Table
-- ============================================

-- Stored procedure to create a new table Accessories
ALTER PROCEDURE sp_CreateTable_Accessories
AS
BEGIN
    -- Check if the table Accessories already exists
    IF NOT EXISTS (
        SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Accessories') AND type in (N'U')
    )
    BEGIN
        -- Create the Accessories table
        CREATE TABLE Accessories (
            AccessoryID INT PRIMARY KEY IDENTITY(1,1),
            AccessoryName NVARCHAR(100),
            Price DECIMAL(10,2)
        );
        PRINT 'Table Accessories has been created.';
    END
    ELSE
    BEGIN
        PRINT 'Table Accessories already exists.';
    END
END;
GO

-- Stored procedure to drop the Accessories table
ALTER PROCEDURE sp_DropTable_Accessories
AS
BEGIN
    -- Check if the table Accessories exists
    IF EXISTS (
        SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Accessories') AND type in (N'U')
    )
    BEGIN
        -- Drop the Accessories table
        DROP TABLE Accessories;
        PRINT 'Table Accessories has been dropped.';
    END
    ELSE
    BEGIN
        PRINT 'Table Accessories does not exist.';
    END
END;
GO

-- ============================================
-- 8. Create a Table to Hold the Current Version of the Database Schema
-- ============================================

-- Drop the SchemaVersion table if it exists
IF OBJECT_ID('SchemaVersion', 'U') IS NOT NULL
    DROP TABLE SchemaVersion;
GO

-- Create the SchemaVersion table to hold the current version number
CREATE TABLE SchemaVersion (
    CurrentVersion INT NOT NULL
);
GO

-- Initialize the schema version to 1
INSERT INTO SchemaVersion (CurrentVersion) VALUES (1);
GO

-- ============================================
-- 9. Stored Procedure to Update the Database Schema to a Specific Version
-- ============================================

-- Stored procedure to update the database schema to a specific version
ALTER PROCEDURE sp_UpdateSchemaToVersion @TargetVersion INT
AS
BEGIN
    -- Declare variable to hold the current version
    DECLARE @CurrentVersion INT;

    -- Retrieve the current version from the SchemaVersion table
    SELECT @CurrentVersion = CurrentVersion FROM SchemaVersion;

    -- Validate that the target version is within the acceptable range (1-8)
    IF @TargetVersion < 1 OR @TargetVersion > 8
    BEGIN
        PRINT 'Error: Target version must be between 1 and 8.';
        RETURN;
    END

    -- Check if the target version is the same as the current version
    IF @TargetVersion = @CurrentVersion
    BEGIN
        PRINT 'Database is already at the target version.';
        RETURN;
    END

    -- Begin a transaction to ensure all operations succeed or fail together
    BEGIN TRANSACTION;

    BEGIN TRY
        -- If upgrading to a higher version
        IF @TargetVersion > @CurrentVersion
        BEGIN
            -- Loop through each version incrementally
            WHILE @CurrentVersion < @TargetVersion
            BEGIN
                SET @CurrentVersion = @CurrentVersion + 1;

                PRINT 'Upgrading to version ' + CAST(@CurrentVersion AS NVARCHAR(10)) + '...';

                -- Apply changes based on the version number
                IF @CurrentVersion = 2
                BEGIN
                    -- Modify EngineCapacity data type to INT
                    EXEC sp_ModifyColumnType_EngineCapacity_ToInt;
                END
                ELSE IF @CurrentVersion = 3
                BEGIN
                    -- Add Color column to Motorcycles
                    EXEC sp_AddColumn_Motorcycles_Color;
                END
                ELSE IF @CurrentVersion = 4
                BEGIN
                    -- Add DEFAULT constraint to StockQuantity
                    EXEC sp_AddDefaultConstraint_StockQuantity;
                END
                ELSE IF @CurrentVersion = 5
                BEGIN
                    -- Remove foreign key from MaintenanceServices to Motorcycles
                    EXEC sp_RemoveForeignKey_MaintenanceServices_Motorcycles;
                END
                ELSE IF @CurrentVersion = 6
                BEGIN
                    -- Remove primary key from Motorcycles
                    EXEC sp_RemovePrimaryKey_Motorcycles;
                END
                ELSE IF @CurrentVersion = 7
                BEGIN
                    -- Add candidate key on Model and Brand
                    EXEC sp_AddCandidateKey_Motorcycles_ModelBrand;
                END
                ELSE IF @CurrentVersion = 8
                BEGIN
                    -- Create the Accessories table
                    EXEC sp_CreateTable_Accessories;
                END

                -- Update the current version in the SchemaVersion table
                UPDATE SchemaVersion SET CurrentVersion = @CurrentVersion;
                PRINT 'Upgrade to version ' + CAST(@CurrentVersion AS NVARCHAR(10)) + ' completed.';
            END
        END
        -- If downgrading to a lower version
        ELSE IF @TargetVersion < @CurrentVersion
        BEGIN
            -- Loop through each version decrementally
            WHILE @CurrentVersion > @TargetVersion
            BEGIN
                PRINT 'Downgrading from version ' + CAST(@CurrentVersion AS NVARCHAR(10)) + '...';

                -- Revert changes based on the current version
                IF @CurrentVersion = 8
                BEGIN
                    -- Drop the Accessories table
                    EXEC sp_DropTable_Accessories;
                END
                ELSE IF @CurrentVersion = 7
                BEGIN
                    -- Remove candidate key from Motorcycles
                    EXEC sp_RemoveCandidateKey_Motorcycles_ModelBrand;
                END
                ELSE IF @CurrentVersion = 6
                BEGIN
                    -- Add primary key back to Motorcycles
                    EXEC sp_AddPrimaryKey_Motorcycles;
                END
                ELSE IF @CurrentVersion = 5
                BEGIN
                    -- Add foreign key back to MaintenanceServices
                    EXEC sp_AddForeignKey_MaintenanceServices_Motorcycles;
                END
                ELSE IF @CurrentVersion = 4
                BEGIN
                    -- Remove DEFAULT constraint from StockQuantity
                    EXEC sp_RemoveDefaultConstraint_StockQuantity;
                END
                ELSE IF @CurrentVersion = 3
                BEGIN
                    -- Remove Color column from Motorcycles
                    EXEC sp_RemoveColumn_Motorcycles_Color;
                END
                ELSE IF @CurrentVersion = 2
                BEGIN
                    -- Revert EngineCapacity data type back to DECIMAL(10,2)
                    EXEC sp_Revert_ModifyColumnType_EngineCapacity;
                END

                -- Decrement the version after reverting the changes
                SET @CurrentVersion = @CurrentVersion - 1;

                -- Update the current version in the SchemaVersion table
                UPDATE SchemaVersion SET CurrentVersion = @CurrentVersion;
                PRINT 'Downgrade to version ' + CAST(@CurrentVersion AS NVARCHAR(10)) + ' completed.';
            END
        END

        -- Commit the transaction if all operations succeeded
        COMMIT TRANSACTION;
        PRINT 'Database schema updated successfully.';
    END TRY
    BEGIN CATCH
        -- Rollback the transaction if any error occurred
        ROLLBACK TRANSACTION;
        PRINT 'Error occurred while updating the database schema.';
        THROW;
    END CATCH
END;
GO


-- Upgrade the database schema to version 5
EXEC sp_UpdateSchemaToVersion 30;

-- Downgrade the database schema to version 2
EXEC sp_UpdateSchemaToVersion 1;

-- Retrieve the current schema version
SELECT * FROM SchemaVersion;
