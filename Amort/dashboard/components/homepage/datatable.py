
from dash import Dash, dcc, html, Input, Output, State, callback, register_page, page_registry, dash_table
import dash_bootstrap_components as dbc

from ..ids import LOAN, DATATABLE, ADDON, ADVANCED
from Amort.loan import calculator
from ..toolkit import convert_df_to_dash
from .controls import MortgageOptions, AdvancedOptions
from ..toolkit import suffix_for_type

from Amort.dashboard.components.homepage import controls
class CONFIG:
    PAGE_SIZE = 24
    class SPLITS:
        XS= 6
        SM= 5
        MD= 5
        LG= 4
        XL= 3


# 設定data table的列數
rows_per_page = dbc.Row(
    [
        dbc.Label('Rows per pages'),
        dbc.Input(
            type='number',
            id=DATATABLE.PAGE.SIZE,
            value= CONFIG.PAGE_SIZE,
            min=1,
            max=481,
            step=1,
            style={
                'textAlign': 'left'
            }
        )
    ],
    style={
        'display': 'inline-block',
        'verticalAlign': 'right',
        'marginLeft': '90%'  # 把物件推到右邊去
    },
)


# data table
datatable = dash_table.DataTable(
    id=DATATABLE.TABLE,
    columns=[],
    data=[],
    merge_duplicate_headers=True,
    editable=True,
    page_current=0,
    page_size= CONFIG.PAGE_SIZE,
    page_count=0,
    page_action='custom',
    sort_action='custom',
    # sort_mode='single',
    sort_by=[],
    style_table={
        'overflow': 'scroll',
        'margin': '1%',
    },
    style_header={'border': '1px solid black'},
    style_cell={'border': '1px solid grey'},
)


# data table
@callback(
    [
        Output(DATATABLE.TABLE, 'data'),
        Output(DATATABLE.TABLE, 'columns'),
        Output(DATATABLE.TABLE, 'page_count'),
    ],
    [
        Input(LOAN.RESULT, 'data'),
        Input(DATATABLE.TABLE, 'page_current'),
        Input(DATATABLE.PAGE.SIZE, 'value')  # 調整列數
    ]
)
def update_datatable(
    kwargs,
    page_current,
    page_size_editable,
    ):
    df = calculator(**kwargs)
    page_size_editable = (
        page_size_editable if page_size_editable > 0 else 1
    )
    df_dash = convert_df_to_dash(df.iloc[page_current*page_size_editable: (page_current + 1) * page_size_editable]
                                     )

    pages = round((len(df.values) - 2) / page_size_editable, 0) + 1

    return df_dash[1],  df_dash[0], pages


# py -m Amort.dashboard.components.homepage.datatable
if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls.layout(),
                    ],
                    xs=CONFIG.SPLITS.XS,
                    sm=CONFIG.SPLITS.SM,
                    md=CONFIG.SPLITS.MD,
                    lg=CONFIG.SPLITS.LG,
                    xl=CONFIG.SPLITS.XL,
                ),                      
                dbc.Col(
                    [
                        rows_per_page,
                        datatable
                    ],
                    xs= 12 - CONFIG.SPLITS.XS,
                    sm= 12 - CONFIG.SPLITS.SM,
                    md= 12 - CONFIG.SPLITS.MD,
                    lg= 12 - CONFIG.SPLITS.LG,
                    xl= 12 - CONFIG.SPLITS.XL,
                )
            ],
            style={
                'marginTop': '2%',
                'marginBottom': '2%',
            },
        ),
        fluid=True
    )
    app.run_server(debug=True)