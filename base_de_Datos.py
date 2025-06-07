import mysql.connector
import pandas as pd
from mysql.connector import Error

def conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Josva2309',
            database='peli'
        )
        if conexion.is_connected():
            print('Conexión exitosa')
            return conexion
    except Error as ex:
        print('Error durante la conexión', ex)
        return None

def insertar_anios(conexion, df):
    cursor = conexion.cursor()
    for valor in df['Fecha'].dropna().unique():
        try:
            numero = int(valor)
            cursor.execute("INSERT IGNORE INTO anios (anio) VALUES (%s)", (numero,))
        except Exception as e:
            print(f"Error al insertar año {valor}: {e}")
    conexion.commit()
    cursor.close()
    print("Años insertados")

def insertar_ratings(conexion, df):
    cursor = conexion.cursor()
    for valor in df['Rating'].dropna():
        numero = float(valor)
        cursor.execute("INSERT INTO ratings (rating) VALUES (%s)", (numero,))
    conexion.commit()
    cursor.close()
    print("Ratings insertados")

def convertir_a_minutos(duracion):
    if pd.isna(duracion):
        return None
    try:
        if "h" in duracion:
            horas, minutos = duracion.split("h")
            minutos = minutos.replace("m", "").strip()
            return int(horas.strip()) * 60 + int(minutos)
        else:
            return int(duracion.replace("m", "").strip())
    except:
        return None


def importarDuraciones(conexion, df):
    cursor = conexion.cursor()
    for minutos in df['duracion_minutos'].dropna():
        cursor.execute("INSERT INTO duraciones (minutos) VALUES (%s)", (minutos,))
    conexion.commit()
    cursor.close()
    print("Duraciones insertadas con éxito")

def insertar_descripciones(conexion, df):
    cursor = conexion.cursor()
    for descripcion in df['descripcion']:
        texto = descripcion.strip().lower()
        cursor.execute("INSERT IGNORE INTO descripciones (descripcion) VALUES (%s)", (texto,))
    conexion.commit()
    cursor.close()
    print("Descripciones insertadas")

def guardar_id(conexion, tabla, columna):
    cursor = conexion.cursor()
    cursor.execute(f"SELECT id, {columna} FROM {tabla}")
    resultado = {}
    for id_, valor in cursor.fetchall():
        try:
            clave = valor.strip().lower()
        except AttributeError:
            clave = valor
        resultado[clave] = id_
    cursor.close()
    return resultado
def importar_peliculas(conexion, df):

    anios_ =guardar_id(conexion, 'anios', 'anio')
    ratings_ = guardar_id(conexion, 'ratings', 'rating')
    duraciones_ = guardar_id(conexion, 'duraciones', 'minutos')
    descripciones_ = guardar_id(conexion, 'descripciones', 'descripcion')
    cursor = conexion.cursor()
    for _, fila in df.iterrows():
        try:
            nombre = fila['Nombre']
            fecha = fila['Fecha']
            rating = fila['Rating']
            duracion = fila['duracion_minutos']
            descripcion = fila['descripcion']

            if pd.notna(fecha):
                anio = int(fecha)
                anio_id = anios_.get(anio)
            else:
                anio_id = None

            if pd.notna(rating):
                rating = float(str(rating).replace(",", "."))
                rating_id = ratings_.get(rating)
            else:
                rating_id = None

            if pd.notna(duracion):
                duracion_id = duraciones_.get(duracion)
            else:
                duracion_id = None

            if pd.notna(descripcion):
                descripcion_id = descripciones_.get(descripcion.strip().lower())
            else:
                descripcion_id = None

            cursor.execute(
                "INSERT INTO peliculas (nombre, anio_id, rating_id, duracion_id, descripcion_id) VALUES (%s, %s, %s, %s, %s)",
                (nombre, anio_id, rating_id, duracion_id, descripcion_id)
            )


        except Exception as error:
            print(f"Error con la película '{nombre}': {error}")

    conexion.commit()
    cursor.close()
    print("Películas insertadas correctamente.")

if __name__ == "__main__":
    conexion_db = conexion()
    if conexion_db:
        df = pd.read_csv("Dataset/pelicula.csv")

        df["duracion_minutos"] = df["duracion"].apply(convertir_a_minutos)

        # Limpieza básica para convertir datos numéricos
        df["Fecha"] = pd.to_numeric(df["Fecha"], errors='coerce')
        df["Rating"] = df["Rating"].str.replace(",", ".")
        df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')

        insertar_anios(conexion_db, df)
        insertar_ratings(conexion_db, df)  # ← ESTO FALTABA
        importarDuraciones(conexion_db, df)
        insertar_descripciones(conexion_db, df)
        importar_peliculas(conexion_db, df)


        conexion_db.close()




