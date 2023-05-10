from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from dash import Dash, dcc, html

from components._01_import_cdr import import_data
from components._02_layout import create_layout

data = import_data()
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])#a
app.title = "Carbon Dioxide Removal - Certificate Market"
app.layout = create_layout(app, data)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, port="8051")