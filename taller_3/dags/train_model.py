import pandas as pd
import pickle
import mysql.connector
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def load_preprocessed_data():
    conn = mysql.connector.connect(
        host="mysql",
        user="airflow",
        password="airflow",
        database="airflow_db"
    )
    query = "SELECT * FROM preprocessed_penguins"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Guardar datos preprocesados en un CSV en la carpeta models (montada como volumen)
    csv_path = "/opt/airflow/models/preprocessed_penguins.csv"
    df.to_csv(csv_path, index=False)
    print(f"Datos preprocesados guardados en {csv_path}")

def train():
    # Cargar datos preprocesados desde el CSV
    csv_path = "/opt/airflow/models/preprocessed_penguins.csv"
    df = pd.read_csv(csv_path)
    
    # Separar variables independientes y la variable objetivo
    X = df[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
    y = df['sex']

    # Dividir los datos en conjuntos de entrenamiento y validación/test
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Entrenar el modelo de Regresión Logística
    model = LogisticRegression(random_state=42, max_iter=500, C=1, penalty='l2')
    model.fit(X_train, y_train)

    # Evaluar el modelo en validación y test
    y_val_pred = model.predict(X_val)
    print("Validation Accuracy:", accuracy_score(y_val, y_val_pred))
    print("\nValidation Classification Report:\n", classification_report(y_val, y_val_pred))
    
    y_test_pred = model.predict(X_test)
    print("Test Accuracy:", accuracy_score(y_test, y_test_pred))
    print("\nTest Classification Report:\n", classification_report(y_test, y_test_pred))

    # Guardar el modelo en /opt/airflow/models para que la API lo pueda usar
    model_dir = "/opt/airflow/models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"Modelo guardado en {model_path}")

with DAG(
    dag_id="train_model",
    start_date=datetime(2025, 3, 8),
    schedule_interval="@weekly",
    catchup=False
) as dag:
    
    load_data_task = PythonOperator(
        task_id="load_preprocessed_data",
        python_callable=load_preprocessed_data
    )

    train_task = PythonOperator(
        task_id="train",
        python_callable=train
    )

load_data_task >> train_task

