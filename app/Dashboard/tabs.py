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
    "app/Dashboard/assets/style.css",
    ]
)


panel_tabs= dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab(
                        children= 'Main',
                        id= 'main-options',
                        #    icon= DashIconify(icon="bi:graph-up"),
                        value= 'Main',
                        style= {
                            'font-weight': 'bold',
                          },
                        ),
                    dmc.Tab(
                        children= 'Advanced',
                        id= 'advanced-options',
                        # icon= DashIconify(icon="ph:table-light"),
                        value= 'Advanced',
                        icon=DashIconify(icon="tabler:settings"),
                        style= {
                            'font-weight': 'bold',
                          },
                    ),
                ],
                grow= True,
            ),
            dmc.TabsPanel(panel.front(), value= 'Main'),
            dmc.TabsPanel(
                html.Div(
                    panel._advancedoptions(),
                    className= 'custom-scrollbar',
                    style= {
                        'width': '100%',
                        'height': '70dvh',
                        'overflow-y': 'scroll',
                        # 'scrollbar-color': '#0C82DF #E2E2E2',
                        'color': '#333',
                        'background-color': 'white',
                    },
                ), 
                value= 'Advanced',
            ),
        ],
        value= 'Main',
        id="options-tabs",
        activateTabWithKeyboard= True,
        className= 'custom-scrollbar',
        variant= 'outline',
        style= {
            'width': '100%',
            # 'height': '70vdh',
            'color': '#333',
            'background-color': 'white',
        },
    )

app.layout = dmc.MantineProvider(
    id= ids.APP.LOADING,
    theme= {
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
            'scrollbar': {
                'thumb': {
                    'backgroundColor': '#0C82DF',
                    'borderRadius': '4px',
                },
                'track': {
                    'backgroundColor': '#E2E2E2',
                    'borderRadius': '4px',
                },
            },
        },
    },
    children=[
        panel.register(),
        # NAVBAR,
        dmc.Container(
            [
                
                html.Div(
                    children= [
                        panel_tabs,
                    ],
                    className= 'custom-scrollbar',
                    style= {
                        'width': '25dvw',
                        'height': '80dvh',
                        'margin-top': 10,
                        'margin-left': 15,
                        # 'scrollbar-color': '#0C82DF #E2E2E2',
                        'border': '1px solid #ccc',
                        'border-radius': '5px',
                        'font-size': '20px',
                        'font-weight': 'bold',
                        'padding': '10px',
                        'color': '#333',
                        'background-color': 'white',
                    },
                ),
                html.Div(
                    [
                        graph(),
                        html.Br(),
                        dataframe.table(),
                    ],
                    className= 'custom-scrollbar',
                    style= {
                        'width': 'calc(100dvw - 365px)',
                        'height': '98vh',
                        'overflow-y': 'scroll',
                        'scrollbar-color': '#0C82DF #E2E2E2',
                        'margin-left': 20,
                        'margin-right': 20,
                    }
                ),
                
            ],
            fluid= True,
            style= {
                'background-color': 'rgba(246,248,250,255)',
                'width': '100vw',
                'height': '98vh',
                'margin': 0,
                'padding': 0,
                'display': 'flex',
            }
        ),
        
    ],
    withGlobalStyles= True,
    withCSSVariables= True,
    

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