import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

from src.consts import LOG_DATA_DIR, MAP_CENTER
from src.preprocessing.agg import load_and_concat_csv

dash.register_page(__name__)

df = load_and_concat_csv(LOG_DATA_DIR / "agg")


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
            "center": MAP_CENTER,
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
                size=10,
                color=df["climb_rate"],
                colorscale="RdBu_r",
                cmin=-3,
                cmax=3,
                colorbar=dict(title="Climb Rate"),
            ),
            hovertext=df["altitude(press)"],
            hovertemplate="climb rate: %{marker.color:.2f} m/s<br>altitude: %{hovertext:d} m",
        )
    )

    return fig
