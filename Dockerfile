# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar uv 
RUN pip install uv 

# Copiar el archivo de configuración de dependencias (pyproject.toml)
COPY pyproject.toml .

# Instalar las dependencias del proyecto
RUN uv pip install --system .

# Copiar los archivos necesarios
COPY . .

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
