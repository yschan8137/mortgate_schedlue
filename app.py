from dash import Dash
import dash_bootstrap_components as dbc
from Dashboard.components.DataTable.app import deployment

# py -m app
if __name__ == '__main__':
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = deployment
    app.run_server(debug=True)
