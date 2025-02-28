-- Insert into Motorcycles table
INSERT INTO Motorcycles (Model, Brand, EngineCapacity, Price, Year, StockQuantity) 
VALUES 
('Ninja ZX-6R', 'Kawasaki', 636, 9999.99, 2023, 5),
('CBR1000RR', 'Honda', 1000, 15500.00, 2022, 3),
('MT-09', 'Yamaha', 847, 8999.99, 2023, 8),
('Street Triple', 'Triumph', 765, 9500.00, 2022, 6),
('Panigale V4', 'Ducati', 1103, 22000.00, 2024, 2);

-- Insert into Customers table
INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) 
VALUES 
('John', 'Doe', 'john.doe@example.com', '555-1234', '123 Main St'),
('Jane', 'Smith', 'jane.smith@example.com', '555-5678', '456 Oak Ave'),
('Mike', 'Johnson', 'mike.johnson@example.com', '555-8765', '789 Pine Rd'),
('Sara', 'Williams', 'sara.williams@example.com', '555-4321', '101 Maple Dr'),
('Chris', 'Davis', 'chris.davis@example.com', '555-1122', '102 Elm St');

-- Insert into Dealerships table
INSERT INTO Dealerships (Name, Location, ContactNumber) 
VALUES 
('Motorcycle Heaven', 'New York, NY', '212-555-7890'),
('Speed King Motors', 'Los Angeles, CA', '323-555-1234'),
('Bikes R Us', 'Miami, FL', '305-555-9876'),
('Cycle World', 'Austin, TX', '512-555-6543'),
('Performance Bikes', 'Chicago, IL', '312-555-4321');

-- Insert into Employees table
INSERT INTO Employees (FirstName, LastName, Position, Salary, DealershipID) 
VALUES 
('David', 'Brown', 'Sales Manager', 55000.00, 1),
('Emily', 'Wilson', 'Mechanic', 40000.00, 2),
('Daniel', 'Moore', 'Sales Associate', 35000.00, 3),
('Anna', 'Taylor', 'Receptionist', 32000.00, 4),
('Michael', 'Anderson', 'General Manager', 60000.00, 5);

-- Insert into Suppliers table
INSERT INTO Suppliers (SupplierName, ContactNumber, Email, Address) 
VALUES 
('Motorbike Supplies Ltd', '555-3333', 'info@motorbikesupplies.com', '101 Bike St, London, UK'),
('Performance Parts Inc', '555-4444', 'sales@performanceparts.com', '202 Speed Rd, Munich, DE'),
('Superbikes Wholesale', '555-5555', 'contact@superbikeswholesale.com', '303 Fast Ln, Tokyo, JP');

-- Insert into Sales table
INSERT INTO Sales (SaleDate, TotalAmount, CustomerID, DealershipID) 
VALUES 
('2024-01-10', 10000.00, 1, 1),
('2024-02-15', 23000.00, 2, 2),
('2024-03-20', 8500.00, 3, 3),
('2024-04-25', 14500.00, 4, 4),
('2024-05-05', 19000.00, 5, 5);

-- Insert into SalesDetails table
INSERT INTO SalesDetails (SaleID, MotorcycleID, Quantity, UnitPrice) 
VALUES 
(1, 1, 1, 9999.99),
(2, 5, 1, 22000.00),
(3, 3, 1, 8999.99),
(4, 4, 1, 9500.00),
(5, 2, 1, 15500.00);

-- Insert into SupplierOrders table
INSERT INTO SupplierOrders (OrderDate, SupplierID, DealershipID) 
VALUES 
('2023-12-01', 1, 1),
('2023-12-15', 2, 2),
('2023-12-20', 3, 3),
('2024-01-05', 1, 4),
('2024-01-10', 2, 5);

-- Insert into OrderDetails table
INSERT INTO OrderDetails (SupplierOrderID, MotorcycleID, Quantity, PricePerUnit) 
VALUES 
(1, 1, 5, 9500.00),
(2, 2, 3, 15000.00),
(3, 3, 8, 9000.00),
(4, 4, 6, 9300.00),
(5, 5, 2, 21000.00);

