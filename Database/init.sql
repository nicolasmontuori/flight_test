-- creo la base de datos 
CREATE DATABASE testfligoo;

-- me conecto a la base 
\c testfligoo;

CREATE TABLE IF NOT EXISTS testdata (
    flight_date DATE,
    flight_status VARCHAR (200),
    departure_airport VARCHAR (200),
    departure_timezone VARCHAR (200),
    arrival_airport VARCHAR (200),
    arrival_timezone VARCHAR (200),
    arrival_terminal VARCHAR (200),
    airline_name VARCHAR (200),
    flight_number VARCHAR (200)
);