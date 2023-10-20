from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from app.Dashboard.navbar import create_navbar
from app.Dashboard.pages.components.Controls.panels import panel, register
from app.Dashboard.pages.components.Graphic.app import graph
from app.Dashboard.pages.components.DataTable import dataframe
from app.Dashboard.assets import ids, specs


NAVBAR = create_navbar()
# To use Font Awesome Icons
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "Amort"

[] divided frames by setting html. div
[] scroll bar style

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUMEN,  # Dash Themes CSS
        dbc.icons.BOOTSTRAP,
        FA621,  # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
    assets_external_path= 'app/Dashboard/assets',
)

tabs = dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab(
                               ids.APP.INDEX.GRAPH,
                               icon= DashIconify(icon="bi:graph-up"),
                               value= ids.APP.INDEX.GRAPH,
                               ),
                        dmc.Tab(
                               ids.APP.INDEX.DATA,
                               icon= DashIconify(icon="ph:table-light"),
                               value= ids.APP.INDEX.DATA
                        ),
                    ]
                ),
                dmc.TabsPanel(graph(), value= ids.APP.INDEX.GRAPH),
                dmc.TabsPanel(
                    dataframe.deployment(), 
                    value= ids.APP.INDEX.DATA,
                ),
            ],
            value= ids.APP.INDEX.GRAPH,
            id="card-tabs",
            activateTabWithKeyboard= True,
            style= specs.APP.TAB.STYLE
        )

app.layout = dmc.MantineProvider(  # <- Wrap App with Loading Component
    id= ids.APP.LOADING,
    children=[
        # dmc.Aside(
            # p= 'md',
            # width= {'base': '100%'},
            # height= 77,
            # fixed= True,
            # position= {
                # 'top': -16,
                # 'left': 0,
            # },
            # children= [
                # NAVBAR
            # ],
            # style= {
                # 'background-color': 'black',
            # },
        # ),
        register(),
        NAVBAR,
        dmc.Group(
            [
                html.Div(
                    panel.front(),
                    style= specs.APP.PANEL.STYLE
                ),
                # dmc.Aside(
                    # p="md",
                    # width={"base": 420},
                    # height=5000,
                    # fixed=True,
                    # position={
                        # "left": 0, 
                        # "top": 68,
                    # },
                    # children=[
                                # panel.front(),
                    # ],
                    # 
                    # style= {
                        # 'background-color': 'rgba(255, 255, 255, 0)',
                        # 'z-index': 100,
                        # 'overflow-y': 'hidden',

                    # },
                # ),
                html.Div(tabs),
            ],
            spacing= 0,
            position= 'flex-start',
            align= 'start',
        )
    ],
    # theme= {"colorScheme": ""},
    # style={
        # 'width': '100%',
        # 'background': '#CBD9E0',
        # 'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
        # 'border': '1px solid #ccc',
        # 'border-radius': '5px',
    # },
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