# Usar una imagen base con TensorFlow 2.14 y Python 3.9
FROM jupyter/tensorflow-notebook:python-3.9

# Asegurar que Python es 3.9 o 3.10
RUN python --version

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt /tmp/

# Instalar dependencias
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Exponer el puerto de Jupyter Lab
EXPOSE 8888

# Comando por defecto para iniciar el contenedor en modo desarrollo
CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]