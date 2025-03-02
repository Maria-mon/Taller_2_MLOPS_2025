# Proyecto: Pipeline de Machine Learning con TFX

## Descripción
Este proyecto crea un contenedor que soporte jupyter-lab en un ambiente de desarrollo. Implementa un pipeline de Machine Learning utilizando TensorFlow Extended (TFX) para procesar y analizar el dataset "Covertype". Incluye la ingesta de datos, preprocesamiento, selección de características y configuración del pipeline con TFX.

## Estructura del Proyecto
- **Subir el contenedor**: Se crean los archivos y requerimeintos necesarios para desarrollar el proyecto en Docker.
- **Limpieza de directorios**: Se eliminan archivos previos para asegurar una ejecución limpia.
- **Descarga de dataset**: Se obtiene el dataset "Covertype" desde una fuente en línea.
- **Carga y exploración de datos**: Se utiliza Pandas para leer y explorar los datos.
- **Selección de características**: Se aplica `SelectKBest` para seleccionar las características más relevantes.
- **Configuración del pipeline con TFX**: Se configura el contexto interactivo y se prepara la ingesta de datos.

## Ejecución

1. Clonar el repositorio para crear  el contenedor.
2. Ejecutar en consola docker-compose up --build para construir el contenedor y caragar los archivos correspondientes.
3. Ejecuta las celdas en orden para descargar, procesar y analizar los datos. (Recordar que al reiniciar el entorno algunas rutas podrian cambiar)

## Notas
- La limpieza de directorios es opcional y solo debe ejecutarse si es necesario reiniciar el entorno.
- La selección de características está configurada para elegir las 5 mejores características del dataset.

-Imagen de falal de maquinas virtuales:
![imagen](https://github.com/user-attachments/assets/5607631a-e8e1-478b-930f-744360e8aa11)

