from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from dash import Dash, dcc, html

from components.layout import create_layout
from components.import_cdr import import_data

def main() -> None:
    data = import_data()
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Carbon Dioxide Removal - Certificate Market"
    app.layout = create_layout(app, data)
    app.run(port="8051")
    server = app.server

if __name__ == "__main__":
    main()
