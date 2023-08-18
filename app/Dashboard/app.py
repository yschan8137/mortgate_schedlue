import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from app.Dashboard.components.Controls.main import panel
from app.Dashboard.components.Controls.options import AdvancedOptions
from app.Dashboard.components.DataTable.app import deployment

# https://dash.plotly.com/urls
# https://medium.com/@mcmanus_data_works/how-to-create-a-multipage-dash-app-261a8699ac3f
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
	app.run(debug=True)








# py -m app.Dashboard.app
if __name__ == "__main__":
    app= Dash(
        __name__,
        external_stylesheets= [dbc.themes.LUMEN, dbc.icons.BOOTSTRAP],
        suppress_callback_exceptions= True,
        )
    app.layout= mainpage()
    app.run_server(debug=True)