import dash_bootstrap_components as dbc
from dash import Dash, html

from components import flight_log

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

sidebar = html.Div(
    [html.H3("Glider Dashboard"), html.P("Select IGC files"), flight_log.dropdown]
)
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([html.P("Trajectory"), flight_log.graph_trajectory]),
            ],
            style={"height": "50vh"},
        ),
        dbc.Row(
            [
                dbc.Col([html.P("Altitude"), flight_log.graph_altitude]),
                dbc.Col([html.P("Climb Rate")]),
            ],
            style={"height": "50vh"},
        ),
    ]
)


app.layout = dbc.Container(
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


if __name__ == "__main__":
    app.run(debug=True)
