from airflow import DAG
from airflow.operators.python import PythonOperator
import mysql.connector
from datetime import datetime

def clean_db():
    conn = mysql.connector.connect(
        host="mysql",
        user="airflow",
        password="airflow",
        database="airflow_db"
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM penguins")
    conn.commit()
    conn.close()

with DAG(
    dag_id="clean_database",
    start_date=datetime(2025, 3, 8),
    schedule_interval="@daily",
    catchup=False
) as dag:
    clean_task = PythonOperator(
        task_id="clean_db",
        python_callable=clean_db
    )

clean_task
