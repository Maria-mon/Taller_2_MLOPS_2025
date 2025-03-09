from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import mysql.connector
from datetime import datetime
from seaborn import load_dataset

def load_data():
    df = load_dataset("penguins").dropna()

    conn = mysql.connector.connect(
        host="mysql",
        user="airflow",
        password="airflow",
        database="airflow_db"
    )
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penguins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            species VARCHAR(50),
            island VARCHAR(50),
            bill_length_mm FLOAT,
            bill_depth_mm FLOAT,
            flipper_length_mm INT,
            body_mass_g INT,
            sex VARCHAR(10)
        )
    """)
    conn.commit()

    # Insertar datos en la tabla
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO penguins (species, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (row.species, row.island, row.bill_length_mm, row.bill_depth_mm, row.flipper_length_mm, row.body_mass_g, row.sex)
        )
    conn.commit()
    conn.close()

with DAG(
    dag_id="load_penguins",
    start_date=datetime(2025, 3, 8),
    schedule_interval="@daily",
    catchup=False
) as dag:
    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data
    )

load_task
