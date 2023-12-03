import math
import dash
from dash import Dash, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import time
from itertools import groupby

from app.Dashboard.assets.ids import LOAN, DATATABLE
from app.Loan import df_schema
from app.Dashboard.pages.components.toolkit import convert_df_to_dash
from app.Dashboard.pages.components.Controls.panels import panel
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
                                dmc.Title("Columns", order= 3),
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
                                        # df_schema.level_2.PAYMENT,  # 每期貸款為預選欄位，不可刪除
                                        # df_schema.level_0.TOTAL
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
        data,
        page_current,
        page_size_editable,
        columns,
        ):
        if df_schema.level_0.SUBSIDY in [col[0] for col in data['columns']]:
            data['data'] = [*map(lambda x: [f"{round(x[n]):,}" for n, col in enumerate(data['columns']) if col[2] in columns or col[0] in columns], data['data'])]
            data['columns'] = [col for col in data['columns'] if col[2] in columns or col[0] in columns]
        else:
            data['data'] = [*map(lambda x: [f"{round(x[n]):,}" for n, col in enumerate(data['columns']) if col[1] in columns], data['data'])]
            data['columns'] = [col for col in data['columns'] if col[1] in columns]

        if len(columns) == 1:  # avoid merging the columns if there is only one column
            merge_duplicate_headers = False
        else:
            merge_duplicate_headers = True
        page_size_editable = (
            page_size_editable if page_size_editable and page_size_editable > 0 else 1)
        pages = math.ceil((len(data['data']) - 2) / page_size_editable)
        df_dash= convert_df_to_dash(
            {k: (v if k not in ['data', 'index'] 
                   else (v[(page_current * page_size_editable) + 1: ((page_current + 1) * page_size_editable) + 1] if len(v) >= ((page_current + 1) * page_size_editable) + 1 else v)
                )    
                for (k, v) in data.items()
            }
        )
        df_sum = convert_df_to_dash(
            {k: (v if k not in ['data', 'index'] 
                   else [v[-1]]) for (k, v) in data.items()
            }
        )
        return df_sum[1], df_sum[0], df_dash[1], df_dash[0], pages, merge_duplicate_headers, merge_duplicate_headers
    return layout

def deployment():
    layout = dbc.Container(
        [
            datatable()
        ],
        fluid=True
    )
    return layout

# use dmc to create data table
def create_table(df, **kwargs):
    style= kwargs.get('style', {})
    style['textAlign']= 'center'
    Index_name= kwargs.get('index', {}).get('name', 'Index')
    indexes, columns, values = df['index'], df['columns'], df['data']
    header = [html.Tr([html.Th(value, rowSpan= (len(columns[0]) if value == Index_name else 1), colSpan= len([*col]), loading_state= {}, style= style) for value, col in (groupby([Index_name] + [v[i] for v in columns]) if i== 0 else groupby([v[i] for v in columns])) ]) for i in range(len(columns[0]))]
    rows = [
        html.Tr(
            [html.Td(index, style= {'textAlign': 'center'})] + [html.Td(cell, style= style) for cell in row]) for index, row in zip(indexes, values)
    ]
    table = [html.Thead(header), html.Tbody(rows)]
    return table




# py -m app.Dashboard.pages.components.DataTable.dataframe
if __name__ == "__main__":
    from app.Loan import calculator, default_kwargs
    default_kwargs['subsidy_arr'] = {
        'interest_arr': {'interest': [1, 1.33], 'time': [10]},
        'start': 2,
        'amount': 15_000,
        'tenure': 20,
        'grace_period': 0,
        'prepay_arr': {'amount': [], 'time': []},
        'method': ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL'],

    }
    df= calculator(**default_kwargs)
    # columns, data = df['columns'], df['data']
    app.layout= dmc.Table(
        create_table(df),
        striped= True,
        highlightOnHover=True,
        withBorder=True,
        withColumnBorders=True,
        verticalSpacing="xs",
        horizontalSpacing=10,
        # style= {
            # 'height': '100vh',
        # }
    )
    # app.layout = dbc.Container(
        # [
            # panel.register(),
            # deployment()
        # ]
    # )
    # print(create_table(df))
    
    app.run_server(debug= True)
    # app.run_server(port=80, host= '0.0.0.0', debug=False, use_reloader=True)