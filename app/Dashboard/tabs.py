from dash import Dash, html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from app.Dashboard.navbar import create_navbar
from app.Dashboard.pages.components.Controls.panels import panel
from app.Dashboard.pages.components.Graphic.app import graph
from app.Dashboard.pages.components.DataTable import dataframe
from app.Dashboard.assets import ids, specs


NAVBAR = create_navbar()
# To use Font Awesome Icons
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "Amort"

# [] divided frames by setting html. div
# [] scroll bar style

app = Dash(
    __name__,
    # assets_folder= 'app/Dashboard/assets', #redirects to assets folder
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUMEN,  # Dash Themes CSS
        dbc.icons.BOOTSTRAP,
        FA621,  # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
    # assets_external_path= 'app/Dashboard/assets',
    
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
                               value= ids.APP.INDEX.DATA,
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
            style= specs.APP.TAB.STYLE,
            className= 'custom-scrollbar'
        )


app.layout = dmc.MantineProvider(  # <- Wrap App with Loading Component
    id= ids.APP.LOADING,
    children=[
        panel.register(),
        NAVBAR,
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
                html.Div(
                    tabs,
                ),
            ],
            spacing= 0,
            position= 'flex-start',
            align= 'start',
        )
    ],
    withGlobalStyles= True,
)


# py -m app.Dashboard.tabs
if __name__ == "__main__":
    app.run_server(
    debug=True, 
    # threaded=True,
)