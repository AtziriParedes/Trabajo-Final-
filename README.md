Proyecto IMDD

Este proyecto realiza web scraping de películas de IMDb, guarda los datos en una base de datos MySQL, y permite visualizar dashboards interactivos con Dash, todo controlado desde una interfaz gráfica creada con Tkinter.

FUNCIONALIDADES:

Scraping automático de películas desde IMDD.

Guardado de datos en una base de datos MySQL.

Dashboards interactivos con gráficos en Plotly/Dash.

Interfaz gráfica amigable en Tkinter.

Acceso a dashboards desde el navegador local.

ESTRUCTURA DEL PROYECTO:
proyecto_imdb/
├── base_de_Datos.py → Funciones de conexión e inserción a MySQL
├── codigo.py → Web scraping con Selenium y BeautifulSoup
├── MenuDashboards.py → App principal de Dash con navegación
├── dashboards/
│ ├── dashboard_rating.py → Top 10 películas mejor valoradas
│ └── dashboard_antiguas.py → Top 10 películas más antiguas
├── imagenes/
│ └── CAMARITA.png → Imagen para interfaz Tkinter
├── dataset/
│ └── pelicula.csv → CSV generado por scraping
├── pagina principal.py → Interfaz gráfica con botones (Tkinter)

REQUISITOS DEL SISTEMA:

Tener instalado:

Python 3.8 o superior

MySQL Server (localhost)

Google Chrome


CÓMO EJECUTAR:

Crear la base de datos y tablas en MySQL ejecutando el siguiente script:

CREATE DATABASE IF NOT EXISTS peli;
USE peli;

CREATE TABLE IF NOT EXISTS anios (
id INT AUTO_INCREMENT PRIMARY KEY,
anio INT 
);

CREATE TABLE IF NOT EXISTS ratings (
id INT AUTO_INCREMENT PRIMARY KEY,
rating FLOAT
);

CREATE TABLE IF NOT EXISTS duraciones (
id INT AUTO_INCREMENT PRIMARY KEY,
minutos FLOAT
);

CREATE TABLE IF NOT EXISTS descripciones (
id INT AUTO_INCREMENT PRIMARY KEY,
descripcion VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS peliculas (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(255),
anio_id INT,
rating_id INT,
duracion_id INT,
descripcion_id INT,
FOREIGN KEY (anio_id) REFERENCES anios(id),
FOREIGN KEY (rating_id) REFERENCES ratings(id),
FOREIGN KEY (duracion_id) REFERENCES duraciones(id),
FOREIGN KEY (descripcion_id) REFERENCES descripciones(id)
);

Ejecutar la interfaz gráfica con:
pagina principal.py

Desde la interfaz puedes:

1. Iniciar scraping con Selenium

2. Guardar los datos en la base de datos

3. Lanzar los dashboards interactivos

DASHBOARDS:
Cuando presionas el botón “Dashboard” en la interfaz, se ejecuta el servidor Dash (MenuDashboards.py), que muestra gráficas como:

Top 10 películas mejor calificadas (por rating)

Top 10 películas más antiguas

NOTAS TÉCNICAS:
En la pagina principal de top peliculas utillizamos el formato de "VISTA DETALLADA" que viene en formato de tres lineas con puntitos a lado

Las gráficas usan Plotly Express.

El servidor Dash corre por separado del programa principal usando subprocess.

El scraping usa Selenium con BeautifulSoup.

Los datos se transforman antes de insertarse (conversión de duración, limpieza de ratings, etc.).

AUTOR:
Borquez Gutierrez Karina
Bueno Acosta Ailyn
Carapia Cardenas Armando Daniel
Garcia Armijo Valeria Josselyn
Paredes Dominguez Atziri Zukei

Proyecto final - Universidad Autónoma de Baja California
Licenciatura en Inteligencia de Negocios


