from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc

from utils import stats

DATA_DIR = Path(__file__).parents[1] / "data/csv"


igc_files = [file.stem for file in DATA_DIR.glob("*.csv")]
dropdown = dcc.Dropdown(igc_files, id="igc-files-dropdown", optionHeight=50, multi=True)

graph_trajectory = dcc.Graph(id="trajectory")
graph_altitude = dcc.Graph(id="altitude")

graph_climb_rate = dcc.Graph(id="climb-rate")


@callback(
    Output(component_id="trajectory", component_property="figure"),
    Input(component_id="igc-files-dropdown", component_property="value"),
)
def update_trajectory(files):
    fig = go.Figure()
    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": 139.41889, "lat": 36.21139},
            "style": "carto-positron",
            "zoom": 13,
        },
    )

    if files is None:
        fig.add_trace(go.Scattermapbox())
        return fig

    for file in files:
        df = pd.read_csv(DATA_DIR / f"{file}.csv")
        fig.add_trace(
            go.Scattermapbox(
                mode="lines",
                lon=df["longitude"],
                lat=df["latitude"],
                hovertext=df["altitude(press)"],
                hovertemplate="%{hovertext} m",
                name=file,
            )
        )

    return fig


@callback(
    Output(component_id="altitude", component_property="figure"),
    Input(component_id="igc-files-dropdown", component_property="value"),
)
def update_altitude(files):
    fig = go.Figure()
    fig.update_layout(
        xaxis_title="time",
        yaxis_title="altitulde (m)",
        showlegend=False,
        hovermode="x unified",
    )

    if files is None:
        return fig

    for file in files:
        df = pd.read_csv(DATA_DIR / f"{file}.csv")
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["altitude(press)"], name=file))

    return fig


@callback(
    Output(component_id="climb-rate", component_property="figure"),
    Input(component_id="igc-files-dropdown", component_property="value"),
)
def update_climb_rate(files):
    fig = go.Figure()
    fig.update_layout(yaxis_title="climb rate (m/s)", showlegend=False)

    if files is None:
        return fig

    for file in files:
        df = pd.read_csv(DATA_DIR / f"{file}.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        climb_rate = stats.average_climb_rate(df)
        fig.add_trace(
            go.Bar(
                x=[file],
                y=[climb_rate],
                text=[round(climb_rate, 2)],
                hovertext=[round(climb_rate, 2)],
                hovertemplate="%{hovertext} m/s",
                name=file,
            )
        )

    return fig
