from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = 'c5ab66bd901a970d5ac8ff385d51717c'
DB_URL = "postgresql://airflow:airflow@postgres/airflow" 


def extract_data():
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_status=active&limit=100"
    response = requests.get(url)
    data = response.json()
    flights_list = data["data"] # Accedo a la lista de vuelos que está en  la variable data dentro de la clave ["data"]

    flights = []
    for flight in flights_list: # tomo solo los campos requeridos de la variable 'data' y guardarlos en un dataframe 
        flights.append({
            "flight_date": flight.get("flight_date"),
            "flight_status": flight.get("flight_status"),
            "departure_airport": flight.get("departure", {}).get("airport"),
            "departure_timezone": str (flight.get("departure", {}).get("timezone", "")).replace("/", " - "),
            "arrival_airport": flight.get("arrival", {}).get("airport"),
            "arrival_timezone": flight.get("arrival", {}).get("timezone"),
            "arrival_terminal": str(flight.get("arrival", {}).get("terminal") or "").replace("/", " - "),
            "airline_name": flight.get("airline", {}).get("name"),
            "flight_number": flight.get("flight", {}).get("number")
        })

    df_flights = pd.DataFrame(flights) # convierto en un DataFrame de Pandas
    df_flights.to_csv("/tmp/flights_data.csv", index=False)

def load_data():
    df = pd.read_csv("/tmp/flights_data.csv")
    engine = sqlalchemy.create_engine(DB_URL)  
    df.to_sql("testdata", engine, if_exists="replace", index=False)

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 2, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "flight_status_etl",
    default_args=default_args,
    schedule="@daily", 
    catchup=False,
)

extract_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    dag=dag,
)

extract_task >> load_task
