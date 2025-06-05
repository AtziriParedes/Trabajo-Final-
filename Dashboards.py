import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table
from sqlalchemy import create_engine
import base_de_Datos as bd

COLORES = ['#FE5668', '#FF8D8F', '#FEC1A5', '#B9D394', '#64A002']

def dibujar(data_peliculas: pd.DataFrame):
    data_peliculas["Fecha"] = pd.to_numeric(data_peliculas["Fecha"], errors='coerce')
    data_peliculas = data_peliculas.dropna(subset=["Fecha"])

    top_antiguas = data_peliculas.sort_values("Fecha", ascending=True).head(10)

    min_fecha = top_antiguas["Fecha"].min()
    max_fecha = top_antiguas["Fecha"].max()

    fig_top = px.bar(
        top_antiguas,
        x="Nombre",
        y="Fecha",
        title="Top 10 Películas Más Antiguas",
        color="Nombre",
        color_discrete_sequence=COLORES
    )

    fig_top.update_layout(
        xaxis_title="Película",
        yaxis_title="Año de Lanzamiento",
        yaxis=dict(range=[min_fecha - 1, max_fecha + 1]),
        font=dict(color="#141414")
    )

    # Layout del dashboard
    layout = html.Div([
        html.H2("Películas IMDb", style={"textAlign": "center", "color": "#FE5668"}),
        html.P("Top 10 películas más antiguas en la base de datos.", style={"color": "#141414"}),
        html.Hr(),
        dcc.Graph(figure=fig_top),
        html.H3("Tabla de Películas (más antiguas)", style={"color": "#64A002"}),
        dash_table.DataTable(
            data=top_antiguas.to_dict("records"),
            page_size=10,
            style_header={"backgroundColor": "#FF8D8F", "fontWeight": "bold"},
            style_data={"backgroundColor": "#FEC1A5"},
            style_cell={"textAlign": "left", "padding": "5px"}
        )
    ], style={"backgroundColor": "#B9D394", "padding": "20px"})

    return layout

if __name__ == "__main__":
    conexion = bd.conexion()
    if conexion:
        engine = create_engine('mysql+mysqlconnector://root:12345678@localhost:3306/peli')

        query = """
        SELECT p.nombre AS Nombre, a.anio AS Fecha, r.rating AS Rating,
               d.minutos AS duracion, de.descripcion
        FROM peliculas p
        LEFT JOIN anios a ON p.anio_id = a.id
        LEFT JOIN ratings r ON p.rating_id = r.id
        LEFT JOIN duraciones d ON p.duracion_id = d.id
        LEFT JOIN descripciones de ON p.descripcion_id = de.id
        """

        df_peliculas = pd.read_sql(query, engine)

        app = Dash(__name__)
        app.layout = dibujar(df_peliculas)
        app.run(debug=True)
    else:
        print("No se pudo conectar a la base de datos.")
