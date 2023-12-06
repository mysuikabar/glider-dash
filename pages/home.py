import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__, path="/")

content = html.Div([html.H4("Welcome to Glider Dashboard!")])

layout = layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(content, width=10),
            ],
        ),
    ],
    fluid=True,
)
