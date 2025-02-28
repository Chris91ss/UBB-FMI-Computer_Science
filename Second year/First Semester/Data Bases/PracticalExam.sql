CREATE DATABASE MuseumToursDataBase;
GO

USE MuseumToursDataBase;
GO

--1.
CREATE TABLE Museums (
    MuseumID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(255) NOT NULL,
    OpeningYear INT NOT NULL,
    City NVARCHAR(100) NOT NULL,
    Country NVARCHAR(100) NOT NULL
);

CREATE TABLE Exhibitions (
    ExhibitionID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(255) NOT NULL,
    Description NVARCHAR(MAX),
    MuseumID INT NOT NULL,
    FOREIGN KEY (MuseumID) REFERENCES Museums(MuseumID)
);

CREATE TABLE Tours (
    TourID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(255) NOT NULL,
    TourDate DATETIME NOT NULL,
    GuideName NVARCHAR(255) NOT NULL,
    TicketPrice DECIMAL(10,2) NOT NULL,
    MuseumID INT NOT NULL,
    FOREIGN KEY (MuseumID) REFERENCES Museums(MuseumID)
);

CREATE TABLE Tourists (
    TouristID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    Gender NVARCHAR(10),
    Age INT
);

CREATE TABLE TourBookings (
    TourID INT NOT NULL,
    TouristID INT NOT NULL,
    NumberOfTickets INT NOT NULL,
    RateAfterVisit INT,
    CONSTRAINT PK_TourTourist PRIMARY KEY (TourID, TouristID),
    FOREIGN KEY (TourID) REFERENCES Tours(TourID),
    FOREIGN KEY (TouristID) REFERENCES Tourists(TouristID)
);


-- 2.
USE MuseumToursDB;
GO
CREATE PROCEDURE AddOrUpdateTourBooking
    @TourID INT,
    @TouristID INT,
    @NumberOfTickets INT,
    @RateAfterVisit INT
AS
BEGIN
    
    IF EXISTS (
        SELECT 1
        FROM TourBookings
        WHERE TourID = @TourID
          AND TouristID = @TouristID
    )
    BEGIN
        UPDATE TourBookings
           SET NumberOfTickets = @NumberOfTickets,
               RateAfterVisit  = @RateAfterVisit
         WHERE TourID = @TourID
           AND TouristID = @TouristID;
    END
    ELSE
    BEGIN
        INSERT INTO TourBookings (TourID, TouristID, NumberOfTickets, RateAfterVisit)
        VALUES (@TourID, @TouristID, @NumberOfTickets, @RateAfterVisit);
    END
END;
GO

USE MuseumToursDB;
GO
EXEC AddOrUpdateTourBooking 1, 1, 1, 1

--3.
USE MuseumToursDB;
GO
CREATE VIEW NationalMuseumOfArtAndScience
AS
SELECT e.Name AS ExhibitionName
FROM Exhibitions e
JOIN Museums m
  ON e.MuseumID = m.MuseumID
WHERE m.Name = 'National Museum of Art and Science';
GO

SELECT *
FROM NationalMuseumOfArtAndScience;


--4.
USE MuseumToursDB;
GO
CREATE FUNCTION GetTouristsWithMoreThan(@m INT)
RETURNS TABLE
AS
RETURN
(
    SELECT t.FirstName,
           t.LastName,
           COUNT(tb.TourID) AS TotalToursBooked
    FROM Tourists t
    INNER JOIN TourBookings tb ON t.TouristID = tb.TouristID
    GROUP BY t.FirstName, t.LastName
    HAVING COUNT(tb.TourID) > @m
);
GO

USE MuseumToursDB;
GO
SELECT * FROM
GetTouristsWithMoreThan(1)
