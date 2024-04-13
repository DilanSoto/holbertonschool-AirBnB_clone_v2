-- Script that prepares a MySQL server for AirBnB Console v2
-- This script will create a database and a user for the AirBnB project
-- Create the database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the user if not exists
-- Create user in localhost identified by 'hbnb_test_pwd'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
Flush privileges;

-- Grant select privileges on performance_schema to the user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
Flush privileges;