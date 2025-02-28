#Definir función de preprocesameinto
import tensorflow as tf
import tensorflow_transform as tft

# Nombre de la etiqueta (variable objetivo)
LABEL_KEY = "Cover_Type"

# Características numéricas que deben normalizarse
NUMERIC_FEATURE_KEYS = [
    "Elevation", "Aspect", "Slope", "Horizontal_Distance_To_Hydrology", 
    "Vertical_Distance_To_Hydrology", "Horizontal_Distance_To_Roadways", 
    "Hillshade_9am", "Hillshade_Noon", "Hillshade_3pm",
    "Horizontal_Distance_To_Fire_Points"
]

def preprocessing_fn(inputs):
    """Función de preprocesamiento para TFX Transform. Aplica normalización y transformación de características."""
    
    outputs = {}

    # Normalización Min-Max para características numéricas
    for key in NUMERIC_FEATURE_KEYS:
        outputs[key] = tft.scale_to_0_1(tf.cast(inputs[key], tf.float32))  # Convertir a float antes de normalizar

    # Transformar la etiqueta en valores enteros (para entrenamiento)
    outputs[LABEL_KEY] = tf.cast(inputs[LABEL_KEY], tf.int64)

    return outputs




