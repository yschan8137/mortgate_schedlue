from dash import Dash
import dash_bootstrap_components as dbc
from Dashboard.components.DataTable.app import datatable, CONFIG
from Dashboard.components.DataTable.controls import layout

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
        #    suppress_callback_exceptions=True
           )

app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    layout(),
                ],
                xs=CONFIG.SPLITS.XS,
                sm=CONFIG.SPLITS.SM,
                md=CONFIG.SPLITS.MD,
                lg=CONFIG.SPLITS.LG,
                xl=CONFIG.SPLITS.XL,
            ),
            dbc.Col(
                [
                    datatable()
                ],
                xs=12 - CONFIG.SPLITS.XS,
                sm=12 - CONFIG.SPLITS.SM,
                md=12 - CONFIG.SPLITS.MD,
                lg=12 - CONFIG.SPLITS.LG,
                xl=12 - CONFIG.SPLITS.XL,
            )
        ],
        style={
            'marginTop': '2%',
            'marginBottom': '2%',
        },
    ),
    fluid=True
)

# py -m main
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug= False)
