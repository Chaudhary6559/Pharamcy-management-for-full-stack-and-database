-- SQL Server schema for Pharmacy Management (inferred from code)

IF DB_ID('DBMSPHARMA') IS NULL
BEGIN
  CREATE DATABASE DBMSPHARMA;
END
GO

USE DBMSPHARMA;
GO

IF OBJECT_ID('dbo.users', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    userRole NVARCHAR(50) NOT NULL,
    name NVARCHAR(200) NOT NULL,
    dob DATE NULL,
    mobile BIGINT NULL,
    email NVARCHAR(256) NULL,
    username NVARCHAR(100) NOT NULL UNIQUE,
    pass NVARCHAR(200) NOT NULL
  );
END
GO

IF OBJECT_ID('dbo.medic', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.medic (
    id INT IDENTITY(1,1) PRIMARY KEY,
    mid NVARCHAR(50) NOT NULL UNIQUE,
    mname NVARCHAR(200) NOT NULL,
    mnumber NVARCHAR(100) NULL,
    mDate DATE NULL,
    eDate DATE NULL,
    quantity BIGINT NOT NULL DEFAULT 0,
    Perunit BIGINT NOT NULL DEFAULT 0
  );

  -- Sample data
  INSERT INTO dbo.medic (mid, mname, mnumber, mDate, eDate, quantity, Perunit)
  VALUES ('M-001','Paracetamol','B123','2024-01-01','2026-01-01',100,5);
END
GO

-- Seed an admin if table empty
IF NOT EXISTS (SELECT 1 FROM dbo.users)
BEGIN
  INSERT INTO dbo.users (userRole, name, dob, mobile, email, username, pass)
  VALUES ('Administrator','System Admin','1990-01-01',NULL,'admin@example.com','root','root');
END
GO