-- Insert into MaintenanceServices table
INSERT INTO MaintenanceServices (ServiceType, ServiceDate, MotorcycleID, EmployeeID, ServiceCost) 
VALUES 
('Oil Change', '2024-01-15', 1, 2, 150.00),
('Engine Repair', '2024-02-20', 3, 3, 500.00),
('Brake Replacement', '2024-03-10', 2, 4, 300.00),
('Tire Change', '2024-04-05', 5, 5, 250.00),
('General Service', '2024-05-01', 4, 1, 200.00);

-- Attempt to insert into SalesDetails with a non-existing SaleID (violates referential integrity)
INSERT INTO SalesDetails (SaleID, MotorcycleID, Quantity, UnitPrice)
VALUES (999, 2, 1, 10000.00); -- SaleID 999 does not exist




-- Update Motorcycles based on certain conditions
UPDATE Motorcycles
SET Price = Price * 1.05
WHERE NOT (StockQuantity >= 5 OR Year < 2023);

-- Update Customers, setting Phone to NULL where certain conditions are met
UPDATE Customers
SET Phone = NULL
WHERE NOT (Email NOT LIKE '%example.com' OR FirstName <> 'John');

-- Update Employees' salary where conditions match
UPDATE Employees
SET Salary = Salary + 5000
WHERE (Position = 'Mechanic' OR Position = 'Sales Associate') AND NOT (Salary > 50000);




-- Delete services that are between specific ServiceIDs and have a ServiceType that is not NULL
DELETE FROM MaintenanceServices
WHERE ServiceID BETWEEN 1 AND 10
AND ServiceCost >= 200
AND ServiceType IS NOT NULL
AND NOT (ServiceType LIKE '%Oil%');

-- Delete all services where ServiceType contains the word "Oil" and ServiceCost is outside the range of 150 to 250
DELETE FROM MaintenanceServices
WHERE ServiceType LIKE '%Oil%'
AND NOT (ServiceCost BETWEEN 150 AND 250);

-- Delete sales records where TotalAmount is less than 9000 or CustomerID is NULL
DELETE FROM Sales
WHERE NOT (TotalAmount >= 9000 AND CustomerID IS NOT NULL);



-- Using UNION to find models and brands that either have a price greater than 10,000 or a low stock quantity (less than 3)
SELECT Model, Brand FROM Motorcycles WHERE Price > 10000
UNION
SELECT Model, Brand FROM Motorcycles WHERE StockQuantity < 3;

-- Using OR in the WHERE clause to achieve the same result
SELECT Model, Brand FROM Motorcycles WHERE Price > 10000 OR StockQuantity < 3;

-- Using UNION ALL to find all motorcycles from 2023 onward, as well as any motorcycles priced below 10,000 (including duplicates if any)
SELECT Model, Year FROM Motorcycles WHERE Year >= 2023
UNION ALL
SELECT Model, Year FROM Motorcycles WHERE Price < 10000;




-- Using INTERSECT to find MotorcycleIDs that are present in both SalesDetails and OrderDetails
SELECT MotorcycleID FROM SalesDetails
INTERSECT
SELECT MotorcycleID FROM OrderDetails;

-- Using IN and INTERSECT to identify SupplierIDs that appear in both SupplierOrders and OrderDetails
SELECT SupplierID FROM Suppliers WHERE SupplierID IN (
    SELECT SupplierID FROM SupplierOrders
    INTERSECT
    SELECT SupplierID FROM (
        SELECT SupplierOrders.SupplierID
        FROM SupplierOrders
        INNER JOIN OrderDetails ON SupplierOrders.SupplierOrderID = OrderDetails.SupplierOrderID
    ) AS SupplierOrderDetails
);




-- Using EXCEPT to find MotorcycleIDs listed in SalesDetails but not in MaintenanceServices
SELECT MotorcycleID FROM SalesDetails
EXCEPT
SELECT MotorcycleID FROM MaintenanceServices;

-- Using NOT IN to find motorcycles in inventory that haven’t been sold yet
SELECT MotorcycleID FROM Motorcycles
WHERE MotorcycleID NOT IN (SELECT MotorcycleID FROM SalesDetails);




-- INNER JOIN to list sales records along with customer names
SELECT s.SaleID, s.SaleDate, c.FirstName, c.LastName
FROM Sales s
INNER JOIN Customers c ON s.CustomerID = c.CustomerID;

-- LEFT JOIN to list all dealerships, including those without employees
SELECT d.Name, e.FirstName, e.LastName
FROM Dealerships d
LEFT JOIN Employees e ON d.DealershipID = e.DealershipID;

