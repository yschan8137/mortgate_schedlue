import math
import pandas as pd  # type: ignore
import dash
from dash import Dash, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc  # type: ignore

from app.Dashboard.assets.ids import LOAN, DATATABLE
from app.Loan import df_schema  # type: ignore
from app.Dashboard.pages.components.toolkit import convert_df_to_dash
from app.Dashboard.pages.components.Controls.panels import panel, register
from app.Dashboard.assets import specs


app = Dash(__name__, 
       external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP],
       suppress_callback_exceptions=True,
       ) 

class CONFIG:
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
            value= specs.DATAFRAME.ROWS.SIZE,
            min=1,
            max=481,
            step=1,
            style={
                # 'textAlign': 'center',
            },
            className='mb-3'
        )
    ],
    className="ms-auto",
    style= specs.DATAFRAME.ROWS.STYLE,
)


# data table
def datatable():
    layout = html.Div(
        dbc.Col(
            [
                dbc.Stack(
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
                            style= specs.DATAFRAME.COLUMN_CHECKBOX.STYLE,
                        ),
                        rows_per_page,
                    ],
                    direction= 'horizontal',
                    gap= 3,
                    style= {}
                ),
                dbc.Row(
                    dash_table.DataTable(
                        id= DATATABLE.SUM,
                        data=[],
                        merge_duplicate_headers=True,
                        editable=True,
                        page_current=0,
                        page_size=1,
                        page_count=0,
                        sort_action='custom',
                        sort_by=[],
                        style_table= specs.DATAFRAME.SUM.STYLE.TABLE,
                        style_header= specs.DATAFRAME.SUM.STYLE.HEADER,
                        style_cell= specs.DATAFRAME.SUM.STYLE.CELL,
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
                        page_size= specs.DATAFRAME.ROWS.SIZE,
                        page_count=0,
                        page_action='custom',
                        sort_action='custom',
                        # sort_mode='single',
                        # fixed_rows= {'headers': True, 'data': 1},
                        sort_by=[],
                        style_table= specs.DATAFRAME.CONTENT.STYLES.TABLE,
                        style_header= specs.DATAFRAME.CONTENT.STYLES.HEADER,
                        style_cell= specs.DATAFRAME.CONTENT.STYLES.CELL,
                    )
                )
            ],
        ),
        style= specs.DATAFRAME.CONTENT.STYLE,
        className= 'custom-scrollbar',
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
    )
    def update_datatable(
        data,  # kwargs,
        page_current,
        page_size_editable,
        columns,
    ):
        merge_duplicate_headers = True
        df = pd.DataFrame.from_dict(data, 'tight')
        dff = df.map(lambda x: f"{round(x):,}") #type: ignore
        if df_schema.level_0.SUBSIDY in df.columns.levels[0]: #type: ignore
            dataset = dff[[(l0, l1, l2) for (l0, l1, l2)
                     in df.columns if l2 in columns or l0 in columns]]
        else:
            dataset = dff[[(l1, l2) for (l1, l2) in df.columns if l2 in columns]]
        if len(columns) == 1:  # avoid merging the columns if there is only one column
            merge_duplicate_headers = False
        page_size_editable = (
            page_size_editable if page_size_editable and page_size_editable > 0 else 1)
        df_dash = convert_df_to_dash(dataset[0:-1].iloc[(page_current * page_size_editable) + 1: ((page_current + 1) * page_size_editable) + 1])
        df_sum = convert_df_to_dash(dataset.tail(1))
        pages = math.ceil((len(dataset.values) - 2) / page_size_editable)

        return df_sum[1], df_sum[0], df_dash[1],  df_dash[0], pages, merge_duplicate_headers, merge_duplicate_headers
    
    return layout

def deployment():
    layout = dbc.Container(
        [
            datatable()
        ],
        fluid=True
    )
    return layout


# py -m app.Dashboard.pages.components.DataTable.app
if __name__ == "__main__":  
    app.layout = dbc.Container(
        [
            register(),
            deployment()
        ]
    )
    
    app.run_server(debug= True)
    # app.run_server(port=80, host= '0.0.0.0', debug=False, use_reloader=True)