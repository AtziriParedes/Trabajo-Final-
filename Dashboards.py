print("hola mundo")

#dashboard

if __name__ == "__main__":
   pagina = 6
   IMDB(pagina)
   df = pd.read_csv("dataset/pelicula.csv")
   limpieza_datos(df)