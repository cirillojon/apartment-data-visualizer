# Notes


## Connect to postgres as super user:
psql -U postgres

## Create DB:
CREATE DATABASE apartments_db;

## Some commands:
\d - descibes a table
\c - connects to a database

## Connect to DB:
\c apartments_db

## View tables:
\dt

## Create table:
CREATE TABLE apartments (
    id SERIAL PRIMARY KEY,
    floorplan_name VARCHAR(255),
    available_units INT,
    bedrooms INT,
    bathrooms INT,
    size_range VARCHAR(255),
    availability_date DATE,
    price MONEY
);


## View details of db:
\d apartments_db


## Add a table for complexes which contains a unique identifier (ID) and the complex name.
Add a foreign key in the apartments table linking each apartment to a complex.

CREATE TABLE complexes (
    complex_id SERIAL PRIMARY KEY,
    complex_name VARCHAR(255)
);

ALTER TABLE apartments 
ADD COLUMN complex_id INT REFERENCES complexes(complex_id);

## Misc

-- Find the complex_id of "AMLI ARC"
SELECT complex_id FROM complexes WHERE complex_name = 'AMLI ARC';

-- Delete all apartment entries related to complex_id 4
DELETE FROM apartments WHERE complex_id = 4;

-- Delete the entry for "AMLI ARC" with complex_id 4
DELETE FROM complexes WHERE complex_id = 4;