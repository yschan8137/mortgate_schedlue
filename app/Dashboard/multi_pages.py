from dash import Dash, html, dcc, Input, Output, State, page_container
import dash_bootstrap_components as dbc
from app.Dashboard.pages.components.Controls.main import panel, register
from app.Dashboard.pages.components.Controls.options import AdvancedOptions
from app.Dashboard.pages.components.ids import APP
from app.Dashboard.navbar import create_navbar

# https://dash.plotly.com/urls
# Template reference from: https://medium.com/@mcmanus_data_works/how-to-create-a-multipage-dash-app-261a8699ac3f
# https://dash.plotly.com/urls
# https://github.com/AnnMarieW/dash-multi-page-app-demos/blob/main/multi_page_example1/app.py

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
    use_pages=True, 
)

# To use if you're planning on using Google Analytics
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

app.layout = html.Div(  # <- Wrap App with Loading Component
    id= APP.LOADING,
    children=[
        dcc.Location(id="url"),
        register(),
        NAVBAR,
        page_container
    ],
    style={
        'width': '100%',
        'background': '#F7F7F7',
    },
    # color='primary',  # <- Color of the loading spinner
    # fullscreen=True,  # <- Loading Spinner should take up full screen
)

server = app.server

# py -m app.Dashboard.multi_pages
if __name__ == '__main__':
    app.run_server(
        debug=True, 
        threaded=True
    )