import os

import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import polars as pl
from dash import Input, Output, callback, dcc, html

from src.consts import AMEDAS_DATA_DIR, LOG_DATA_DIR, MAP_CENTER
from src.preprocessing.agg import load_and_concat_csv, merge_log_and_amedas_data

dash.register_page(__name__)


# load data
df_log = load_and_concat_csv(LOG_DATA_DIR / "agg").with_columns(
    pl.col("timestamp").str.strptime(pl.Datetime)
)
df_amedas = load_and_concat_csv(AMEDAS_DATA_DIR / "processed").with_columns(
    pl.col("timestamp").str.strptime(pl.Datetime)
)
df = merge_log_and_amedas_data(df_log, df_amedas)


sidebar = html.Div(
    [
        html.Div(
            [
                html.P("temperature (℃)"),
                dcc.RangeSlider(min=0, max=35, step=5, value=[0, 35], id="temperature"),
            ]
        ),
        html.Div(
            [
                html.P("wind speed (m/s)"),
                dcc.RangeSlider(min=0, max=10, step=1, value=[0, 10], id="wind-speed"),
            ]
        ),
        html.Div(
            [
                html.P("wind direction (°)"),
                dcc.RangeSlider(
                    min=0,
                    max=360,
                    step=45,
                    value=[0, 360],
                    marks={
                        v: str(v) if v % 90 == 0 else "" for v in range(0, 360 + 45, 45)
                    },
                    id="wind-direction",
                ),
            ]
        ),
        html.Div(
            [
                html.P("daylight hours (h)"),
                dcc.RangeSlider(
                    min=0, max=1, step=0.2, value=[0, 1], id="daylight-hours"
                ),
            ]
        ),
    ],
    className="parent-div",
    style={"textAlign": "center"},
)

content = html.Div(
    [
        dcc.Store(data=MAP_CENTER, id="map-center"),
        dcc.Graph(id="thermal-spots", className="fig", style={"height": "90vh"}),
    ]
)

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
    Input(component_id="temperature", component_property="value"),
    Input(component_id="wind-speed", component_property="value"),
    Input(component_id="wind-direction", component_property="value"),
    Input(component_id="daylight-hours", component_property="value"),
)
def update_thermal_spots(
    temperature_range, wind_speed_range, wind_direction_range, daylight_hours_range
):
    df_filtered = df.filter(
        (pl.col("temperature").is_between(temperature_range[0], temperature_range[1]))
        & (pl.col("wind speed").is_between(wind_speed_range[0], wind_speed_range[1]))
        & (
            pl.col("wind direction").is_between(
                wind_direction_range[0], wind_direction_range[1]
            )
        )
        & (
            pl.col("daylight hours").is_between(
                daylight_hours_range[0], daylight_hours_range[1]
            )
        )
    )

    fig = go.Figure()
    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "accesstoken": os.getenv("MAPBOX_ACCESS_TOKEN"),
            "center": MAP_CENTER,
            "style": "satellite",
            "zoom": 12,
        },
        uirevision=True,
    )

    fig.add_trace(
        go.Scattermapbox(
            mode="markers",
            lat=df_filtered["latitude"],
            lon=df_filtered["longitude"],
            marker=dict(
                size=10,
                color=df_filtered["climb_rate"],
                colorscale="Blackbody_r",
                cmin=-1,
                cmax=3,
                colorbar=dict(title="Climb Rate"),
            ),
            hovertext=df_filtered["altitude(press)"],
            hovertemplate="climb rate: %{marker.color:.2f} m/s<br>altitude: %{hovertext:d} m",
        )
    )

    return fig
