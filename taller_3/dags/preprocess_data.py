from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import mysql.connector
from datetime import datetime

def preprocess():
    # Conectar y obtener datos de la tabla de pingüinos
    conn = mysql.connector.connect(
        host="mysql",
        user="airflow",
        password="airflow",
        database="airflow_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM penguins")
    data = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(data)

    # Seleccionar y ordenar las columnas correctas
    df = df[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']]
    
    # Convertir 'sex' a valores numéricos (Male = 1, Female = 0)
    df['sex'] = df['sex'].map({'Male': 1, 'Female': 0})

    # Conectar nuevamente para crear la tabla preprocesada
    conn = mysql.connector.connect(
        host="mysql",
        user="airflow",
        password="airflow",
        database="airflow_db"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preprocessed_penguins (
            bill_length_mm FLOAT,
            bill_depth_mm FLOAT,
            flipper_length_mm INT,
            body_mass_g INT,
            sex INT
        )
    """)
    conn.commit()

    # Insertar los datos preprocesados
    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO preprocessed_penguins (bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex) VALUES (%s, %s, %s, %s, %s)",
            (row.bill_length_mm, row.bill_depth_mm, row.flipper_length_mm, row.body_mass_g, row.sex)
        )
    conn.commit()
    conn.close()

with DAG(
    dag_id="preprocess_data",
    start_date=datetime(2025, 3, 8),
    schedule_interval="@daily",
    catchup=False
) as dag:
    preprocess_task = PythonOperator(
        task_id="preprocess",
        python_callable=preprocess
    )

preprocess_task

