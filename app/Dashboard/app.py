from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from app.Dashboard.components.Controls.options import AdvancedOptions
from app.Dashboard.components.DataTable.app import deployment

def mainpage():
    layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
    
    @callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')]
            )
    def display_page(pathname):
        if pathname == '/page-1':
            return deployment()
        # elif pathname == '/page-2':
            # return page2.layout
        else:
            return '404'
    
    return layout



# py -m app.Dashboard.app
if __name__ == "__main__":
    app= Dash(
        __name__,
        external_stylesheets= [dbc.themes.LUMEN, dbc.icons.BOOTSTRAP],
        suppress_callback_exceptions= True,
        )
    app.layout= mainpage()
    app.run_server(debug=True)