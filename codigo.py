import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup




def IMDB(pagina):
   manejador = ChromeDriverManager().install()
   s = Service(manejador)
   opc = Options()
   opc.add_argument("--window-size=1020,1200")
   nave = webdriver.Chrome(service=s, options=opc)
   nave.get("https://www.imdb.com/es-es/search/title/?title_type=feature")


   time.sleep(5)


   producto = {"Nombre": [], "Fecha": [], "Rating": [], "duracion": [], "descripcion": []}


   for page_num in range(1, pagina + 1):


       soup = BeautifulSoup(nave.page_source, "html.parser")


       peliculas = soup.find_all("div", class_="sc-995e3276-1 jziSZL dli-parent")


       for item in peliculas:
           titulo = item.find("h3", class_="ipc-title__text")


           if titulo:
               producto["Nombre"].append(titulo.text.strip())
           else:
               producto["Nombre"].append("No disponible")




           rating = item.find("span", class_="ipc-rating-star--rating")
           if rating:
               producto["Rating"].append(rating.text.strip())
           else:
               producto["Rating"].append("No disponible")




           descripcion = item.find("div", class_="ipc-html-content-inner-div")
           if descripcion:
               producto["descripcion"].append(descripcion.text.strip())
           else:
               producto["descripcion"].append("No disponible")


           extra_info = item.find("div", class_="sc-5179a348-6 bnnHxo dli-title-metadata")
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


       try:


           btn = nave.find_element(By.XPATH, "//span[text()='50 más']")
           nave.execute_script("arguments[0].scrollIntoView(true);", btn)
           time.sleep(10)
           btn.click()
           time.sleep(10)


       except:
           print("No se encontró el botón o ya no hay más resultados.")
           break


   nave.quit()


   df = pd.DataFrame(producto)
   df.to_csv("dataset/pelicula.csv", index=False)




def limpieza_datos(df:pd.DataFrame):
   df.head()



   print(df)




if __name__ == "__main__":
   pagina = 6
   IMDB(pagina)
   df = pd.read_csv("dataset/pelicula.csv")
   limpieza_datos(df)

