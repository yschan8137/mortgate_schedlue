from Loan import calculator

from dash import Dash, dcc, html, page_registry, page_container  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
from Loan.computation.categories import amortization
from app.Dashboard.pages.components.Controls.options import *


# py -m app.main
if __name__ == '__main__':
    app = Dash(
        __name__,
        # use_pages=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    # app.run(debug=True)

# example: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/