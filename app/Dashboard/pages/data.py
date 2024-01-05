from dash import html, register_page, callback
from app.Dashboard.pages.components.DataTable import dataframe
import dash_bootstrap_components as dbc

import sys
sys.path.append('./')

from app.Dashboard.assets.ids import APP

# https://community.plotly.com/t/callback-for-dynamically-created-graph/5511/4?_gl=1*efions*_ga*MTczNDU5MjM4LjE2NjI4ODY4Mjc.*_ga_6G7EE0JNSC*MTY5MjUxODEyMi4xNjMuMS4xNjkyNTE4MzMzLjYwLjAuMA..

register_page(
    __name__,
    name= APP.INDEX.DATA,
    # top_nav=True,
    path= APP.URL.DATA,
    suppress_callback_exceptions=True,
)

layout = dbc.Container(
    [
        dataframe.deployment(),
    ],
    fluid= True
)