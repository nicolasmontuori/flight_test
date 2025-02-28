# Real-time Flight Status
The AviationStack API was built to provide a simple way of accessing global aviation data for real-time and historical flights as well as allow customers to tap into an extensive data set of airline routes and other up-to-date aviation-related information. Requests to the REST API are made using a straightforward HTTP GET URL structure and responses are provided in lightweight JSON format. The objective of this project is to construct an ETL for a client in order to query information from the API, clean it, and store the results into a consumable database.

<img src="https://s3-us-west-2.amazonaws.com/fligoo.data-science/TechInterviews/RealTimeFlightStatus/header.jpg"/>

**Take-Home Goals**
- Navigate to https://aviationstack.com/ and create a key for the API and read the documentation to understand how it works. For this exercise, consider only `flight_status = active` and `limit = 100`. We are not interested in acquiring the entire information, just focus on:

```
- Flight date
- Flight status
- Departure
     - Airport
     - Timezone
- Arrival
     - Airport
     - Timezone
     - Terminal
- Airline
     - Name
- Flight
     - Number
```

- Build a docker with the services you think are necessary. The database and the table have to be created when running docker.

```
Database: testfligoo
Table: testdata
```
- Create a process in [Airflow](https://airflow.apache.org) that allows obtaining the information from the API.
- Replace the "/" of the `arrivalTerminal` and `departureTimezone` fields for " - ". E.g: "Asia/Shanghai" to "Asia - Shanghai"
- Insert the information in the database.
- Create a Jupyter notebook to consume the information stored in the database.
- Show the information in a Pandas dataframe
  
**Requirements**
- Python 3.x & Pandas 1.x
- Paying attention to the details and narrative is far way more important than extensive development.
- Once you complete the assessment, share the Git repository link.
- Have a final meeting with the team to discuss the work done in this notebook and answer the questions that could arise.
- Finally, but most important: Have fun!

**Nice to have aspects**
- Environment isolation.
- Code versioning with Git (you are free to publish it on your own Github/Bitbucket account!).
- Show proficiency in Python: By showing good practices in the structure and documentation, usage of several programming paradigms (e.g. imperative, OOP, functional), etc.

**Solution Explanation**
*Etl_Dags.py*
This script defines an Apache Airflow Directed Acyclic Graph (DAG) named flight_status_etl that performs an Extract, Transform, Load (ETL) process for flight data. The DAG consists of two primary tasks: extracting flight data from the AviationStack API and loading it into a PostgreSQL database.

- Prerequisites 
AviationStack API Key: Obtain an API key from AviationStack and set it as the API_KEY variable in the script.
PostgreSQL Database: Ensure a PostgreSQL instance is running and accessible. Update the DB_URL variable with the appropriate connection string.

- Dependencies
pandas: For data manipulation and CSV handling.
sqlalchemy: For database connection and operations.
psycopg2: PostgreSQL database adapter for Python.
requests: To make HTTP requests to the AviationStack API.
apache-airflow: To define and manage the DAG and its tasks.

- DAG Structure
extract_data Task: Fetches active flight data from the AviationStack API and saves it as a CSV file in /tmp/flights_data.csv.

 load_data Task: Reads the CSV file and loads the data into a PostgreSQL table named testdata.

*init.sql*
This sql script creates the testfligoo Database and the testdata table.

*query.ipynb*
Script jupyter notebook that consumes data of the testfligoo database. 

*docker-compose.yaml*
The docker-compose.yml file defines the services required to run PostgreSQL and Airflow. It specifies the configuration for each service, including environment variables, ports, and dependencies, enabling the orchestration of these services in a containerized environment. This setup facilitates the deployment and management of Airflow workflows with a PostgreSQL backend.