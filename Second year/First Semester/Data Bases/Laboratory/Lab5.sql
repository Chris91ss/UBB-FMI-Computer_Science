-- LAB 5: INDEXES

-- ===============================
-- Step 1: Create Tables and Populate Data
-- ===============================

-- Drop tables if they already exist
IF OBJECT_ID('Tc', 'U') IS NOT NULL DROP TABLE Tc;
IF OBJECT_ID('Tb', 'U') IS NOT NULL DROP TABLE Tb;
IF OBJECT_ID('Ta', 'U') IS NOT NULL DROP TABLE Ta;

-- Create Table Ta
CREATE TABLE Ta (
    aid INT PRIMARY KEY, -- Clustered Index by default
    a2 INT UNIQUE        -- Nonclustered Index
);

-- Create Table Tb
CREATE TABLE Tb (
    bid INT PRIMARY KEY, -- Clustered Index by default
    b2 INT
);

-- Create Table Tc
CREATE TABLE Tc (
    cid INT PRIMARY KEY, -- Clustered Index by default
    aid INT FOREIGN KEY REFERENCES Ta(aid),
    bid INT FOREIGN KEY REFERENCES Tb(bid)
);

-- Insert sample data into Ta
INSERT INTO Ta (aid, a2) VALUES (1, 100), (2, 200), (3, 300);

-- Insert sample data into Tb
INSERT INTO Tb (bid, b2) VALUES (1, 500), (2, 600), (3, 700);

-- Insert sample data into Tc
INSERT INTO Tc (cid, aid, bid) VALUES (1, 1, 1), (2, 2, 2), (3, 3, 3);

-- ===============================
-- Step 2: Queries on Ta for Execution Plan Operators
-- ===============================

-- 1. Clustered Index Scan
SELECT * FROM Ta;

-- 2. Clustered Index Seek
SELECT * FROM Ta WHERE aid = 1;

-- Create Nonclustered Index on a2
CREATE NONCLUSTERED INDEX IX_Ta_a2 ON Ta(a2);

-- 3. Nonclustered Index Scan
SELECT a2 FROM Ta WHERE a2 < 300;

-- 4. Nonclustered Index Seek
SELECT a2 FROM Ta WHERE a2 = 100;

-- 5. Key Lookup
SELECT * FROM Ta WHERE a2 = 100;

-- ===============================
-- Step 3: Query on Tb with Optimization
-- ===============================

-- Initial Query on Tb (likely to cause a table scan)
SELECT * FROM Tb WHERE b2 = 600;

-- Create Nonclustered Index on b2
CREATE NONCLUSTERED INDEX IX_Tb_b2 ON Tb(b2);

-- Optimized Query
SELECT * FROM Tb WHERE b2 = 600;

-- ===============================
-- Step 4: Create a View and Optimize Indexes
-- ===============================

-- Drop the View if it already exists
IF OBJECT_ID('vw_Ta_Tb_Tc', 'V') IS NOT NULL DROP VIEW vw_Ta_Tb_Tc;
GO

-- Create a View that Joins Ta, Tb, and Tc
CREATE VIEW vw_Ta_Tb_Tc AS
SELECT 
    Tc.cid, Tc.aid, Tc.bid, Ta.a2, Tb.b2
FROM Tc
INNER JOIN Ta ON Tc.aid = Ta.aid
INNER JOIN Tb ON Tc.bid = Tb.bid;
GO

-- Query the View (Updated to avoid multi-part identifier issues)
SELECT * 
FROM vw_Ta_Tb_Tc 
WHERE a2 = 100 AND b2 = 600;

-- Add Nonclustered Indexes for Optimization
CREATE NONCLUSTERED INDEX IX_Tc_aid ON Tc(aid);
CREATE NONCLUSTERED INDEX IX_Tc_bid ON Tc(bid);

-- ===============================
-- Step 5: Verify Index Usage
-- ===============================

-- Query to verify if indexes are being used
SELECT * 
FROM vw_Ta_Tb_Tc 
WHERE a2 = 100 AND b2 = 600;
