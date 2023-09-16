from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from app.Dashboard.navbar import create_navbar
from app.Dashboard.pages.components.Controls.main import panel, register
from app.Dashboard.pages.components.Graphic.app import graph
from app.Dashboard.pages.components.DataTable import dataframe
from app.Dashboard.pages.components.ids import APP
NAVBAR = create_navbar()
# To use Font Awesome Icons
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "Amort"

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUMEN,  # Dash Themes CSS
        dbc.icons.BOOTSTRAP,
        FA621,  # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
)

card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(
                        graph(), 
                        label=APP.INDEX.GRAPH, 
                        tab_id="tab-1",
                    ),
                    dbc.Tab(dataframe.deployment(),label=APP.INDEX.DATA, tab_id="tab-2", style= {'height': '550px', "overflow-y": "scroll",}),
                ],
                id="card-tabs",
                active_tab="tab-1",
                className= 'mb-2'
            )
        ),
        # dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)

app.layout = html.Div(  # <- Wrap App with Loading Component
    id= APP.LOADING,
    children=[
        NAVBAR,
        register(),
        dbc.Container(
        [
            html.Br(),
            panel.front(),
            card
        ],
   className="vstack gap-3"
)
    ],
    style={
        'width': '100%',
        'background': '#F7F7F7',
    },
    # color='primary',  # <- Color of the loading spinner
    # fullscreen=True,  # <- Loading Spinner should take up full screen
)

# @callback(
    # Output("card-content", "children"), [Input("card-tabs", "active_tab")]
# )
# def tab_content(active_tab):
    # return "This is tab {}".format(active_tab)

# py -m app.Dashboard.tabs
if __name__ == "__main__":
    app.run_server(
    debug=True, 
    threaded=True
)