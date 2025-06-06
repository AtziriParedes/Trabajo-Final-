import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback
from Dashboards import dashboard_antiguas
from Dashboards2 import dashboard_rating


SIDEBAR_STYLE = {
   "position": "fixed",
   "top": 0,
   "left": 0,
   "bottom": 0,
   "width": "16rem",
   "padding": "2rem 1rem",
   "background-color": "#FF8D8F",
}


CONTENT_STYLE = {
   "margin-left": "18rem",
   "margin-right": "2rem",
   "padding": "2rem 1rem",
   "background-color": "#FEC1A5"
}


sidebar = html.Div(
   [
       html.H2("IMDB", className="display-4", style={"color": "#FE5668"}),
       html.Hr(),
       html.P("Visualización de películas", className="lead"),
       dbc.Nav(
           [
               dbc.NavLink("Inicio", href="/", active="exact"),
               dbc.NavLink("Películas más antiguas", href="/antiguas", active="exact"),
               dbc.NavLink("Películas con mayor rating", href="/rating", active="exact"),
           ],
           vertical=True,
           pills=True,
       ),
   ],
   style=SIDEBAR_STYLE,
)


content = html.Div(id="page-content", style=CONTENT_STYLE)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
               suppress_callback_exceptions=True)


app.layout = html.Div([
   dcc.Location(id="url"),
   sidebar,
   content
])


@callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
   if pathname == "/":
       return html.Div([
           html.H1("Bienvenido a IMDb Dashboards", style={"color": "#64A002"}),
           html.P("Selecciona una opción del menú para comenzar.")
       ])
   elif pathname == "/antiguas":
       return dashboard_antiguas()
   elif pathname == "/rating":
       return dashboard_rating()
   return html.Div([
       html.H1("404: Página no encontrada", className="text-danger"),
       html.P(f"No existe la ruta: {pathname}")
   ])


if __name__ == "__main__":
   app.run(debug=True)


