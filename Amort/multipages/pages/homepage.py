import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback, register_page, page_registry, dash_table
import dash_bootstrap_components as dbc
from collections import OrderedDict
import dash_mantine_components as dmc

from Amort.multipages.pages.toolkit import *
from Amort.multipages.pages import ids, amortization_types
from Amort.loan import calculator

# register_page(
#     __name__,
#     path= '/',
#     name= 'Home',
#     title= 'Index',
#     description= 'Homepage')

class config:
    PAGE_SIZE= 50

class className:
    DROPDOWN_BUTTON= 'dropdown-button'

def refreshable_dropdown(label, id, id_for_refreshment, disabled= False):
    dropdown = dbc.Row(
        [
            dbc.Col([
                dbc.Label(label),
                dcc.Dropdown(
                    id= id,
                    options= to_dropdown_options([*amortization_types]),
                    value= amortization_types,
                    multi= True,
                    searchable= True,
                    placeholder= 'Choose methods of the payment',
                    disabled= disabled
                    )
                ]
            ),
            dbc.Col([html.Button(
                'Refresh',
                className= className.DROPDOWN_BUTTON,
                id= id_for_refreshment,
                n_clicks= 0,
                    )
                ]
            ),
            ],
            className= 'mb-3'
        )
        # Refresh the Dropdown of the Payment options
    @callback(
        Output(id, 'value'),
        Input(id_for_refreshment, 'n_clicks')
    )
    def refresh_options(_:int) -> list[str]:
        return amortization_types
    return dropdown

controls= dbc.Card(
    [
        # Mortgage Amount
        dbc.Row(
            [
                dbc.Label(
                    'Mortgage Amount',
                    size= 'md'
                    ),
                dbc.Col(
                    dbc.Input(
                        type= 'number',
                        name= 'Mortgage Amount',
                        required= True,
                        id= ids.LOAN.TOTAL_AMOUNT,
                        placeholder= 'Input the mortgage amount',
                        min= 0,
                        step = 1,
                        value= 10_000_000,
                        style= {
                            'width': "100%",
                            'textAlign': 'left'
                            },
                        ),
                        width= 10
                ),
            ]
        ),

        # Down Payment Rate
        dbc.Row(
            [
                dbc.Label('Down Payment Rate'),
                dbc.Col(
                    dbc.InputGroup(
                        [dbc.Input(
                            type= 'number',
                            name= 'Down Payment Rate',
                            required= True,
                            id= ids.LOAN.DOWN_PAYMENT_RATE,
                            min= 0,
                            step= 10,
                            value= 20,
                            style= {
                                'textAlign': 'left'
                            }
                        ), dbc.InputGroupText('%')
                    ],
                    className="mb-3",
                    ),
                )
            ]
        ),
        
        # Payment Methods
        refreshable_dropdown(label= 'Payment methods', id= ids.LOAN.PAYMENT_OPTIONS, id_for_refreshment= ids.LOAN.REFRESH_ALL_OPTIONS),
        
        # Mortgage Period
        dbc.Row(
            [
                dbc.Label(
                    'Mortgate Term', 
                    size= 'md'
                    ),
                dbc.Col(
                    dbc.Input(
                        min= 1,
                        max= 40,
                        value= 30,
                        step= 1,
                        type= 'number',
                        id= ids.LOAN.PERIOD,
                        style= {
                            'textAlign': 'left'
                        })
                    )
        ]),
        # Grace Period
        dbc.Row(
            [
                dbc.Label(
                    'Grace Period',
                    size= 'md'
                    ),
                dbc.Col(
                    dbc.Input(
                        min= 0,
                        max= 5,
                        step= 1,
                        value= 0,
                        type= 'number',
                        id= ids.LOAN.GRACE,
                        style= {
                            'textAlign': 'left',
                        })
                    )  
            ]
        ),
        # Advanced Options
        dbc.Row(
            [
                dbc.Label('Advanced Options', size= 'md'),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                dbc.Checklist(
                                    options= [
                                        {'label': 'Prepay Plan', 'value': 0},
                                    ],
                                    id= ids.LOAN.PREPAY.OPTION,
                                    switch= True,
                                    inline= True,
                                    value= []
                                )
                            ),
                            dbc.CardBody(
                                [
                                    dbc.Label('Prepay Amount'),
                                    dbc.Input(
                                        id= ids.LOAN.PREPAY.AMOUNT,
                                        type= 'number',
                                        step= 1,
                                        value= [0],
                                        # min= [0],
                                        disabled= True,
                                    ),
                                    dbc.Label('Prepay Arrangement'),
                                    dbc.Input(
                                        id= ids.LOAN.PREPAY.ARR,
                                        value= [0],
                                        disabled= True,
                                    )
                                ]
                            ),
                        ],
                        className="mb-3",
                    )
                ),
                
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                dbc.Checklist(
                                        options= [
                                            {'label': 'Subsidy loan', 'value': 0}
                                        ],
                                        id= ids.LOAN.SUBSIDY.OPTION,
                                        switch= True,
                                        inline= True,
                                        value= []
                                    ),
                            ),
                            dbc.CardBody(
                                [
                                    dbc.Label('Subsidy Loan applied interest'),
                                    dbc.Checklist(
                                        options= [
                                            {'label': 'Adjustable-rate', 'value': 0}
                                        ],
                                        id= ids.LOAN.SUBSIDY.INTEREST_OPTION,
                                        switch= True,
                                        inline= True,
                                        value= [],
                                        className= "mb-3"
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Input(
                                                    children= [],
                                                    id= ids.LOAN.SUBSIDY.ARR,
                                                    disabled= True,
                                                ),
                                            ),
                                            dbc.Col(
                                                dbc.Input(
                                                    children= [],
                                                    id= ids.LOAN.SUBSIDY.INTEREST,
                                                    # value= [0],
                                                    step= 0.01,
                                                    disabled= True,
                                                ),
                                                className= '"w-100 bg-light border"'
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    'Add',
                                                    id= ids.LOAN.SUBSIDY.ADD,
                                                    n_clicks= 0,
                                                ), 
                                                # className= "ms-5"
                                            ),
                                        ],
                                        className= "d-flex flex-wrap align-items-start mb-3"                                      
                                    ),

                                    dbc.Label('Timepoint of Application'),
                                    dbc.Input(
                                        id= ids.LOAN.SUBSIDY.TIME,
                                        value= 0,
                                        step= 1,
                                        disabled= True,
                                    ),
                                    dbc.Label('Amount'),
                                    dbc.Input(
                                        id= ids.LOAN.SUBSIDY.AMOUNT,
                                        value= 0,
                                        step= 1,
                                        disabled= True,
                                    ),
                                    dbc.Label('Term'),
                                    dbc.Input(
                                        id= ids.LOAN.SUBSIDY.TERM,
                                        value= 20,
                                        step= 1,
                                        disabled= True,
                                    ),
                                    refreshable_dropdown(label= 'Payment method', id= ids.LOAN.SUBSIDY.METHOD, id_for_refreshment= ids.LOAN.SUBSIDY.REFRESH_ALL_OPTIONS)
                                ]
                            ),
                        ],  
                        className="mb-3",
                        outline= True,
                    )
                )
            ]
        )
    ],
    body= True,
)

