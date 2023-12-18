from dash import Dash, html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import sys
sys.path.append('./')

# from app.Dashboard.navbar import create_navbar
from app.Dashboard.pages.components.Controls.panels import panel
from app.Dashboard.pages.components.Graphic.app import graph
from app.Dashboard.pages.components.DataTable import table as dataframe
from app.Dashboard.assets import ids, specs


# NAVBAR = create_navbar()
# To use Font Awesome Icons
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "Amort"


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap",
        dbc.themes.LUMEN,  # Dash Themes CSS
        dbc.icons.BOOTSTRAP,
        "https://use.fontawesome.com/releases/v6.2.1/css/all.css",  # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
    assets_external_path= 'app/Dashboard/assets',
    
)


# tabs = dmc.Tabs(
#             [
#                 dmc.TabsList(
#                     [
#                         dmc.Tab(
#                                ids.APP.INDEX.GRAPH,
#                                icon= DashIconify(icon="bi:graph-up"),
#                                value= ids.APP.INDEX.GRAPH,
#                                ),
#                         dmc.Tab(
#                                ids.APP.INDEX.DATA,
#                                icon= DashIconify(icon="ph:table-light"),
#                                value= ids.APP.INDEX.DATA,
#                         ),
#                     ]
#                 ),
#                 dmc.TabsPanel(graph(), value= ids.APP.INDEX.GRAPH),
#                 dmc.TabsPanel(
#                     dataframe.table(), 
#                     value= ids.APP.INDEX.DATA,
#                 ),
#             ],
#             value= ids.APP.INDEX.GRAPH,
#             id="card-tabs",
#             activateTabWithKeyboard= True,
#             style= specs.APP.TAB.STYLE,
#             className= 'custom-scrollbar'
#         )


app.layout = dmc.MantineProvider(  # <- Wrap App with Loading Component
    id= ids.APP.LOADING,
    theme= {
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    children=[
        panel.register(),
        # NAVBAR,
        dmc.Group(
            [
                html.Div(
                    children= [
                        panel.front(),
                        html.Br(),
                        panel._advancedoptions(),
                    ],
                    className= 'custom-scrollbar',
                    style= specs.APP.PANEL.STYLE,
                ),
                # tabs,
                html.Div(
                    [
                        graph(),
                        dmc.Space(h=30),
                        dataframe.table(),
                    ],
                    className= 'custom-scrollbar',
                    style= {
                        'width': '70%',
                        'height': '98vh',
                        'left': '30%',
                        'align-items': 'center',
                        'overflow-y': 'scroll',
                        'scrollbar-color': '#0C82DF #E2E2E2',
                    }
                ),
            ],
            spacing= 10,
            position= 'flex-start',
            align= 'start',
        )
    ],
    withGlobalStyles= True,
)

# python app/Dashboard/tabs.py
# py -m app.Dashboard.tabs
if __name__ == "__main__":
    app.run_server(
        # debug=True,
        # threaded=True, 
)