Taller 2 - MLOps
Este proyecto contiene una API desarrollada con FastAPI para predecir el sexo de pingüinos (MALE/FEMALE) utilizando distintos modelos de clasificación de Machine Learning. Los modelos están entrenados en JupyterLab y son consumidos por la API. El entorno está completamente orquestado mediante Docker Compose.

Instrucciones para Ejecutar el Proyecto
1. Clonar este repositorio

2. Construir y ejecutar los contenedores
docker-compose up --build

3. FastAPI estará disponible en: http://localhost:8000
Documentación interactiva de la API: http://localhost:8000/docs
JupyterLab estará disponible en: http://localhost:8888

4. Click en Predict/predict, luego en try it out e ingresar los datos para las variables de entrada en los siguientes rangos:

model_name : "knn_model_v1"
             "logistic_regression_model_v3"
             "svm_model_v1"
culmen_length_mm: 32.1 - 59.6
culmen_depth_mm: 13.1 - 21.5
flipper_length_mm: 172 - 231
body_mass_g: 2700 - 6300
