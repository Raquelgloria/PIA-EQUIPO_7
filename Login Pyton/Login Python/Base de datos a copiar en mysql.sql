CREATE DATABASE AGENCIA_AUTOS;
USE AGENCIA_AUTOS;



CREATE TABLE Empleados (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    employeeID INT,
    username VARCHAR(255) NOT NULL,
    userPass VARCHAR(255) NOT NULL,
    charge VARCHAR(255),
    salary DECIMAL(10, 2),
    comisions DECIMAL(10, 2)
);
