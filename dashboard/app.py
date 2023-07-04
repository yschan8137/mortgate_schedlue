from ..loan import calculator

from dash import Dash, dcc, html, page_registry, page_container  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
from ..dashboard import amortization

from ..dashboard.components.DataTable.controls import *


# py -m dashboard.app
if __name__ == '__main__':
    app = Dash(
        __name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.SPACELAB])

    app.run(debug=True)
