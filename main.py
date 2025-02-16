from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

# Directorio donde se almacenan los modelos
models_dir = "/models"
loaded_models = {}

# Cargar todos los modelos .pkl en la carpeta
if os.path.exists(models_dir):
    for filename in os.listdir(models_dir):
        if filename.endswith(".pkl"):
            model_path = os.path.join(models_dir, filename)
            try:
                model_name = os.path.splitext(filename)[0]  # Nombre del modelo sin la extensión
                loaded_models[model_name] = joblib.load(model_path)
                print(f"Modelo '{model_name}' cargado exitosamente.")
            except Exception as e:
                print(f"Error al cargar el modelo '{filename}': {e}")
else:
    print(f"No se encontró el directorio de modelos en {models_dir}.")

# Aplicación FastAPI
app = FastAPI()

class PredictionInput(BaseModel):
    model_name: str  # Nombre del modelo que se quiere usar para la predicción
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float

@app.post("/predict")
def predict(input_data: PredictionInput):
    # Verificar si el modelo solicitado está cargado
    if input_data.model_name not in loaded_models:
        return {"error": f"Modelo '{input_data.model_name}' no encontrado."}

    model = loaded_models[input_data.model_name]
    data = np.array([[input_data.culmen_length_mm, input_data.culmen_depth_mm,
                      input_data.flipper_length_mm, input_data.body_mass_g]])
    prediction = model.predict(data)[0]
    label = "MALE" if prediction == 1 else "FEMALE"
    
    return {"model_used": input_data.model_name, "prediction": label}
