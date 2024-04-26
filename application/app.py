import os

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
from dotenv import load_dotenv

from src.config import Config
from src.fetch_data import fetch_csv_from_s3

load_dotenv()

bucket_name_log = os.getenv("BUCKET_NAME_LOG")
bucket_name_amedas = os.getenv("BUCKET_NAME_AMEDAS")
fetch_csv_from_s3(bucket_name=bucket_name_log, local_dir=Config.log_data_dir / "agg")
fetch_csv_from_s3(
    bucket_name=bucket_name_amedas, local_dir=Config.amedas_data_dir / "processed"
)


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
