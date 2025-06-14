CREATE DATABASE BakeryPerformanceDB;
GO
USE BakeryPerformanceDB;
GO

CREATE TABLE Cities (
    CityID INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(100) NOT NULL,
    County NVARCHAR(100),
    Country NVARCHAR(100)
);

CREATE TABLE FavouriteBakeries (
    BakeryID INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(100) NOT NULL,
    StartupYear INT,
    NumberOfStars INT,
    CityID INT NOT NULL,
    FOREIGN KEY (CityID) REFERENCES Cities(CityID)
);

CREATE TABLE Clients (
    ClientID INT PRIMARY KEY IDENTITY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    Gender CHAR(1),
    Age INT,
    FavouriteBakeryID INT,
    FOREIGN KEY (FavouriteBakeryID) REFERENCES FavouriteBakeries(BakeryID)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(100),
    Weight DECIMAL(10,2),
    Price DECIMAL(10,2)
);

CREATE TABLE BakeryProducts (
    BakeryID INT,
    ProductID INT,
    ExpirationDate DATE,
    PRIMARY KEY (BakeryID, ProductID),
    FOREIGN KEY (BakeryID) REFERENCES FavouriteBakeries(BakeryID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);


INSERT INTO Cities (Name, County, Country)
VALUES ('Cluj-Napoca', 'Cluj', 'Romania');

INSERT INTO FavouriteBakeries (Name, StartupYear, NumberOfStars, CityID)
VALUES ('Sweet Bakery', 2015, 4, 1);

SELECT * FROM FavouriteBakeries