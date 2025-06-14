-- ================================================
-- A) INITIALIZATION & SEED DATA
-- ================================================

ALTER DATABASE [LAB3MOTORCYCLE] 
    SET ALLOW_SNAPSHOT_ISOLATION ON;
GO

-- 1) Drop existing objects if they exist
IF OBJECT_ID('dbo.MotorcycleAccessories', 'U')     IS NOT NULL DROP TABLE dbo.MotorcycleAccessories;
IF OBJECT_ID('dbo.Accessories',             'U')     IS NOT NULL DROP TABLE dbo.Accessories;
IF OBJECT_ID('dbo.Motorcycles',             'U')     IS NOT NULL DROP TABLE dbo.Motorcycles;
IF OBJECT_ID('dbo.ActionLogs',               'U')     IS NOT NULL DROP TABLE dbo.ActionLogs;
IF OBJECT_ID('dbo.sp_log_changes',          'P')     IS NOT NULL DROP PROCEDURE dbo.sp_log_changes;
GO

-- 2) Core tables
CREATE TABLE Motorcycles (
    MotorcycleID   INT   IDENTITY PRIMARY KEY,
    ModelName      NVARCHAR(200) NOT NULL
);
CREATE TABLE Accessories (
    AccessoryID    INT   IDENTITY PRIMARY KEY,
    AccessoryName  NVARCHAR(200) NOT NULL
);
CREATE TABLE MotorcycleAccessories (
    MotorcycleID   INT NOT NULL REFERENCES Motorcycles(MotorcycleID),
    AccessoryID    INT NOT NULL REFERENCES Accessories(AccessoryID),
    CONSTRAINT PK_MotoAcc PRIMARY KEY (MotorcycleID, AccessoryID)
);
GO

-- 3) Seed tables with 3–4 rows each
INSERT INTO Motorcycles (ModelName) VALUES
  ('Harley-Davidson Sportster'),
  ('Kawasaki Ninja'),
  ('Ducati Panigale'),
  ('BMW R1250');
INSERT INTO Accessories (AccessoryName) VALUES
  ('Windshield'),
  ('Saddlebags'),
  ('LED Lighting'),
  ('GPS Mount');
GO

-- 4) Verify seed
SELECT * FROM Motorcycles;    -- Expect 4 rows
SELECT * FROM Accessories;    -- Expect 4 rows
SELECT * FROM MotorcycleAccessories; -- Expect 0 rows
GO


-- 5) Logging table & proc
CREATE TABLE ActionLogs (
    LogID      INT IDENTITY PRIMARY KEY,
    OldData    NVARCHAR(200),
    NewData    NVARCHAR(200),
    Action     NVARCHAR(200),
    LogDate    DATETIME DEFAULT GETDATE()
);
GO

CREATE PROCEDURE sp_log_changes
    @OldData NVARCHAR(200),
    @NewData NVARCHAR(200),
    @Action  NVARCHAR(200)
AS
BEGIN
    INSERT INTO ActionLogs (OldData, NewData, Action)
    VALUES (@OldData, @NewData, @Action);
END;
GO

SELECT * FROM ActionLogs;     -- Expect 0 rows


-- ================================================
-- B) GRADE 3: FULL ROLLBACK ON FAILURE
-- ================================================
CREATE OR ALTER PROCEDURE AddMotorcycleAndAccessory_FullRollback
    @ModelName NVARCHAR(200),
    @AccessoryName NVARCHAR(200)
AS
BEGIN
    -- Validate inputs
    IF @ModelName IS NULL OR LTRIM(RTRIM(@ModelName)) = ''
        THROW 51000, 'ModelName must not be null or empty', 1;
    IF @AccessoryName IS NULL OR LTRIM(RTRIM(@AccessoryName)) = ''
        THROW 51001, 'AccessoryName must not be null or empty', 1;

    BEGIN TRANSACTION;
    BEGIN TRY
        -- Insert motorcycle
        INSERT INTO Motorcycles (ModelName) VALUES (@ModelName);
        DECLARE @MotorcycleID INT = SCOPE_IDENTITY();
        EXEC sp_log_changes NULL, @ModelName, 'Inserted Motorcycle';

        -- Insert accessory
        INSERT INTO Accessories (AccessoryName) VALUES (@AccessoryName);
        DECLARE @AccessoryID INT = SCOPE_IDENTITY();
        EXEC sp_log_changes NULL, @AccessoryName, 'Inserted Accessory';

        -- Link motorcycle & accessory
        INSERT INTO MotorcycleAccessories (MotorcycleID, AccessoryID)
        VALUES (@MotorcycleID, @AccessoryID);
        EXEC sp_log_changes @ModelName, @AccessoryName, 'Linked Motorcycle and Accessory';

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- propagate error
    END CATCH;
END;
GO

-- Test Cases for Grade 3:
-- 1) Success scenario
--    EXEC AddMotorcycleAndAccessory_FullRollback 'Triumph Bonneville', 'Windshield';
--    Expect: new rows in Motorcycles, Accessories, MotorcycleAccessories, and corresponding ActionLogs.
-- 2) Failure scenario (invalid name)
--    EXEC AddMotorcycleAndAccessory_FullRollback NULL, 'GPS Mount';
--    Expect: error thrown, no rows inserted in any table.

/*
SELECT * FROM Motorcycles;
SELECT * FROM Accessories;
SELECT * FROM MotorcycleAccessories;
SELECT * FROM ActionLogs;
*/

-- ================================================
-- C) GRADE 5: PARTIAL COMMIT ON FAILURE
-- ================================================
CREATE OR ALTER PROCEDURE AddMotorcycleAndAccessory_PartialCommit
    @ModelName NVARCHAR(200),
    @AccessoryName NVARCHAR(200)
