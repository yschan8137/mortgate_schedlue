# pylint: disable=C0114
import math
from dash import Dash, html, Input, Output, callback
import dash_mantine_components as dmc
import time
from itertools import groupby

from app.Dashboard.assets.ids import LOAN, DATATABLE
from app.Loan import df_schema
from app.Dashboard.pages.components.Controls.panels import panel
from app.Dashboard.assets import specs


app = Dash(
    __name__, 
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap",
        "app/Dashboard/assets/style.css",
    ],
    suppress_callback_exceptions=True)


def create_table(df, **kwargs): 
    style = kwargs.get('style', {})
    style['textAlign'] = 'center'
    Index_name = kwargs.get('index', {}).get('name', 'Index')
    indexes, columns, values = df['index'], df['columns'], df['data']
    header = [html.Tr(
        [
            html.Th(value, rowSpan= (len(columns[0]) if value == Index_name else 1), colSpan= len([*col]), loading_state= {}, style= style) 
            for value, col in (groupby([Index_name] + [v[i] for v in columns]) if i== 0 else groupby([v[i] for v in columns]))
            ]
        ) 
        for i in range(len(columns[0]))
    ]
    rows = [
        html.Tr(
            [html.Td(index, style= {'textAlign': 'center'}
                    )
            ] + [html.Td(cell, style= style) for cell in row]) for index, row in zip(indexes, values)
    ]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


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
        dmc.NumberInput(
            label= 'Rows per pages',
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
def table():
    layout = html.Div(
        dmc.Stack(
            [
                dmc.Group(
                    children= [
                        dmc.Stack(
                            [
                                dmc.CheckboxGroup(
                                    [
                                        dmc.Checkbox(
                                            label= v, 
                                            value= v,
                                        ) for v in [
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
                                    id= DATATABLE.COLUMN,
                                    style= specs.DATAFRAME.COLUMN_CHECKBOX.STYLE,
                                )
                            ]
                        ),
                        rows_per_page,
                    ],
                ),
                dmc.LoadingOverlay(
                    [
                        dmc.Table(
                            children= [],
                            id= DATATABLE.SUM,
                            striped= True,
                            highlightOnHover=True,
                            withBorder=True,
                            withColumnBorders=True,
                            verticalSpacing="xs",
                            horizontalSpacing=10,
                            style= {
                                'width': '100%',
                                'whiteSpace': 'nowrap',
                            },
                        ),
                        dmc.Space(h= 10),
                        dmc.Table(
                            children= [],
                            id= DATATABLE.TABLE,
                            striped= True,
                            highlightOnHover=True,
                            withBorder=True,
                            withColumnBorders=True,
                            verticalSpacing="xs",
                            horizontalSpacing=10,
                            style= {
                                'width': '100%',
                                'whiteSpace': 'nowrap',
                            },
                        ),
                        dmc.Space(h= 5),
                        dmc.Pagination(
                            total= 1,
                            page= 1,
                            siblings=1, 
                            withControls= True,
                            withEdges= True,
                            position= 'right',
                            id= 'page_current',
                        ),
                    ],
                    loaderProps= {
                        "variant": "bars",
                        "color": "yellow", 
                        "size": "lg",
                        'is_loading': True,
                    },
                    transitionDuration= 0.5,
                )
            ],
            
        ),
        style= {
            'height': '100%',
            'overflow-x': 'auto',
            'padding-bottom': '10px',
        },
        className= 'custom-section',
    )


    ## data table
    @callback(
            Output(DATATABLE.TABLE, 'children'),
            Output(DATATABLE.SUM, 'children'),
            Output('page_current', 'total'),
            Output('page_current', 'page'),
        [
            Input(LOAN.RESULT.DATAFRAME, 'data'),
            Input('page_current', 'page'),
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
        data= data['data']
        if df_schema.level_0.SUBSIDY in [col[0] for col in data['columns']]:
            data['data'] = [*map(lambda x: [f"{round(x[n]):,}" for n, col in enumerate(data['columns']) if col[2] in columns or col[0] in columns], data['data'])]
            data['columns'] = [col for col in data['columns'] if col[2] in columns or col[0] in columns]
        else:
            data['data'] = [*map(lambda x: [f"{round(x[n]):,}" for n, col in enumerate(data['columns']) if col[1] in columns], data['data'])]
            data['columns'] = [col for col in data['columns'] if col[1] in columns]
        pages = math.ceil((len(data['data']) - 2) / page_size_editable)
        page_size_editable = (
            page_size_editable if page_size_editable and page_size_editable > 0 else 1)
        if page_current > pages:
            page_current = pages
        elif page_current == 0:
            page_current = 1
        tb= create_table({k: (v if k not in ['data', 'index'] 
                   else (v[((page_current - 1) * page_size_editable) + 1: (page_current * page_size_editable) + 1] if len(v) > (page_current * page_size_editable) + 1 else v[((page_current - 1) * page_size_editable) + 1:-1])
                ) for k, v in data.items()}, style= {'textAlign': 'center', 'fontWeight': 'bold'})
        sum_tb= create_table(
            {k: (v if k not in ['data', 'index'] 
                   else [v[-1]]) for (k, v) in data.items()
            },
            style= {'textAlign': 'center', 'fontWeight': 'bold'}
        )
        return tb, sum_tb, pages, page_current
    
    return layout

# python app/Dashboard/pages/components/DataTable/table.py
# py -m app.Dashboard.pages.components.DataTable.table
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
    # df= calculator(**default_kwargs)

    app.layout = dmc.MantineProvider(
        [
            panel.register(),
            table()
        ]
    )
    
    app.run_server(debug= True, threaded= True)