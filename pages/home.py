import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/")

sidebar = html.Div([])
content = html.Div([html.H4("Welcome to Glider Dashboard!")])

layout = layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=2, className="bg-light"),
                dbc.Col(content, width=10),
            ],
            style={"height": "100vh"},
        ),
    ],
    fluid=True,
)
