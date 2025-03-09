from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Cargar el modelo entrenado con manejo de errores
try:
    with open("/app/models/model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Error al cargar el modelo: {e}")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"error": "El modelo no está disponible"}), 500

        # Obtener los datos del JSON enviado
        data = request.json
        df = pd.DataFrame([data])

        # Renombrar columnas para que coincidan con el modelo
        column_mapping = {
            "culmen_length_mm": "bill_length_mm",
            "culmen_depth_mm": "bill_depth_mm"
        }
        df.rename(columns=column_mapping, inplace=True)

        # Verificar que existan las columnas necesarias
        expected_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
        missing_cols = [col for col in expected_cols if col not in df.columns]
        if missing_cols:
            return jsonify({"error": f"Faltan columnas en la solicitud: {missing_cols}"}), 400

        # Reordenar las columnas según lo que espera el modelo
        df = df[expected_cols]

        # Hacer la predicción
        prediction = model.predict(df)[0]
        predicted_sex = "Male" if prediction == 1 else "Female"

        return jsonify({"prediction": predicted_sex})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