# 設定data table的列數
rows_per_page= dbc.Row(
            [
                dbc.Label('Rows per pages'),
                dbc.Input(
                    type= 'number',
                    id= ids.PAGE_SIZE,
                    value= 12,
                    min= 1,
                    max= 481,
                    step= 1,
                    style= {
                        'textAlign': 'left'
                    }
                )
            ], 
            style= {
                'display': 'inline-block',
                'verticalAlign': 'right',
                'marginLeft': '90%' #把物件推到右邊去
                },
)


# data table
datatable= dash_table.DataTable(
            id= ids.DATA_TABLE,
            columns= [],
            data= [],
            merge_duplicate_headers= True,
            editable= True,
            page_current=0,
            page_size= config.PAGE_SIZE,
            page_count= 0,
            page_action='custom',
            sort_action='custom',
            # sort_mode='single',
            sort_by=[],
            style_table= {
                    'overflow': 'scroll',
                    'margin':'1%',
                    },
            style_header={ 'border': '1px solid black' },
            style_cell={ 'border': '1px solid grey' },
)

# Function of adding new interests to subsidy interest list
# @callback(
    # Output(ids.LOAN.SUBSIDY.INTEREST, 'children'),
    # Input(ids.LOAN.SUBSIDY.ADD, 'n_clicks'),
    # State(ids.LOAN.SUBSIDY.INTEREST, 'children')
# )
# def add_interest_to_subsidy(_, existing_interest):
    # existing_interest.append(dbc.Input())


