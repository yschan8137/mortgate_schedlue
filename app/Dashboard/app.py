from dash import Dash
import dash_bootstrap_components as dbc
from .components.Controls.options import AdvancedOptions

# py -m app.Dashboard.app
if __name__ == "__main__":
    app= Dash(
        __name__,
        external_stylesheets= [dbc.themes.BOOTSTRAP])
    app.layout= AdvancedOptions.prepayment()
    app.run_server(debug=True)