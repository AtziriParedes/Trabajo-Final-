import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup

#Al hacer rl wed cambiar a vista detallada que es la figura de tres lineas con puntitos al lado
def IMDB():

    manejador = ChromeDriverManager().install()
    s = Service(manejador)
    opc = Options()
    opc.add_argument("--window-size=1020,1200")
    nave = webdriver.Chrome(service=s, options=opc)
    nave.get("https://www.imdb.com/es-es/chart/top/?ref_=nv_mv_250")

    time.sleep(5)

    producto = {"Nombre": [], "Fecha": [], "Rating": [], "duracion": [], "descripcion": []}


    soup = BeautifulSoup(nave.page_source, "html.parser")

    peliculas = soup.find_all("li", class_="ipc-metadata-list-summary-item")

    for item in peliculas:
        titulo = item.find("h3")

        if titulo:
            texto = titulo.text.strip()
            texto_limpio = texto.split('. ', 1)[-1]
            producto["Nombre"].append(texto_limpio)
        else:
            producto["Nombre"].append("No disponible")

        rating = item.find("span", class_="ipc-rating-star--rating")
        if rating:
            producto["Rating"].append(rating.text.strip())
        else:
            producto["Rating"].append("No disponible")

        descripcion = item.find("div", class_="ipc-html-content ipc-html-content--base sc-7746c29e-0 fypBkQ sttd-plot-container")
        if descripcion:
            producto["descripcion"].append(descripcion.text.strip())
        else:
            producto["descripcion"].append("No disponible")

        extra_info = item.find("div", class_="sc-4b408797-7 fUdAcX dli-title-metadata")
        if extra_info:
            spans = extra_info.find_all("span")

            if len(spans) > 0:
                fecha = spans[0].text.strip()
            else:
                fecha = "No disponible"

            if len(spans) > 1:
                duracion = spans[1].text.strip()
            else:
                duracion = "No disponible"
        else:
            fecha = "No disponible"
            duracion = "No disponible"

        producto["Fecha"].append(fecha)
        producto["duracion"].append(duracion)



    nave.quit()

    df = pd.DataFrame(producto)
    df.to_csv("dataset/pelicula.csv", index=False)



if __name__ == "__main__":
    IMDB()
    df = pd.read_csv("dataset/pelicula.csv")

    print (df)

