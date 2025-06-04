## pagina para agregar la base de datos normalizada
#prueba para ver si si funciona

import pandas as pd
import sqlite3


import csv
import mysql.connector

# Configura tu conexión MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Angelise21",
    database="progfinal",
    port="3307"
)

cursor = conexion.cursor()

with open('pelicula.csv', encoding='utf-8') as archivo_csv:
    lector = csv.DictReader(archivo_csv)
    for fila in lector:
        cursor.execute("""
            INSERT INTO peliculas (nombre, anio, rating, duracion_minutos, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """, (fila[' nombrep'], fila['anio'], fila['rating'], fila['duracion_minutos'], fila['descripcion']))

conexion.commit()
cursor.close()
conexion.close()
print("Datos insertados correctamente.")
