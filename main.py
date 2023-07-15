from dash import Dash
import dash_bootstrap_components as dbc
from Dashboard.components.DataTable.app import deployment

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = deployment

app.run_server(host='0.0.0.0', port=80, debug= False)
