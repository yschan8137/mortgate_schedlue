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
    assets_folder= 'app/Dashboard/assets',
    
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

panel_tabs= dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.Tab(
                               id= 'main-options',
                               icon= DashIconify(icon="bi:graph-up"),
                               value= 'Main',
                               ),
                        dmc.Tab(
                               id= 'advanced-options',
                               icon= DashIconify(icon="ph:table-light"),
                               value= 'Advanced',
                        ),
                    ]
                ),
                dmc.TabsPanel(panel.front(), value= 'Main'),
                dmc.TabsPanel(
                    panel._advancedoptions(), 
                    value= 'Advanced',
                ),
            ],
            value= 'Main',
            id="options-tabs",
            activateTabWithKeyboard= True,
            style= specs.APP.TAB.STYLE,
            className= 'custom-scrollbar'
        )

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
        dmc.Container(
            [
                panel_tabs,
                # html.Div(
                #     children= [
                #         panel_tabs,
                #     ],
                #     className= 'custom-scrollbar',
                #     style= {
                #         'width': 375,
                #         'height': '98vh',
                #         'margin-top': 10,
                #         'margin-left': 15,
                #         'overflow-y': 'scroll',
                #         'scrollbar-color': '#0C82DF #E2E2E2',
                #     },
                # ),
                html.Div(
                    [
                        graph(),
                        html.Br(),
                        dataframe.table(),
                    ],
                    className= 'custom-scrollbar',
                    style= {
                        'width': 'calc(100vw - 365px)',
                        'height': '98vh',
                        'overflow-y': 'scroll',
                        'scrollbar-color': '#0C82DF #E2E2E2',
                        'margin-left': 5,
                    }
                ),
                
            ],
            fluid= True,
            style= {
                'width': '100vw',
                'height': '98vh',
                'margin': 0,
                'padding': 0,
                'display': 'flex',
            }
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
        # dev_tools_ui=True,
        # dev_tools_hot_reload= True,
        # threaded=True,
        # port= 8050,
        # dev_tools_hot_reload_interval= 1000,
    )