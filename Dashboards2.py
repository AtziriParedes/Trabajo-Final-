import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, callback
from sqlalchemy import create_engine

COLORES = ['#FE5668', '#FF8D8F', '#FEC1A5', '#B9D394', '#64A002']

def layout_dashboard(df):
    anios = df["Fecha"].dropna().unique()
    anios = sorted([int(a) for a in anios if not pd.isna(a)])

    return dbc.Container([
        html.H2("Películas IMDb", style={"textAlign": "center", "color": "#FE5668"}),

        dbc.Card([
            dbc.CardHeader("Filtro por año"),
            dbc.CardBody([
                dbc.Label("Año: "),
                dcc.Dropdown(
                    id="rating-filtro-anio",
                    options=[{"label": str(a), "value": a} for a in anios],
                    value=2024,
                    clearable=False
                )
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Promedio Rating", className="card-title"),
                        html.H4(id="rating-kpi-rrrating")
                    ])
                ], color="danger", inverse=True)
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Promedio Duración", className="card-title"),
                        html.H4(id="rating-kpi-duracion")
                    ])
                ], color="success", inverse=True)
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Películas Totales", className="card-title"),
                        html.H4(id="rating-kpi-totalito")
                    ])
                ], color="warning", inverse=True)
            ]),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="rating-grafico-barra"), md=6),
            dbc.Col(dcc.Graph(id="rating-grafico-pie"), md=6)
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="rating-grafico-linea"))
        ]),

        html.Hr(),

        html.H4("Tabla de Películas", style={"color": "#64A002"}),
        dash_table.DataTable(
            id="rating-tabla",
            page_size=10,
            style_header={"backgroundColor": "#FF8D8F", "fontWeight": "bold"},
            style_data={"backgroundColor": "#FEC1A5"},
            style_cell={"textAlign": "left", "padding": "5px"}
        )
    ], fluid=True)

def dashboard_rating():
    engine = create_engine('mysql+mysqlconnector://root:Josva2309@localhost:3306/peli')
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
    return layout_dashboard(df)


@callback(
    Output("rating-kpi-rrrating", "children"),
    Output("rating-kpi-duracion", "children"),
    Output("rating-kpi-totalito", "children"),
    Output("rating-grafico-barra", "figure"),
    Output("rating-grafico-pie", "figure"),
    Output("rating-grafico-linea", "figure"),
    Output("rating-tabla", "data"),
    Input("rating-filtro-anio", "value")
)
def actualizar_dashboard(anio):
    engine = create_engine('mysql+mysqlconnector://root:Josva2309@localhost:3306/peli')
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
    df = df[df["Fecha"] == anio]
    df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')
    df["duracion"] = pd.to_numeric(df["duracion"], errors='coerce')

    # KPIs
    rating_prom = f"{df['Rating'].mean():.2f}" if not df['Rating'].isna().all() else "N/A"
    duracion_prom = f"{df['duracion'].mean():.0f} min" if not df['duracion'].isna().all() else "N/A"
    total_pelis = len(df)

    # Gráfica de barras (top 10)
    top = df.sort_values("Rating", ascending=False).head(10)
    fig_bar = px.bar(top, x="Nombre", y="Rating", title="Top 10 Películas", color="Nombre", color_discrete_sequence=COLORES)

    # Gráfica pie
    fig_pie = px.pie(df, names="Nombre", values="duracion", title="Duración total por película", color_discrete_sequence=COLORES)

    # Gráfica línea (rating promedio por año)
    df_all = pd.read_sql(query, engine)
    df_all["Rating"] = pd.to_numeric(df_all["Rating"], errors='coerce')
    df_all = df_all.dropna(subset=["Fecha", "Rating"])
    promedio_rating = df_all.groupby("Fecha")["Rating"].mean().reset_index()
    fig_linea = px.line(promedio_rating, x="Fecha", y="Rating", title="Rating Promedio por Año", markers=True)

    return rating_prom, duracion_prom, total_pelis, fig_bar, fig_pie, fig_linea, df.to_dict("records")