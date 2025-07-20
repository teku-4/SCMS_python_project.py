CREATE DATABASE STMS;
GO
USE STMS;
GO

CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    sex VARCHAR(10) NOT NULL,
    department VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    semester INT NOT NULL
);
GO

CREATE TABLE admin (
    admin_id VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    sex VARCHAR(10) NOT NULL,
    position VARCHAR(100) NOT NULL
);
GO

CREATE TABLE Complaints (
    complaint_id INT PRIMARY KEY IDENTITY(1,1),
    student_id VARCHAR(20) NOT NULL,
    admin_id VARCHAR(20) NULL,
    title NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX) NOT NULL,
    category NVARCHAR(50) NOT NULL CHECK (category IN (
        'Academic', 'Hostel', 'Financial', 'Infrastructure', 
        'Faculty', 'Administrative', 'Other'
    )),
    status NVARCHAR(20) NOT NULL DEFAULT 'Open' CHECK (status IN (
        'Open', 'In Progress', 'Resolved', 'Closed', 'Rejected'
    )),
    submission_date DATETIME NOT NULL DEFAULT GETDATE(),
    assigned_date DATETIME NULL,
    resolution_details NVARCHAR(MAX) NULL,
    resolution_date DATETIME NULL,
    priority INT DEFAULT 3 CHECK (priority BETWEEN 1 AND 3),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE NO ACTION,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);
GO