import os

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
from dotenv import load_dotenv

from src.consts import ROOT
from src.fetch_data import fetch_files_from_s3

load_dotenv()

bucket_name = os.getenv("BUCKET_NAME")
fetch_files_from_s3(bucket_name, "log/agg/", ROOT / "data/log/agg/")
fetch_files_from_s3(bucket_name, "amedas/processed/", ROOT / "data/amedas/processed/")


app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], use_pages=True)

server = app.server

navbar = dbc.NavbarSimple(
    children=[
        *[
            dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"]))
            for page in dash.page_registry.values()
        ],
    ],
    brand="Glider Dashboard",
    color="primary",
    dark=True,
)

app.layout = html.Div(
    [
        navbar,
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
