FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el código de la API
COPY . .

# Inicia la aplicación Flask
CMD ["python", "app.py"]