import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], use_pages=True)

app.layout = html.Div(
    [
        html.H1("Glider Dashboard"),
        html.Div(
            [
                html.Div(dcc.Link(f"{page['name']}", href=page["relative_path"]))
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
