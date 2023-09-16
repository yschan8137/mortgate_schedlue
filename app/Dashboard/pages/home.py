from dash import html, register_page, dcc,  Input, Output, State, callback_context, MATCH, ALL, Patch, callback, no_update, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from app.Dashboard.pages.components.Controls.main import panel
from app.Dashboard.pages.components.Graphic.app import graph
from app.Dashboard.pages.components.ids import APP
# from app.Dashboard.pages.components.toolkit import to_dropdown_options, suffix_for_type
# from app.Dashboard.pages.components.ids import *
# from app.Dashboard.pages.components import amortization_types
# import json
# from dataclasses import dataclass
# from app.Loan.main import calculator

register_page(
    __name__,
    name= APP.INDEX.HOME,
    top_nav=True,
    path= APP.URL.HOME,
)

layout = dbc.Container(
            [
                html.Br(),
                panel.front(),
                graph()
            ],
            className="vstack gap-3"
         )