-- RIGHT JOIN to show all supplier orders along with supplier names
SELECT s.SupplierName, so.OrderDate
FROM Suppliers s
RIGHT JOIN SupplierOrders so ON s.SupplierID = so.SupplierID;

-- FULL JOIN to list all motorcycles, sales details, and sales records
SELECT m.Model, sd.Quantity, s.SaleDate
FROM Motorcycles m
FULL JOIN SalesDetails sd ON m.MotorcycleID = sd.MotorcycleID
FULL JOIN Sales s ON sd.SaleID = s.SaleID;

-- Joining two many-to-many relationships: Sales and Motorcycles via SalesDetails, and SupplierOrders and Motorcycles via OrderDetails
SELECT s.SaleID, sd.MotorcycleID, so.SupplierOrderID
FROM Sales s
INNER JOIN SalesDetails sd ON s.SaleID = sd.SaleID
INNER JOIN Motorcycles m ON sd.MotorcycleID = m.MotorcycleID
INNER JOIN OrderDetails od ON m.MotorcycleID = od.MotorcycleID
INNER JOIN SupplierOrders so ON od.SupplierOrderID = so.SupplierOrderID;




-- Using IN with a subquery to list all sales records for customers whose first name starts with 'J'
SELECT CustomerID, TotalAmount
FROM Sales
WHERE CustomerID IN (
    SELECT CustomerID FROM Customers WHERE FirstName LIKE 'J%'
);

-- Nested subquery in WHERE clause to find employees working at dealerships in New York
SELECT EmployeeID, Position FROM Employees
WHERE DealershipID IN (
    SELECT DealershipID FROM Dealerships WHERE Name IN (
        SELECT Name FROM Dealerships WHERE Location LIKE '%NY%'
    )
);




-- Simple EXISTS query to check for customers who have made at least one purchase
SELECT FirstName, LastName FROM Customers
WHERE EXISTS (
    SELECT * FROM Sales WHERE Sales.CustomerID = Customers.CustomerID
);

-- EXISTS with nested subquery to find dealerships that have employees
SELECT DealershipID, Name FROM Dealerships
WHERE EXISTS (
    SELECT * FROM Employees WHERE Employees.DealershipID = Dealerships.DealershipID
);




-- Subquery in FROM clause to calculate the average price of recent models
SELECT AVG(Price) AS AvgPrice FROM (
    SELECT Price FROM Motorcycles WHERE Year >= 2022
) AS RecentModels;

-- Subquery in FROM clause to find total sales revenue grouped by dealership
SELECT DealershipID, TotalSales, TotalSales * 0.1 AS Commission FROM (
    SELECT DealershipID, SUM(TotalAmount) AS TotalSales FROM Sales GROUP BY DealershipID
) AS SalesSummary;




-- GROUP BY without HAVING to count the number of employees at each dealership
SELECT DealershipID, COUNT(*) AS NumEmployees
FROM Employees
GROUP BY DealershipID;

-- GROUP BY with HAVING to find dealerships with more than two sales and highest sale amount
SELECT DealershipID, COUNT(*) AS NumSales, MAX(TotalAmount) AS MaxSale
FROM Sales
GROUP BY DealershipID
HAVING COUNT(*) > 2;

-- GROUP BY with HAVING and a subquery to find motorcycles with average maintenance cost above overall average
SELECT MotorcycleID, AVG(ServiceCost) AS AvgCost
FROM MaintenanceServices
GROUP BY MotorcycleID
HAVING AVG(ServiceCost) > (
    SELECT AVG(ServiceCost) FROM MaintenanceServices
);

-- GROUP BY with HAVING and subquery to identify dealerships with total sales above average
SELECT DealershipID, SUM(TotalAmount) AS TotalSales, MIN(TotalAmount) AS MinSale
FROM Sales
GROUP BY DealershipID
HAVING SUM(TotalAmount) > (
    SELECT AVG(TotalAmount) FROM Sales
);




-- Using ANY to find MotorcycleIDs with a price lower than at least one motorcycle with stock quantity greater than 3
SELECT MotorcycleID FROM Motorcycles
WHERE Price < ANY (SELECT Price FROM Motorcycles WHERE StockQuantity > 3);

-- Using ALL to find MotorcycleIDs with a price higher than all motorcycles made before 2023
SELECT MotorcycleID FROM Motorcycles
WHERE Price > ALL (SELECT Price FROM Motorcycles WHERE Year < 2023);

