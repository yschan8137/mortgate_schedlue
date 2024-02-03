from dash import Dash, dcc, html, Input, Output, State, Patch
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import sys
sys.path.append('./')

# from app.Dashboard.navbar import create_navbar
from app.assets.ids import LOAN
from app.assets.locale import lan
from app.src.Controls.panels import panel
from app.src.Graphic.main import graph
from app.src.DataTable import table as dataframe
from app.assets import ids


# NAVBAR = create_navbar()
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "Amort"


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
            "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap",
            FA621,
            dbc.themes.LUMEN, 
            dbc.icons.BOOTSTRAP,
            "https://use.fontawesome.com/releases/v6.2.1/css/all.css",
    ],
    # assets_folder= "app/assets/",
)

app.index_string = f'''
    <!DOCTYPE html>
    <html>
        <head>
            {{%metas%}}
            <title>{APP_TITLE}</title>
            {{%favicon%}}
            {{%css%}}
        </head>
        <body>
            {{%app_entry%}}
            <footer>
                {{%config%}}
                {{%scripts%}}
                {{%renderer%}}
            </footer>
        </body>
    </html>
    '''

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
            dmc.TabsPanel(
                html.Div(
                    panel.front(),
                    className= 'custom-scrollbar',
                    style= {
                        'width': '100%',
                        'height': '80dvh',
                        'overflow-y': 'auto',
                        'color': '#333',
                        'background-color': 'white',
                    },
                ), 
                value= 'Main'
            ),
            dmc.TabsPanel(
                html.Div(
                    panel._advancedoptions(),
                    className= 'custom-scrollbar',
                    style= {
                        'width': '100%',
                        'height': '80dvh',
                        'overflow-y': 'auto',
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
        "background": {
            "dark": "#141414",
            "light": "#fff",
        },
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    children=[
        panel.register(),
        dmc.Container(
            [
                dmc.Switch(
                    id= "language-switch",
                    offLabel= "EN",
                    onLabel= "TW",
                    size="lg",
                    checked= False, 
                    color= "indigo",
                    style= {
                        'margin-left': '95%',
                        'margin-top': 5,
                        'margin-bottom': 5,
                    },
                ),
                html.Div(
                    [
                        dmc.Modal(
                            title="Details",
                            id="show-table",
                            centered=True,
                            zIndex=10000,
                            size= "100%",
                            overlayOpacity= 0.5,
                            overlayBlur= 5,
                            withCloseButton= True,
                            children=[dataframe.table()],
                            lockScroll= False,
                            style= {
                                'height': '98dvh',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': '#333',
                                'overflow-y': 'auto',
                                'overflow-x': 'auto',
                                'radius': '5px',
                            },
                        ),
                        html.Div(
                            children= [
                                panel_tabs,
                            ],
                            className= 'custom-scrollbar',
                            style= {
                                'width': '25dvw',
                                'height': '90dvh',
                                'border': '1px solid #ccc',
                                'border-radius': '5px',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': '#333',
                                'background-color': 'white',
                                'overflow-y': 'hidden', # [auto, hidden, scroll, visible]
                            },
                        ),
                        html.Div(
                            [
                                graph(),
                            ],
                            className= 'custom-scrollbar',
                            style= {
                                'width': '90dvw',
                                'height': '95dvh',
                                'overflow-y': 'hidden',
                                'scrollbar-color': '#0C82DF #E2E2E2',
                                'overflow-y': 'auto',
                                'margin-left': 20,
                            }
                        )
                    ],
                    style= {
                    'display': 'flex',
                    'flex-direction': 'row',
                    'justify-content': 'space-between',
                    'align-items': 'flex-start',
                    'padding-left': 20,
                    'padding-right': 20,
                    'margin': 'auto',
                    'overflow-y': 'hidden', # [auto, hidden, scroll, visible]
                    'overflow-x': 'hidden',
                    },
                    className= 'custom-section',
                ),
            ],
            fluid= True,
            style= {
                'background-color': 'rgba(246,248,250,255)',
                'width': '100vw',
                'height': '100vh',
                'margin': 'auto',
                'overflow-y': 'auto', # [auto, hidden, scroll, visible]
                'overflow-x': 'hidden',
            },
            className= 'custom-section',
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


# python app/main.py
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
