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