from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from utils.preprocessing.agg import load_and_concat_csv

dash.register_page(__name__)

DATA_DIR = Path(__file__).parents[1] / "data" / "agg"
df = load_and_concat_csv(DATA_DIR)

sidebar = html.Div(
    [html.P("wind speed"), dcc.RangeSlider(min=0, max=10, step=1, id="wind-speed")],
)
content = html.Div([html.P("Thermal Spots"), dcc.Graph(id="thermal-spots")])

layout = layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=2, className="bg-light"),
                dbc.Col(content, width=10),
            ],
            style={"height": "100vp"},
        ),
    ],
    fluid=True,
)


@callback(
    Output(component_id="thermal-spots", component_property="figure"),
    Input(component_id="wind-speed", component_property="value"),
)
def update_thermal_spots(value):
    fig = go.Figure()
    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": 139.41889, "lat": 36.21139},
            "style": "carto-positron",
            "zoom": 13,
        },
    )

    fig.add_trace(
        go.Scattermapbox(
            mode="markers",
            lat=df["latitude"],
            lon=df["longitude"],
            marker=dict(
                color=df["climb_rate"],
                colorscale="RdBu_r",
                cmin=-3,
                cmax=3,
                colorbar=dict(title="Climb Rate"),
            ),
        )
    )

    return fig