# data table
@callback(
    [
        Output(ids.DATA_TABLE, 'data'), 
        Output(ids.DATA_TABLE, 'columns'),
        Output(ids.DATA_TABLE, 'page_count'),
    ],
    [
        Input(ids.LOAN.PAYMENT_OPTIONS, 'value'),
        Input(ids.LOAN.TOTAL_AMOUNT, 'value'),
        Input(ids.LOAN.DOWN_PAYMENT_RATE, 'value'),
        Input(ids.LOAN.PERIOD, 'value'),
        Input(ids.LOAN.GRACE, 'value'),
        Input(ids.LOAN.PREPAY.AMOUNT, 'value'),
        Input(ids.LOAN.PREPAY.ARR, 'value'),
        Input(ids.LOAN.SUBSIDY.AMOUNT, 'value'),
        Input(ids.LOAN.SUBSIDY.INTEREST, 'value'),
        Input(ids.LOAN.SUBSIDY.METHOD, 'value'),
        Input(ids.LOAN.SUBSIDY.TERM, 'value'),
        Input(ids.LOAN.SUBSIDY.TIME, 'value'),
        Input(ids.DATA_TABLE, 'page_current'),
        Input(ids.PAGE_SIZE, 'value')# 調整列數
    ]
)

def update_data_table(
    payment_options,
    loan_amount,
    down_rate,
    loan_period,
    grace_period,
    prepay_amount,
    prepay_arr, #[]
    subsidy_amount, #[]
    subsidy_interest, #[]
    subsidy_methods, #[]
    subsidy_term, 
    subsidy_time,
    page_current, 
    page_size_editable, 
    ):
    if payment_options == []:
        return None, None, None
    else:
        df = calculator(
            interest_arr= {'interest': [1.38]},
            total_amount= loan_amount,
            down_payment_rate= down_rate / 100,
            loan_period= loan_period, 
            grace_period= grace_period,
            prepay_arr= {
              'multi_arr': prepay_arr, 
              'amount': [prepay_amount], #[2_000_000, 200_0000]
              },
            subsidy_arr= {
              'interest': [subsidy_interest],#[1.01],
              'multi_arr':[], 
              'time': subsidy_time,#24, 
              'amount': subsidy_amount,#2_300_000, 
              'term': subsidy_term,#20,
              'method': subsidy_methods,
              },    
            method= payment_options
        )
        page_size_editable= (page_size_editable if page_size_editable > 0 else 1)
        df_dash= convert_df_to_dash(df.iloc[page_current*page_size_editable: (page_current + 1)* page_size_editable]
            )

        pages= round((len(df.values) - 2 ) / page_size_editable, 0) + 1
        
        return df_dash[1],  df_dash[0], pages

app= Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])

app.layout= dbc.Container(
            dbc.Row(
                [
                    dbc.Col(controls, 
                    xs= 4,
                    sm= 4,
                    md= 4,
                    lg= 2,
                    xl= 2),
                    dbc.Col(
                        [
                            rows_per_page,
                            datatable
                    ],
                    xs= 8,
                    sm= 8,
                    md= 8, 
                    lg= 10,
                    xl= 10,
                    )
                ],
                align= 'center'
            ),
            fluid= True
        )

# py -m Amort.multipages.pages.homepage
if __name__ == "__main__":
    app.run_server(debug= True)


# TODO:
# -[X] editable page_size
# -[X] 將row per page向右對齊
# -[X] 解決沒有Input造成錯誤的情況
# -[X] controls加入其他Arguments
# -[X] 嘗試將html.Div改成Boostrap.container
# -[X] 設定mortgage amount的Callback

# 2023/2/2 [X] 檢查那些arguements需要list，特別是subsidy，並設定正確的預設值
# 2023/2/2 [X] 解決少一欄目就產生錯誤的情形 "C:\Users\jank9\env_1111001\Amort\multipages\pages\toolkit.py", line 15,

# 2023/2/4
    # 1[] 設定Subsidy Adjustable rate切換功能
    # 若為Adjustable rate模式，欄位包含期間(subsidy-multi-arr)、利率(subsidy-interest)及新增功能(add-subsidy-interest-to-the-arrangement)
    # 2[] 設定新增功能(add-subsidy-interest-to-the-arrangement)的callback
    # refer: https://dash.plotly.com/pattern-matching-callbacks
    # 3[] Advanced options用Accordion component切換為collapsible lists



# -[] 垂直排列rows_per_page及datatable 
# refer: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

# -[] Matching pattern
# refer: https://dash.plotly.com/pattern-matching-callbacks

# Reference:
# ClassName設定layout: 
# https://dashcheatsheet.pythonanywhere.com/
# 
# Data Table editable: 
# https://dash.plotly.com/datatable/editable
# 
# Bootstrap: 
# https://www.youtube.com/watch?v=0mfIK8zxUds
# https://www.youtube.com/watch?v=VTO6Njy10dY

# Example
# https://dash-bootstrap-components.opensource.faculty.ai/examples/

# Form
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/form/
