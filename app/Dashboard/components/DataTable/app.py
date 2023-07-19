import pandas as pd  # type: ignore
from dash import Dash, html, Input, Output, dash_table, callback  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore

from app.Dashboard.components.ids import LOAN, DATATABLE
from app.Loan import df_schema  # type: ignore
from app.Dashboard.components.toolkit import convert_df_to_dash
from app.Dashboard.components.DataTable.controls import layout

class CONFIG:
    PAGE_SIZE = 24

    class SPLITS:
        XS = 6
        SM = 5
        MD = 5
        LG = 4
        XL = 3


# 設定data table的列數
rows_per_page = html.Div(
    [
        dbc.Label('Rows per pages'),
        dbc.Input(
            type='number',
            id=DATATABLE.PAGE.SIZE,
            value=CONFIG.PAGE_SIZE,
            min=1,
            max=481,
            step=1,
            style={
                # 'textAlign': 'center',
            },
            className='mb-3'
        )
    ],
    style={
        'display': 'inline-block',
        'verticalAlign': 'right',
        'marginLeft': '90%'  # 把物件推到右邊去
    },
)


# data table
def datatable():
    layout = html.Div(
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Label("Columns"),
                        dbc.Checklist(
                            options=[
                                {"label": v, "value": v} for v in [
                                    df_schema.level_2.PRINCIPAL,
                                    df_schema.level_2.INTEREST,
                                    df_schema.level_2.RESIDUAL
                                ]
                            ],
                            value=[
                                df_schema.level_2.PRINCIPAL,
                                df_schema.level_2.INTEREST,
                                df_schema.level_2.PAYMENT,  # 每期貸款為預選欄位，不可刪除
                                df_schema.level_0.TOTAL
                            ],
                            id=DATATABLE.COLUMN,
                            inline=True,
                        ),
                    ],
                    style={
                        'display': 'inline-block',
                        }
                ),
                rows_per_page,
                dbc.Row(
                    dash_table.DataTable(
                        id= DATATABLE.SUM,
                        # columns=[],
                        data=[],
                        merge_duplicate_headers=True,
                        editable=True,
                        page_current=0,
                        page_size=1,
                        page_count=0,
                        # page_action= 'custom',
                        sort_action='custom',
                        sort_by=[],
                        style_table={
                            'overflow': 'auto',
                            #  'margin': '5%',
                            'scrollX': True
                        },
                        style_header={
                            'textAlign': 'center',
                            'border': '1px solid black'
                        },
                        style_cell={
                            'border': '1px solid lightblue',
                        },
                    ),
                    className="mb-3"
                ),
                dbc.Row(
                    dash_table.DataTable(
                        id=DATATABLE.TABLE,
                        columns=[],
                        data=[],
                        merge_duplicate_headers=True,
                        editable=True,
                        page_current=0,
                        page_size=CONFIG.PAGE_SIZE,
                        page_count=0,
                        page_action='custom',
                        sort_action='custom',
                        # sort_mode='single',
                        sort_by=[],
                        style_table={
                            'overflow': 'auto',
                            'border': 'medium'
                            # 'margin': '5%',
                        },
                        style_header={
                            'textAlign': 'center',
                            'border': '1px solid black'
                        },
                        style_cell={
                            'border': '1px solid pink',
                        },
                    )
                )
            ]
        )
    )

    # data table
    @callback(
        [
            Output(DATATABLE.SUM, 'data'),
            Output(DATATABLE.SUM, 'columns'),
            Output(DATATABLE.TABLE, 'data'),
            Output(DATATABLE.TABLE, 'columns'),
            Output(DATATABLE.TABLE, 'page_count'),
            Output(DATATABLE.SUM, 'merge_duplicate_headers'),
            Output(DATATABLE.TABLE, 'merge_duplicate_headers'),
        ],
        [
            Input(LOAN.RESULT.DATAFRAME, 'data'),
            Input(DATATABLE.TABLE, 'page_current'),
            Input(DATATABLE.PAGE.SIZE, 'value'),  # 調整列數
            Input(DATATABLE.COLUMN, 'value'),
        ],
        prevent_initial_call=True,
    )
    def update_datatable(
        df,  # kwargs,
        page_current,
        page_size_editable,
        columns,
    ):
        merge_duplicate_headers = True
        df = pd.DataFrame.from_dict(df, 'tight')
        if df_schema.level_0.SUBSIDY in df.columns.levels[0]: #type: ignore
            
            df = df[[(l0, l1, l2) for (l0, l1, l2)
                     in df.columns if l2 in columns or l0 in columns]]
        else:
            df = df[[(l1, l2) for (l1, l2) in df.columns if l2 in columns]]
        if len(columns) == 1:  # avoid merging the columns if there is only one column
            merge_duplicate_headers = False
        page_size_editable = (
            page_size_editable if page_size_editable and page_size_editable > 0 else 1)
        df_dash = convert_df_to_dash(df[1:-1].iloc[(page_current * page_size_editable if page_current == 0 else (
            page_current * page_size_editable) + 1): ((page_current + 1) * page_size_editable) + 1])
        df_sum = convert_df_to_dash(df.tail(1))
        pages = round((len(df.values) - 2) // page_size_editable, 0)

        return df_sum[1], df_sum[0], df_dash[1],  df_dash[0], pages, merge_duplicate_headers, merge_duplicate_headers
    return layout


# py -m Dashboard.components.DataTable.app
if __name__ == "__main__":  
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True
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
    app.run_server(debug= True)
    # app.run_server(port=80, host= '0.0.0.0', debug=False, use_reloader=True)