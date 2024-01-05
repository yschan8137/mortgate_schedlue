from dash import Dash, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import sys
sys.path.append('./')

# from app.Dashboard.navbar import create_navbar
from app.Dashboard.pages.components.Controls.panels import panel
from app.Dashboard.pages.components.Graphic.main import graph
from app.Dashboard.pages.components.DataTable import table as dataframe
from app.Dashboard.assets import ids


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

#TODO:
#    [X]-fix the issues for information diagram regarding excess column data from subsidy loans. 
#    []-donut charts for the information diagrams
#    []-add side navbar
#    [X]-enable dynamic adjustable screen size
#    [X]-apply modal for table

panel_tabs= dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tab(
                        children= 'Main',
                        id= 'main-options',
                        value= 'Main',
                        style= {
                            'font-weight': 'bold',
                          },
                        ),
                    dmc.Tab(
                        children= 'Advanced',
                        id= 'advanced-options',
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
        },
    },
    children=[
        panel.register(),
        # NAVBAR,
        dmc.Container(
            [
                dmc.Modal(
                    title="Details",
                    id="show-table",
                    centered=True,
                    zIndex=10000,
                    size= "90%",
                    overlayOpacity= 0.5,
                    children=[dataframe.table()],
                    style= {
                        'height': '98dvh',
                        'font-size': '20px',
                        'font-weight': 'bold',
                        'color': '#333',
                        'overflow-y': 'scroll',
                        'radius': '5px',
                        # 'background-color': 'rgba(246,248,250,255)',
                        
                    },
                    className= 'custom-scrollbar',
                ),
                
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

@app.callback(
    Output("show-table", "opened"),
    Input("detailed-table", "n_clicks"),
    State("show-table", "opened"),
)
def toggle_modal(_, opened):
    if _:
        return not opened 

# python app/Dashboard/main.py
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