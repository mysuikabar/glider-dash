from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc

DATA_DIR = Path(__file__).parents[1] / "data/csv"


igc_files = [file.stem for file in DATA_DIR.glob("*.csv")]
dropdown = dcc.Dropdown(igc_files, id="igc-files-dropdown", optionHeight=50, multi=True)

graph_trajectory = dcc.Graph(id="trajectory")
graph_altitude = dcc.Graph(id="altitude")


@callback(
    Output(component_id="trajectory", component_property="figure"),
    Input(component_id="igc-files-dropdown", component_property="value"),
)
def update_trajectory(values):
    fig = go.Figure()
    fig.update_layout(
        margin={"l": 0, "t": 0, "b": 0, "r": 0},
        mapbox={
            "center": {"lon": 139.41889, "lat": 36.21139},
            "style": "carto-positron",
            "zoom": 13,
        },
    )

    if values is None:
        fig.add_trace(go.Scattermapbox())
        return fig

    for value in values:
        df = pd.read_csv(DATA_DIR / f"{value}.csv")
        fig.add_trace(
            go.Scattermapbox(
                mode="lines",
                lon=df["longitude"],
                lat=df["latitude"],
                hovertext=df["altitude(press)"],
                hovertemplate="%{hovertext} m",
                name=value,
            )
        )

    return fig


@callback(
    Output(component_id="altitude", component_property="figure"),
    Input(component_id="igc-files-dropdown", component_property="value"),
)
def update_altitude(values):
    fig = go.Figure()
    fig.update_layout(showlegend=False, hovermode="x unified")

    if values is None:
        return fig

    for value in values:
        df = pd.read_csv(DATA_DIR / f"{value}.csv")
        fig.add_trace(
            go.Scatter(x=df["timestamp"], y=df["altitude(press)"], name=value)
        )

    return fig
