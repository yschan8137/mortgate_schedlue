from Amort.loan import calculator

from dash import Dash, dcc, html, page_registry, page_container
import dash_bootstrap_components as dbc
from Amort.dashboard import amortization

from Amort.dashboard.components.homepage.controls import *


# py -m Amort.dashboard.app
if __name__ == '__main__':
    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.SPACELAB])

    app.run(debug=True)
