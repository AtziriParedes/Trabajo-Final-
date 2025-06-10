import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, Input, Output, callback
from sqlalchemy import create_engine
import base_de_Datos as bd

COLORES = ['#FE5668', '#FF8D8F', '#FEC1A5', '#B9D394', '#64A002']

def dashboard_antiguas():
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

        df = pd.read_sql(query, engine)
        df["Fecha"] = pd.to_numeric(df["Fecha"], errors='coerce')
        df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')
        df["duracion"] = pd.to_numeric(df["duracion"], errors='coerce')
        df = df.dropna(subset=["Fecha"])

        min_cant = 1
        max_cant = 10

        layout = html.Div([
            html.H2("Películas", style={"textAlign": "center", "color": "#FE5668"}),
            html.P("Películas más Antiguas según año de estreno.", style={"color": "#141414"}),
            html.Hr(),

            dbc.Card([
                dbc.CardHeader("Cantidad de películas antiguas a mostrar"),
                dbc.CardBody([
                    dcc.Slider(
                        id="slider-cantidad",
                        min=min_cant,
                        max=max_cant,
                        step=1,
                        value=10,
                        marks={str(i): str(i) for i in range(min_cant, max_cant + 1)},
                        tooltip={"placement": "bottom"}
                    )
                ])
            ], style={"marginBottom": "30px"}),

            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Películas mostradas", className="card-title"),
                    html.H4(id="kpi-total")
                ]), color="#FE5668", inverse=True)),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Duración promedio", className="card-title"),
                    html.H4(id="kpi-duracion")
                ]), color="#64A002", inverse=True)),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Rating promedio", className="card-title"),
                    html.H4(id="kpi-rating")
                ]), color="#FFC32C", inverse=True)),
            ], className="mb-4"),

            dbc.Row([
                dbc.Col(dcc.Graph(id="grafico-antiguas"), md=6),
                dbc.Col(dcc.Graph(id="grafico-dispersion"), md=6)
            ]),

            html.H3("Top películas más antiguas", style={"color": "#64A002"}),
            dash_table.DataTable(
                id="tabla-peliculas",
                page_size=10,
                style_header={"backgroundColor": "#FF8D8F", "fontWeight": "bold"},
                style_data={"backgroundColor": "#FEC1A5"},
                style_cell={"textAlign": "left", "padding": "5px"},
                columns=[
                    {"name": "Nombre", "id": "Nombre"},
                    {"name": "Fecha", "id": "Fecha"},
                    {"name": "Rating", "id": "Rating"},
                    {"name": "Duración (min)", "id": "duracion"},
                    {"name": "Descripción", "id": "descripcion"},
                ]
            )
        ], style={"backgroundColor": "#B9D394", "padding": "20px"})

        return layout
    else:
        return html.Div([
            html.H1("Error de conexión", style={"color": "#FE5668"}),
            html.P("No se pudo conectar a la base de datos.", style={"color": "#141414"})
        ])

@callback(
    Output("kpi-total", "children"),
    Output("kpi-duracion", "children"),
    Output("kpi-rating", "children"),
    Output("grafico-antiguas", "figure"),
    Output("grafico-dispersion", "figure"),
    Output("tabla-peliculas", "data"),
    Input("slider-cantidad", "value")
)
def actualizar_dashboard(cantidad):
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
    df = pd.read_sql(query, engine)
    df["Fecha"] = pd.to_numeric(df["Fecha"], errors='coerce')
    df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')
    df["duracion"] = pd.to_numeric(df["duracion"], errors='coerce')
    df = df.dropna(subset=["Fecha"])

    df_ordenado = df.sort_values("Fecha", ascending=True)
    df_ordenado = df_ordenado.drop_duplicates(subset=["Nombre"], keep="first")
    top_antiguas = df_ordenado.head(cantidad)

    kpi_total = len(top_antiguas)
    kpi_duracion = f"{top_antiguas['duracion'].mean():.2f} min"
    kpi_rating = f"{top_antiguas['Rating'].mean():.2f}"

    fig_antiguas = px.bar(
        top_antiguas,
        x="Nombre", y="Fecha",
        title=f"Top {cantidad} Películas Más Antiguas",
        color="Nombre",
        color_discrete_sequence=COLORES
    )
    fig_antiguas.update_layout(yaxis_title="Año de Estreno")

    fig_dispers = px.scatter(
        top_antiguas,
        x="duracion", y="Rating",
        color="Nombre",
        title="Duración vs Rating (Top películas antiguas)",
        color_discrete_sequence=COLORES
    )

    return str(kpi_total), kpi_duracion, kpi_rating, fig_antiguas, fig_dispers, top_antiguas.to_dict("records")


if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
    app.layout = dashboard_antiguas()
    app.run(debug=True)


