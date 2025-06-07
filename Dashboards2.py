import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table
from sqlalchemy import create_engine
import base_de_Datos as bd

COLORES = ['#FE5668', '#FF8D8F', '#FEC1A5', '#B9D394', '#64A002']

def dashboard_rating():
    conexion = bd.conexion()
    if conexion:
        engine = create_engine("mysql+mysqlconnector://root:Josva2309@localhost:3306/peli")

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
        df_peliculas["Rating"] = pd.to_numeric(df_peliculas["Rating"], errors='coerce')
        df_peliculas = df_peliculas.dropna(subset=["Rating"])

        top_rating = df_peliculas.sort_values("Rating", ascending=False).head(10)

        fig_top = px.bar(
            top_rating,
            x="Nombre",
            y="Rating",
            title="Top 10 Películas con Mejor Rating",
            color="Nombre",
            color_discrete_sequence=COLORES
    )
        fig_top.update_layout(
            xaxis_title="Película",
            yaxis_title="Rating",
            font=dict(color="#141414")
    )

        layout = html.Div([
            html.H2("Películas IMDb", style={"textAlign": "center", "color": "#FE5668"}),
            html.P("Top 10 películas mejor valoradas en la base de datos.", style={"color": "#141414"}),
            html.Hr(),
            dcc.Graph(figure=fig_top),
            html.H3("Tabla de Películas", style={"color": "#64A002"}),
            dash_table.DataTable(
                data=df_peliculas.to_dict("records"),
                page_size=10,
                style_header={"backgroundColor": "#FF8D8F", "fontWeight": "bold"},
                style_data={"backgroundColor": "#FEC1A5"},
                style_cell={"textAlign": "left", "padding": "5px"}
            )
        ], style={"backgroundColor": "#B9D394", "padding": "20px"})

        return layout

if __name__ == "__main__":
        app = Dash(__name__)
        app.layout = dashboard_rating()
        app.run(debug=True)
