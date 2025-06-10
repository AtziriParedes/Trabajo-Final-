import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import base_de_Datos as db
import  codigo as wb
import pandas as pd
import subprocess
import sys


class peliculassis:
    def __init__(self, root):
        self.root = root
        self.root.title("IMDB")
        self.root.geometry("600x500")
        self.root.config(bg="#d6d691")


        self.label_bienvenida = tk.Label(self.root, text="Bienvenido al menu principal", font=("Impact", 20), bg="#d6d691", fg="#141414",)
        self.label_bienvenida.pack(pady=20)

        self.cargar_imagen_bienvenida()

        boton_config = {
            "width": 20,
            "bg": "#cfcfbe",
            "fg": "#141414",
            "activebackground": "#d4b8f0",
            "relief": "solid",
            "borderwidth": 1,
            "highlightbackground": "#d4b8f0",
            "highlightthickness": 4,
            "padx": 10,
            "pady": 5,
             "font": ("Comic Sans MS", 10, "bold")
        }

        self.btn_capturar = tk.Button(self.root, text="Iniciar recoleccion de datos", command=self.scraping,
                                      **boton_config)
        self.btn_capturar.pack(pady=5)

        self.btn_mostrar = tk.Button(self.root, text="Guardar datos en Mysql", command=self.guardar_en_bd, **boton_config)
        self.btn_mostrar.pack(pady=5)

        self.btn_mostrar = tk.Button(self.root, text="Dashboard", command=self.dash, **boton_config)
        self.btn_mostrar.pack(pady=5)



    def cargar_imagen_bienvenida(self):
        ruta_imagen = os.path.join(os.path.dirname(__file__), "imagenes", "CAMARITA.png")
        try:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((200,150), Image.LANCZOS)
            self.imagen_bienvenida = ImageTk.PhotoImage(imagen)
            label_imagen = tk.Label(self.root, image=self.imagen_bienvenida, bg="#d6d691")
            label_imagen.pack(pady=8)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def scraping(self):
            try:
                wb.IMDB()
                messagebox.showinfo("Éxito", "Web scraping completado. CSV guardado.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error en el scraping:\n{e}")

    def guardar_en_bd(self):
        try:
            conexion = db.conexion()
            if conexion:
                df = pd.read_csv("dataset/pelicula.csv")
                df["duracion_minutos"] = df["duracion"].apply(db.convertir_a_minutos)
                df["Fecha"] = pd.to_numeric(df["Fecha"], errors='coerce')
                df["Rating"] = df["Rating"].str.replace(",", ".")
                df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')

                db.insertar_anios(conexion, df)
                db.insertar_ratings(conexion, df)
                db.importarDuraciones(conexion, df)
                db.insertar_descripciones(conexion, df)
                db.importar_peliculas(conexion, df)
                conexion.close()

                messagebox.showinfo("Éxito", "Datos insertados en la base de datos.")
            else:
                messagebox.showwarning("Conexión fallida", "No se pudo conectar a la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar los datos:\n{e}")

    def dash(self):
        try:
            # esta linea de codigo lo que hace es buscar el archivo del menu para poder ejecutarlo en la pgina principal la usamos en el semestre anterior
            ruta_script_dash = os.path.join(os.path.dirname(__file__), "MenuDashboards.py")

            # esta linea de codigfo Ejecuta el dashboard en otra ventana sin cerrar este programa
            subprocess.Popen([sys.executable, ruta_script_dash])

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el dashboard:\n{e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = peliculassis(root)
    root.mainloop()
