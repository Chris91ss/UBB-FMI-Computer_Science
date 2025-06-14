IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Lab7WebDB')
BEGIN
    CREATE DATABASE Lab7WebDB;
END
GO

USE Lab7WebDB;
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[documents]') AND type in (N'U'))
BEGIN
    CREATE TABLE documents (
        id INT IDENTITY(1,1) PRIMARY KEY,
        title NVARCHAR(255) NOT NULL,
        author NVARCHAR(255) NOT NULL,
        pages INT NOT NULL,
        type NVARCHAR(50) NOT NULL,
        format NVARCHAR(50) NOT NULL,
        created_at DATETIME DEFAULT GETDATE()
    );
END 


SELECT * FROM documents