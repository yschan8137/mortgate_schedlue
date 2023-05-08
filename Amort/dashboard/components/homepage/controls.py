# This file is the collection of control components for the homepage

from dataclasses import dataclass
from gc import disable
from re import S
from sre_constants import IN
from unittest.mock import call
from dash import Dash, html, dcc, Input, Output, State, callback, MATCH, ALL, ALLSMALLER
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from numpy import place

from .. import amortization_types
from .widgets import refreshable_dropdown, addon
from ..ids import *
from ..toolkit import suffix_for_type

# TODO:
# [X] 1. resolve the issues of the missing id while accordion hasn't been toggled. 
# [X] 2. collect the all result from all inputs.
# [X] 3. enable the format for multi-stage interest rate, which combines results of the sigle interest rate and the addon on multi-stage interest rates.
        
@dataclass
class MortgageOptions:
    type= LOAN.TYPE

    # Mortgage Amount
    amount = html.Div(
        [
            dbc.Label(
                'Mortgage Amount',
                size='md'
            ),
            dbc.Col(
                dbc.Input(
                    type='number',
                    name='Mortgage Amount',
                    required=True,
                    id=suffix_for_type(LOAN.AMOUNT, type),
                    placeholder='Enter the loan amount',
                    min=0,
                    step=1,
                    value=10_000_000,
                    style={
                        # 'width': "20%",
                        'textAlign': 'left'
                    },
                ),
                # width=10
            ),
        ]
    )

    # Down Payment Rate
    down_payment = html.Div(
        [
            dbc.Label('Down Payment Rate'),
            dbc.Col(
                dbc.InputGroup(
                    [dbc.Input(
                        type='number',
                        name='Down Payment Rate',
                        required=True,
                        id=LOAN.DOWNPAYMENT,
                        min=0,
                        max=100,
                        step=10,
                        value=20,
                        style={
                            'textAlign': 'left'
                        }
                    ), dbc.InputGroupText('%')
                    ],
                    style={
                        # 'width': "15%",
                    }
                ),
            )
        ]
    )

    # Mortgage Period
    @classmethod
    def term(cls): 
        return html.Div(
            [
                dcc.Store(suffix_for_type('momory for the term', cls.type), data= []),
                dbc.Label(
                    'Mortgate Term',
                    size='md'
                ),
                dbc.Col(
                    dbc.Input(
                        min=1,
                        max=40,
                        value=30,
                        step=1,
                        type='number',
                        id= LOAN.TERM,
                        style={
                            # 'width': "10%",
                            'textAlign': 'left'
                        }
                    )
                )
            ]
        )
    # Grace Period
    grace = html.Div(
        [
            dbc.Label(
                'Grace Period',
                size='md'
            ),
            dbc.Col(
                dbc.Input(
                    min=0,
                    max=5,
                    step=1,
                    value=0,
                    type='number',
                    id=suffix_for_type(LOAN.GRACE, type),
                    style={
                        # 'width': "10%",
                        'textAlign': 'left',
                    }
                )
            )
        ]
    )

    # Payment Methods
    dropdown_refresh = html.Div(
        [
            refreshable_dropdown(
                label='Payment methods',
                type= LOAN.TYPE,
                options=amortization_types
            )
        ]
    )


    @classmethod
    def interest_rate(
        cls,
        value= 0,
        type: str = None,  # type: ignore
        label: str = 'Multistage Interest Rate',
        placeholder='Input the interest rate',
    ):
        layout = html.Div(
            [
                html.Div(
                    [
                        dbc.Label('Applied Interest'),
                        dbc.InputGroup(
                            [
                                dbc.Input(
                                    id=suffix_for_type(LOAN.INTEREST, type),
                                    type='float',
                                    step= 0.01,
                                    value=value,
                                    min=0.0,
                                    max= 100.0
                                ),
                                dbc.InputGroupText('%')
                            ],
                            style={
                                # ''
                                # 'width': "20%",
                            },
                            className= 'mb-2'
                        )
                    ]
                ),
                dbc.Checklist(
                    options=[
                        {'label': label, 'value': 1}
                    ],
                    value=[0],
                    id=suffix_for_type(ADVANCED.TOGGLE.BUTTON, type),
                    inline=True,
                    switch=True,
                ),
                html.Div(
                    [html.Div(
                        [
                            addon(
                                    type= type,  # type: ignore
                                    dropdown_label= 'Time',
                                    pattern_matching= True, # avoid the errors regarding the nonexistent objects.
                                    placeholder= placeholder,
                            )
                        ],
                        style= {
                            'display': 'none',
                            "maxWidth": "400px"
                                },
                        id= suffix_for_type('toggle to show the options', type)
                    ),
                     ],
                )
            ],
            className='mb-3'
        )
        @callback(
            Output(suffix_for_type('toggle to show the options', type), 'style'),
            Output(suffix_for_type('momory for the term', LOAN.TYPE), 'data', allow_duplicate=True), # type: ignore
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            State(LOAN.TERM, 'value'),
            State(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def toggle_options(
            value,
            term,
            memory
            ):
            if value[-1] == 1:
                memory.append(term)
                return {'display': 'block'}, memory
            else:
                return {'display': 'none'}, memory
        
        @callback(
            Output(suffix_for_type('momory for the term', LOAN.TYPE), 'data', allow_duplicate=True), # type: ignore
            Input(LOAN.TERM, 'value'),
            State(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def update_momery_of_term(term, memory):
            memory.append(term)
            return memory
        
        return layout
    
    @classmethod
    def setup(cls):
        layout= html.Div(
                    [
                        dcc.Store(
                            id= suffix_for_type(LOAN.RESULT, cls.type),
                            data= {
                                'interest_arr': {'interest': [], 'multi_arr': []},
                                'total_amount': 0,
                                'down_payment_rate': 0,
                                'loan_period': 0,
                                'grace_period': 0,
                                'method':['EQUAL_TOTAL', 'EQUAL_PRINCIPAL']
                            }
                        ),
                        cls.amount,
                        cls.interest_rate(
                            type= cls.type,
                            value= 1.38  # type: ignore
                        ),
                        cls.down_payment,
                        cls.term(),
                        cls.grace,
                        cls.dropdown_refresh,
                    ]
                )
        @callback(
            Output(suffix_for_type(LOAN.RESULT, cls.type), 
                   'data', 
                   ),
            Input(suffix_for_type(LOAN.AMOUNT, cls.type), 'value'),
            Input(suffix_for_type(LOAN.GRACE, cls.type), 'value'),
            Input(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, cls.type), 'value'),
            Input(LOAN.TERM, 'value'),
            Input(LOAN.DOWNPAYMENT, 'value'),
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, cls.type), 'value'),
            Input(suffix_for_type(LOAN.INTEREST, cls.type), 'value'),
            Input(suffix_for_type(ADDON.MEMORY, cls.type), 'data'),
            State(suffix_for_type(LOAN.RESULT, cls.type), 'data'),
        )
        def update_result_for_loan(
            loan_amount,
            grace_period,
            repayment_options,
            term,
            downpayment_rate,
            multi_stage_interest,
            interest,
            arr,
            memory
        ):
            memory['total_amount'] = loan_amount
            memory['grace_period'] = grace_period
            memory['method'] = repayment_options
            memory['interest_arr'] = {
                'interest': [[interest, *arr.values()] if multi_stage_interest[-1] == 1 else [interest]][-1], 
                'multi_arr': [[int(v) for v in arr.keys()] if multi_stage_interest[-1] == 1 else []][-1]
            }
            memory['loan_period'] = term
            memory['down_payment_rate'] = downpayment_rate/100
            return memory
        
        return layout


@ dataclass
class AdvancedOptions:
    #  accordion
    @ classmethod
    def accordion(cls, **kwargs):
        """
        Arguments:
            - content(list): a list of items for the specification of title and children of the accordion as follows:
                [
                    {
                        'id': the id of the accordion,
                        'title': the title of the accordion,
                        'children': the content children in the accordion
                    },
                ...
                ]
            - style(dict): the style of the accordion
        """
        titles = [c.get('title', None) for c in kwargs.get('content', [])]
        childrens = [c.get('children', None)
                     for c in kwargs.get('content', [])]
        style = kwargs.get('style', None)
        away_open = kwargs.get('away_open', True)
        
        #  prevent the width of the accordion component to be 100% of the screen

        layout = html.Div(
            [

                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            children=children,
                            title=title,
                            id= 'accordion-{}'.format(title),
                            item_id= title, 
                            style= {"maxWidth": "400px"}
                        ) for title, children in zip(titles, childrens)
                    ],
                    id=f"accordion",
                    always_open=away_open,
                    start_collapsed=True,
                    flush=True,
                    style=style,
                ),
            ],
        )

        return layout

    # prepayment

    @ classmethod
    def prepayment(cls, type=LOAN.PREPAY.TYPE):
        layout = html.Div(
            [
                dcc.Store(
                    suffix_for_type(LOAN.RESULT, LOAN.PREPAY.TYPE),
                    data= {
                        'prepay_arr':{
                              'multi_arr': [],
                              'amount': []
                          }
                    }
                ),
                dbc.Label(
                    'Prepay Arrangement',
                    size='md',
                ),
                addon(
                    type=type,
                    dropdown_label='Time',
                    pattern_matching=True,
                    placeholder='Input Prepay Arrangement',
                )
            ]
        )
        @ callback(
            Output({'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, type)}, 'data'),
            Input(LOAN.TERM, 'value'),
        )
        def update_prepay_arrangement(term):
            return [[1, term - 1]]
        
        # Toggle the addon setting for prepay
        @callback(
                Output(suffix_for_type(ADDON.INPUT, type), 'type'),
                Output(suffix_for_type(ADDON.INPUT, type), 'step'),
                Output(suffix_for_type(ADDON.INPUT, type), 'max'),
                [Input('accordion', 'active_item')],
                State(suffix_for_type(LOAN.AMOUNT, LOAN.TYPE), 'value'),
                prevent_initial_call=True,
        )
        def toggle_prepay_arrangement(_, amount):
            if _ and _[0] == LOAN.PREPAY.TYPE:
                return 'number', 1, amount, 
            else:
                return 'flaot', 0.01, 100


        @callback(
            Output(suffix_for_type(LOAN.RESULT, type), 'data'), # type: ignore
            Input(suffix_for_type(ADDON.MEMORY, type), 'data'),
            State(suffix_for_type(LOAN.RESULT, type), 'data'),
        )
        def update_result_for_prepay(arr, memory):
            memory['prepay_arr'] = {
                'amount': [*arr.values()], 
                'multi_arr': [int(v) for v in arr.keys()]
            }
            return memory
        
        return layout

    # subsidy

    @ classmethod
    def subsidy(cls, type=LOAN.SUBSIDY.TYPE):
        layout = html.Div(
            [
                dcc.Store( 
                    suffix_for_type(LOAN.RESULT, type),
                    data= {                
                        'subsidy_arr': {
                            'interest': [],
                            'multi_arr': [],
                            'time': 0,
                            'amount': 0,
                            'term': 0,
                            'grace_period': 0,
                            'prepay_arr': {'amount': [], 'multi_arr': []},
                            'method': ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL']
                        },
                    }
                ),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        dbc.Label('Subsidy Amount'),  # 優惠貸款金額
                                        dbc.Input(
                                            id= suffix_for_type(LOAN.AMOUNT, type),
                                            type='number',
                                            step=1,
                                            value=0,
                                            min=0,
                                        ),
                                    ]
                                ),
                                MortgageOptions.interest_rate(
                                    type= type,
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Subsidy Start timepoint'),
                                        dbc.Input(
                                            id=LOAN.SUBSIDY.START,
                                            type='number',
                                            step=1,
                                            value=0,
                                            min=0,
                                            max=24,
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Subsidy Term'),
                                        dbc.Input(
                                            id= LOAN.SUBSIDY.TERM,
                                            type='number',
                                            step=1,
                                            value=0,
                                            min=0,
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Subsidy Grace Period'),
                                        dbc.Input(
                                            id=suffix_for_type(LOAN.GRACE, type),
                                            type='number',
                                            step=1,
                                            value=0,
                                            min=0,
                                        )
                                    ]
                                ),
                                refreshable_dropdown(
                                    label='Subsidy Payment methods',
                                    type=LOAN.SUBSIDY.TYPE,
                                    options=amortization_types),
                                html.Div(
                                    [
                                        dbc.Checklist(
                                            options=[
                                                {'label': 'Prepayment', 'value': 1},
                                            ],
                                            value=[0],
                                            id=LOAN.SUBSIDY.PREPAY.OPTION,
                                            inline=True,
                                        ),
                                        html.Div(
                                            children=addon(
                                                # addition of extra string to avoid conflict with other addons
                                                type= LOAN.SUBSIDY.PREPAY.TYPE,
                                                dropdown_label='Time',
                                                placeholder='Input Prepay Arrangement',
                                                disabled=True,
                                            ),
                                            id=LOAN.SUBSIDY.PREPAY.ARR
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="mb-3 w-auto",
                ),
            ]
        )
        @callback(
            Output({'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.TYPE)}, 'data'),
            Input(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def update_arrangement(memory):
            if len(memory) == 0:
                return PreventUpdate()
            else:
                return [[1, memory[-1] - 1]]                                          

        @callback(
            Output({'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.SUBSIDY.TYPE)}, 'data'),
            Input(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            Input(LOAN.SUBSIDY.START, 'value'),
            prevent_initial_call=True,
        )
        def update_subsidy_arrangement(
            memory,
            start
            ):
            if len(memory) == 0:
                return PreventUpdate()
            else:
                return [[start, memory[-1] - 1]]                                  

        @callback(
            Output(suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.SUBSIDY.PREPAY.TYPE), 'data'), # type: ignore
            Input(LOAN.SUBSIDY.TERM, 'value'),
            Input(LOAN.SUBSIDY.START, 'value'),
        )
        def update_subsidy_prepay_arrangement(
            period,
            start,
            ):
            return [[start, period + start - 1]]

        @callback(
            Output(suffix_for_type(ADDON.INPUT, LOAN.SUBSIDY.PREPAY.TYPE),
                   'disabled', allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.DROPDOWN.MENU, LOAN.SUBSIDY.PREPAY.TYPE),
                   'disabled', allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.ADD, LOAN.SUBSIDY.PREPAY.TYPE), 'disabled',
                   allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.DELETE, LOAN.SUBSIDY.PREPAY.TYPE), 'disabled',
                   allow_duplicate=True),  # type: ignore
            Input(LOAN.SUBSIDY.PREPAY.OPTION, 'value'),
            prevent_initial_call=True
        )
        def control_disabled(value):
            if value[-1] == 1:
                return [False] * 4
            else:
                return [True] * 4
        
        @callback(
            Output(suffix_for_type(LOAN.RESULT, type), 'data'), # type: ignore
            Input(suffix_for_type(LOAN.AMOUNT, type), 'value'),
            Input(suffix_for_type(LOAN.GRACE, type), 'value'),
            Input(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, type), 'value'),
            Input(suffix_for_type(ADDON.MEMORY, LOAN.SUBSIDY.PREPAY.TYPE), 'data'),
            Input(LOAN.SUBSIDY.START, 'value'),
            Input(LOAN.SUBSIDY.TERM, 'value'),
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            Input(suffix_for_type(LOAN.INTEREST, type), 'value'),
            Input(suffix_for_type(ADDON.MEMORY, type), 'data'),
            State(suffix_for_type(LOAN.RESULT, type), 'data'),
        )
        def update_result_for_subsidy(
            loan_amount,
            grace_period,
            repayment_options,
            prepay_arr,
            start,
            term,
            multi_stage_interest,
            interest,
            arr,
            memory
        ):
            memory['subsidy_arr'] = {
                'amount': loan_amount,
                'time': grace_period,
                'grace_period': grace_period,
                'method': repayment_options,
                'multi_arr': [[int(v) for v in arr.keys()] if multi_stage_interest[-1] == 1 else []][-1],
                'interest': [[interest, *arr.values()] if multi_stage_interest[-1] == 1 else [interest]][-1],
                'prepay_arr': {
                    'multi_arr': [int(v) for v in prepay_arr.keys()],
                    'amount': [*prepay_arr.values()],    
                },
                'term': term,
                'time': start
            }
            return memory

        return layout


# layout
def layout():
    layout = html.Div(
                 [
                     dcc.Store(suffix_for_type(LOAN.RESULT, 'all'), data={}),
                     dbc.Card(
                         [
                             dbc.CardBody(
                                 [
                                     MortgageOptions.setup(),
                                     html.Div(
                                         [
                                             AdvancedOptions.accordion(
                                                 style={
                                                     'display': 'inline-block',
                                                     'active-bg': 'red',
                                                 },
                                                 content=[
                                                     {
                                                         'id': title,
                                                         'title': title,
                                                         'children': children
                                                     } for title, children in zip(
                                                                                  [LOAN.PREPAY.TYPE,  LOAN.SUBSIDY.TYPE], 
                                                                                  [AdvancedOptions.prepayment(),   AdvancedOptions.subsidy()]
                                                                              )
                                                 ]
                                             )
                                         ],
                                     ),
                                 ],
                             )
                         ],
                         body=True,
                     )
                 ]
             )
    @callback(
        Output(suffix_for_type(LOAN.RESULT, 'all'), 'data'),
        Input(suffix_for_type(LOAN.RESULT, LOAN.TYPE), 'data'),
        Input(suffix_for_type(LOAN.RESULT, LOAN.SUBSIDY.TYPE), 'data'),
        Input(suffix_for_type(LOAN.RESULT, LOAN.PREPAY.TYPE), 'data'),
    )
    def consolidate_result(
        loan_result,
        subsidy_result,
        prepay_result,
    ):
        # print('result: ', {**loan_result, **subsidy_result, **prepay_result})
        return {**loan_result, **subsidy_result, **prepay_result}
    return layout

# py -m Amort.dashboard.components.homepage.controls
if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    app.layout = layout()

    app.run_server(debug=True)

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
    # refer to: https://dash.plotly.com/pattern-matching-callbacks
    # 3[] Advanced options用Accordion component切換為collapsible lists

    # 2023/3/29
    # [] buttongroup搭配

    # [X 垂直排列rows_per_page及datatable
    # refer: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

    # [X] Matching pattern
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
