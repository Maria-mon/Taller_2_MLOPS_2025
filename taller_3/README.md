## Proyecto ETL y Modelado con Airflow y Docker Compose

Integrantes: María del Mar Montenegro,
Andrés David Gomez Bautista,
Juan Felipe Forero Bocanegra

Este proyecto implementa un pipeline completo que:

- **Limpia** la base de datos.
- **Carga** datos de pingüinos sin preprocesar.
- **Preprocesa** los datos para entrenamiento.
- **Entrena** un modelo de clasificación.
- **Expone** una API para realizar inferencias.

Todos los servicios se orquestan en un único archivo Docker Compose.

## Servicios

- **MySQL**  
  Base de datos para almacenar datos de pingüinos y resultados del preprocesamiento.

- **Airflow**  
  Orquesta los DAGs encargados de:  
  - Borrar el contenido de la base de datos (DAG: *clean_database.py*).  
  - Cargar datos de pingüinos (DAG: *load_penguins.py*).  
  - Preprocesar datos (DAG: *preprocess_data.py*).  
  - Entrenar el modelo (DAG: *train_model.py*).

- **API (Flask)**  
  Servicio expuesto en el puerto 5000 para realizar inferencias a través del endpoint `/predict`.


## Instrucciones de Uso

1. **Clonar el repositorio.**

2. **Levantar los servicios:**  
   Ejecuta en la raíz del proyecto:
   ```bash
   docker-compose up --build -d
   ```
2.1 Iniciar los contenedores:
   ```bash
   docker start taller_3-airflow-webserver-1 taller_3-airflow-scheduler-1 taller_3-airflow-worker-1
   ```

3. **Acceder a Airflow:**  
   - Interfaz web disponible en [http://localhost:9090](http://localhost:9090).
   - Monitorea y dispara los DAGs desde la UI.

4. **Uso de la API:**  
   - Realiza solicitudes POST al endpoint `http://localhost:5000/predict`.
   - Envía un JSON con los campos:
     - `culmen_length_mm` (se renombra a `bill_length_mm`)
     - `culmen_depth_mm` (se renombra a `bill_depth_mm`)
     - `flipper_length_mm`
     - `body_mass_g`
     
   Ejemplo de solicitud:
   metodo: POST
   link: http://localhost:5000/predict
   Headers: Content-Type: application/json

    body: {
      "culmen_length_mm": 50.0,
      "culmen_depth_mm": 15.0,
      "flipper_length_mm": 200.0,
      "body_mass_g": 5000
    }

    Response
    {
        "prediction": "Male"
    }



## Consideraciones

- **Docker Compose:** Todos los servicios (MySQL, Airflow, Redis, Postgres para metadata y la API) se definen en un único archivo `docker-compose.yml`.

- **Programación de DAGs:**  
  - *clean_database* y *preprocess_data*: programados para ejecutarse diariamente.  
  - *load_penguins*: ejecutado una sola vez.  
  - *train_model*: programado semanalmente.

- **Persistencia de Datos:**  
  Las carpetas `models`, `dags`, `logs` y `plugins` se montan como volúmenes para mantener la persistencia y facilitar el desarrollo.

- **Dependencias:**  
  Airflow instala dependencias adicionales (pandas, scikit-learn, numpy, mysql-connector-python, seaborn) para el correcto funcionamiento de los DAGs.

---