-- Using ANY to find MotorcycleIDs with stock quantity lower than at least one motorcycle with a price above 10000
SELECT MotorcycleID FROM Motorcycles
WHERE StockQuantity < ANY (SELECT StockQuantity FROM Motorcycles WHERE Price > 10000);

-- Using ALL to find MotorcycleIDs with stock quantity higher than all motorcycles manufactured in 2022
SELECT MotorcycleID FROM Motorcycles
WHERE StockQuantity > ALL (SELECT StockQuantity FROM Motorcycles WHERE Year = 2022);

-- Using MAX to find MotorcycleIDs with a price lower than the maximum price of motorcycles with stock quantity greater than 3
SELECT MotorcycleID FROM Motorcycles
WHERE Price < (SELECT MAX(Price) FROM Motorcycles WHERE StockQuantity > 3);

-- Using MIN to find MotorcycleIDs with a price higher than the minimum price of motorcycles manufactured before 2023
SELECT MotorcycleID FROM Motorcycles
WHERE Price > (SELECT MIN(Price) FROM Motorcycles WHERE Year < 2023);

-- Using IN to find MotorcycleIDs with stock quantities equal to any motorcycle with a price above 10000
SELECT MotorcycleID FROM Motorcycles
WHERE StockQuantity IN (SELECT StockQuantity FROM Motorcycles WHERE Price > 10000);

-- Using NOT IN to find MotorcycleIDs with stock quantities not present among motorcycles manufactured in 2022
SELECT MotorcycleID FROM Motorcycles
WHERE StockQuantity NOT IN (SELECT StockQuantity FROM Motorcycles WHERE Year = 2022);




-- Arithmetic expressions in SELECT clause to calculate discounted price
SELECT MotorcycleID, Model, Price, Price * 0.9 AS DiscountedPrice FROM Motorcycles;

-- List all employees with their annual salaries
SELECT EmployeeID, FirstName, LastName, Salary * 12 AS AnnualSalary FROM Employees;

-- Calculate average discounted price of recent models
SELECT AVG(DiscountedPrice) AS AvgDiscountedPrice FROM (
    SELECT Price * 0.9 AS DiscountedPrice FROM Motorcycles WHERE Year >= 2022
) AS RecentModels;

-- Conditions with AND, OR, NOT, and parentheses in WHERE clause to find specific motorcycles
SELECT * FROM Motorcycles
WHERE (Year >= 2023 OR Price < 10000) AND NOT (Year >= 2023 AND Price < 10000);

-- Find customers whose first name starts with 'J' but not 'John'
SELECT * FROM Customers
WHERE FirstName LIKE 'J%' AND NOT FirstName = 'John';

-- Find employees who are 'Mechanic' or 'Sales Associate' and have a salary <= 50000
SELECT * FROM Employees
WHERE (Position = 'Mechanic' OR Position = 'Sales Associate') AND Salary <= 50000;

-- Using DISTINCT to list distinct brands of motorcycles
SELECT DISTINCT Brand FROM Motorcycles;

-- Using DISTINCT to list distinct positions held by employees
SELECT DISTINCT Position FROM Employees;

-- Using DISTINCT to list distinct locations of dealerships
SELECT DISTINCT Location FROM Dealerships;

-- Using ORDER BY to list motorcycles ordered by price descending
SELECT * FROM Motorcycles ORDER BY Price DESC;

-- Using ORDER BY to list sales ordered by total amount ascending
SELECT * FROM Sales ORDER BY TotalAmount ASC;

-- Using TOP to get the top 2 most expensive motorcycles
SELECT TOP 2 * FROM Motorcycles ORDER BY Price DESC;

-- Using TOP to get the top 3 customers with highest total purchases
SELECT TOP 3 CustomerID, SUM(TotalAmount) AS TotalPurchases
FROM Sales
GROUP BY CustomerID
ORDER BY TotalPurchases DESC;

-- Final data retrieval from all tables
SELECT * FROM Motorcycles;
SELECT * FROM Customers;
SELECT * FROM Dealerships;
SELECT * FROM Employees;
SELECT * FROM Suppliers;
SELECT * FROM Sales;
SELECT * FROM SalesDetails;
SELECT * FROM SupplierOrders;
SELECT * FROM OrderDetails;
SELECT * FROM MaintenanceServices;