AS
BEGIN
    DECLARE @Errors INT = 0;
    DECLARE @MotorcycleID INT;
    DECLARE @AccessoryID INT;

    -- Try add motorcycle
    BEGIN TRY
        IF @ModelName IS NULL OR LTRIM(RTRIM(@ModelName)) = ''
            THROW 52000, 'ModelName must not be null or empty', 1;
        INSERT INTO Motorcycles (ModelName) VALUES (@ModelName);
        SET @MotorcycleID = SCOPE_IDENTITY();
        EXEC sp_log_changes NULL, @ModelName, 'Inserted Motorcycle';
    END TRY
    BEGIN CATCH
        SET @Errors += 1;
    END CATCH;

    -- Try add accessory
    BEGIN TRY
        IF @AccessoryName IS NULL OR LTRIM(RTRIM(@AccessoryName)) = ''
            THROW 52001, 'AccessoryName must not be null or empty', 1;
        INSERT INTO Accessories (AccessoryName) VALUES (@AccessoryName);
        SET @AccessoryID = SCOPE_IDENTITY();
        EXEC sp_log_changes NULL, @AccessoryName, 'Inserted Accessory';
    END TRY
    BEGIN CATCH
        SET @Errors += 1;
    END CATCH;

    -- Link only if both inserted successfully
    IF @Errors = 0
    BEGIN
        BEGIN TRY
            INSERT INTO MotorcycleAccessories (MotorcycleID, AccessoryID)
            VALUES (@MotorcycleID, @AccessoryID);
            EXEC sp_log_changes @ModelName, @AccessoryName, 'Linked Motorcycle and Accessory';
        END TRY
        BEGIN CATCH
            -- swallow linking errors
        END CATCH;
    END;
END;
GO

-- Test Cases for Grade 5:
-- 1) Both valid: expect all inserted and linked.
--    EXEC AddMotorcycleAndAccessory_PartialCommit 'Royal Enfield Bullet', 'GPS Mount';
-- 2) Accessory invalid: expect only motorcycle inserted, accessory error, no link.
--    EXEC AddMotorcycleAndAccessory_PartialCommit 'BMW GS', NULL;

/*
SELECT * FROM Motorcycles;
SELECT * FROM Accessories;
SELECT * FROM MotorcycleAccessories;
SELECT * FROM ActionLogs;
*/

-- ================================================
-- D) GRADE 9: PESSIMISTIC CONCURRENCY ISSUES & SOLUTIONS
-- ================================================

-- 1) Dirty Read Example
-- 
-- Session 1:
BEGIN TRAN;
UPDATE Motorcycles SET ModelName = 'DirtyReadTest' WHERE MotorcycleID = 1;
WAITFOR DELAY '00:00:10';
ROLLBACK TRAN;
-- Session 2 (READ UNCOMMITTED):
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN TRAN;
SELECT * FROM Motorcycles WHERE MotorcycleID = 1; -- sees uncommitted change
COMMIT TRAN;
-- Solution: use READ COMMITTED or higher
--   SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- 2) Non-Repeatable Read Example
-- Session 1:
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN TRAN;
SELECT * FROM Accessories WHERE AccessoryID = 1;
WAITFOR DELAY '00:00:10';
SELECT * FROM Accessories WHERE AccessoryID = 1; -- may see change
COMMIT TRAN;
-- Session 2:
UPDATE Accessories SET AccessoryName = 'NonRepeatableTest' WHERE AccessoryID = 1;
-- Solution: use REPEATABLE READ
--   SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- 3) Phantom Read Example
-- Session 1:
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRAN;
SELECT * FROM MotorcycleAccessories WHERE MotorcycleID = 2;
WAITFOR DELAY '00:00:10';
SELECT * FROM MotorcycleAccessories WHERE MotorcycleID = 2; -- may see new rows (phantoms)
COMMIT TRAN;
-- Session 2:
INSERT INTO MotorcycleAccessories (MotorcycleID, AccessoryID) VALUES (2, 3);
-- Solution: use SERIALIZABLE
--   SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 4) Deadlock Example
-- Console 1:
BEGIN TRAN;
UPDATE Motorcycles SET ModelName='DL1' WHERE MotorcycleID=3;
WAITFOR DELAY '00:00:10';
UPDATE Accessories SET AccessoryName='DL-Test' WHERE AccessoryID=2;
COMMIT TRAN;
-- Console 2:
BEGIN TRAN;
UPDATE Accessories SET AccessoryName='DL2' WHERE AccessoryID=2;
WAITFOR DELAY '00:00:10';
UPDATE Motorcycles SET ModelName='DL-Test2' WHERE MotorcycleID=3;
COMMIT TRAN;
-- Solution: enforce consistent ordering of resource access
BEGIN TRAN;
UPDATE Motorcycles SET ModelName='DL-Test2' WHERE MotorcycleID=3;
WAITFOR DELAY '00:00:10';
UPDATE Accessories SET AccessoryName='DL2' WHERE AccessoryID=2;
COMMIT TRAN;

-- ================================================
-- E) GRADE 10: OPTIMISTIC ISOLATION UPDATE CONFLICT
-- ================================================
-- Session 1:
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRAN;
SELECT * FROM Motorcycles WHERE MotorcycleID=4;
WAITFOR DELAY '00:00:10';
UPDATE Motorcycles SET ModelName='SnapshotTest1' WHERE MotorcycleID=4;
COMMIT TRAN;
-- Session 2:
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRAN;
SELECT * FROM Motorcycles WHERE MotorcycleID=4;
WAITFOR DELAY '00:00:10';
UPDATE Motorcycles SET ModelName='SnapshotTest2' WHERE MotorcycleID=4;
COMMIT TRAN; -- conflict error: update conflict under snapshot

