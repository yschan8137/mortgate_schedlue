# This file is the collectikwargs_schemaon of control components for the homepage

from dataclasses import dataclass
from gc import disable
from re import I, S
from sre_constants import IN
from unittest.mock import call
from dash import Dash, html, dcc, Input, Output, State, MATCH, ALL, ALLSMALLER, no_update, callback_context, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from numpy import place
# from traitlets import default
from time import time

from Dashboard.components import amortization_types
from Dashboard.components.DataTable.widgets import refreshable_dropdown, addon
from Dashboard.components.ids import *
from Dashboard.components.toolkit import suffix_for_type
from Loan.main import calculator

# TODO:
# [X] 1. resolve the issues of the missing id while accordion hasn't been toggled.
# [X] 2. collect the all result from all inputs.
# [X] 3. enable the format for multi-stage interest rate, which combines results of the sigle interest rate and the addon on multi-stage interest rates.

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )

kwargs_schema = {
    'interest_arr': {'interest': [1.38], 'time': []},
    'total_amount': 10_000_000,
    'down_payment_rate': 20,
    'tenure': 30,
    'grace_period': 0,
    'method': ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL'],
    'prepay_arr': {
        'amount': [],
        'time': []
    },
    'subsidy_arr': {
        'interest': [0],
        'time': [],
        'start': 0,
        'amount': 0,
        'tenure': 0,
        'grace_period': 0,
        'prepay_arr': {'amount': [], 'time': []},
        'method': ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL']
    },
}


@dataclass
class MortgageOptions:
    type = LOAN.TYPE
    app= app
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
                    value=kwargs_schema['total_amount'],
                    style={
                        'textAlign': 'left'
                    },
                ),
            ),
        ]
    )

    @callback(
        Output(LOAN.RESULT.KWARGS, 'data',
               allow_duplicate=True),  # type: ignore
        Input(suffix_for_type(LOAN.AMOUNT, type), 'value'),
        State(LOAN.RESULT.KWARGS, 'data'),
        prevent_initial_call=True
    )
    def _amount(total_amount, memory):
        if total_amount is None:
            raise PreventUpdate
        else:
            memory['total_amount'] = total_amount
        return memory

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
                        value=kwargs_schema['down_payment_rate'],
                        style={
                            'textAlign': 'left'
                        }
                    ), dbc.InputGroupText('%')
                    ],
                ),
            )
        ]
    )

    @callback(
        Output(LOAN.RESULT.KWARGS, 'data',
               allow_duplicate=True),  # type: ignore
        Input(LOAN.DOWNPAYMENT, 'value'),
        State(LOAN.RESULT.KWARGS, 'data'),
        prevent_initial_call=True
    )
    def _down_payment(downpayment_rate, memory):
        if downpayment_rate is None:
            return no_update
        else:
            memory['down_payment_rate'] = downpayment_rate
        return memory

    # Mortgage Period
    @classmethod
    def tenure(cls):
        return html.Div(
            [
                dcc.Store(suffix_for_type(
                    'momory for the tenure', cls.type), data=[]),
                dbc.Label(
                    'Mortgate tenure',
                    size='md'
                ),
                dbc.Col(
                    dbc.Input(
                        min=1,
                        max=40,
                        value=kwargs_schema['tenure'],
                        step=1,
                        type='number',
                        id=LOAN.TENURE,
                        style={
                            # 'width': "10%",
                            'textAlign': 'left'
                        }
                    )
                )
            ]
        )

    @callback(
        Output(LOAN.RESULT.KWARGS, 'data',
               allow_duplicate=True),  # type: ignore
        Input(LOAN.TENURE, 'value'),
        State(LOAN.RESULT.KWARGS, 'data'),
        prevent_initial_call=True
    )
    def _tenure(tenure, memory):
        if tenure is None:
            raise PreventUpdate
        else:
            memory['tenure'] = tenure
        return memory

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
                    value=kwargs_schema['grace_period'],
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

    @callback(
        Output(LOAN.RESULT.KWARGS, 'data',
               allow_duplicate=True),  # type: ignore
        Input(suffix_for_type(LOAN.GRACE, type), 'value'),
        State(LOAN.RESULT.KWARGS, 'data'),
        prevent_initial_call=True
    )
    def _grace(grace_period, memory):
        if grace_period is None:
            raise PreventUpdate
        else:
            memory['grace_period'] = grace_period
        return memory

    # Payment Methods
    dropdown_refresh = html.Div(
        [
            refreshable_dropdown(
                label='Payment methods',
                type=LOAN.TYPE,
                options=amortization_types
            )
        ]
    )

    @callback(
        Output(LOAN.RESULT.KWARGS, 'data',
               allow_duplicate=True),  # type: ignore
        Input(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, type), 'value'),
        State(LOAN.RESULT.KWARGS, 'data'),
        prevent_initial_call=True
    )
    def _payment_methods(repayment_methods, memory):
        if repayment_methods is None:
            raise PreventUpdate
        else:
            memory['method'] = repayment_methods
        return memory

    @classmethod
    def interest_rate(
        cls,
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
                                    type='number',
                                    step=0.01,
                                    value=(kwargs_schema['interest_arr']['interest'][0] if type ==
                                           LOAN.TYPE else kwargs_schema['subsidy_arr']['interest'][0]),
                                    min=0,
                                    max=100
                                ),
                                dbc.InputGroupText('%')
                            ],
                            style={
                                # ''
                                # 'width': "20%",
                            },
                            className='mb-2'
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
                                type=type,  # type: ignore
                                dropdown_label='Time',
                                # avoid the errors regarding the nonexistent objects.
                                pattern_matching=True,
                                placeholder=placeholder,
                            )
                        ],
                        style={
                            'display': 'none',
                            "maxWidth": "100%"
                        },
                        id=suffix_for_type('toggle to show the options', type)
                    ),
                    ],
                )
            ],
            className='mb-3'
        )

        @callback(
            Output(suffix_for_type('toggle to show the options', type), 'style'),
            Output(suffix_for_type('momory for the tenure', LOAN.TYPE),
                   'data', allow_duplicate=True),  # type: ignore
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            State(LOAN.TENURE, 'value'),
            State(suffix_for_type('momory for the tenure', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def toggle_options(
            value,
            tenure,
            memory
        ):
            if value[-1] == 1:
                memory.append(tenure)
                return {'display': 'block'}, memory
            else:
                return {'display': 'none'}, memory

        @callback(
            Output(suffix_for_type('momory for the tenure', LOAN.TYPE),
                   'data', allow_duplicate=True),  # type: ignore
            Input(LOAN.TENURE, 'value'),
            State(suffix_for_type('momory for the tenure', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def update_momery_of_tenure(tenure, memory):
            memory.append(tenure)
            return memory

        @callback(
            Output(LOAN.RESULT.KWARGS, 'data',
                   allow_duplicate=True),  # type: ignore
            Input(suffix_for_type(LOAN.INTEREST, type), 'value'),
            Input(suffix_for_type(ADDON.MEMORY, type), 'data'),
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            State(LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _interest_rate(interest, arr, multi_stage_interest, memory):
            if interest is None:
                raise PreventUpdate
            elif type == LOAN.TYPE:
                memory['interest_arr'] = {
                    'interest': [[interest, *arr.values()] if multi_stage_interest[-1] == 1 else [interest]][-1],
                    'time': [[int(v) for v in arr.keys()] if multi_stage_interest[-1] == 1 else []][-1]
                }
            elif type == LOAN.SUBSIDY.TYPE:
                memory['subsidy_arr'] = {
                    'interest': [[interest, *arr.values()] if multi_stage_interest[-1] == 1 else [interest]][-1],
                    'time': [[int(v) for v in arr.keys()] if multi_stage_interest[-1] == 1 else []][-1]
                }
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
                            id='accordion-{}'.format(title),
                            item_id=title,
                            style={
                                'width': '100%',
                                'align-items': 'right',
                                'justify-content': 'right',
                                'margin': '0px',
                                'padding': '0px',
                                'border': '0px',
                                'border-radius': '0px',
                                'background-color': 'transparent',
                            }
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

        @callback(
            Output({'index': ALL, 'type': suffix_for_type(
                ADDON.DROPDOWN.LIST, type)}, 'data'),
            Input(LOAN.TENURE, 'value'),
        )
        def update_prepay_arrangement(tenure):
            return [[1, tenure - 1]]

        # Toggle the addon setting for prepay
        @callback(
            Output(suffix_for_type(ADDON.INPUT, type), 'type'),
            Output(suffix_for_type(ADDON.INPUT, type), 'step'),
            Output(suffix_for_type(ADDON.INPUT, type), 'max'),
            [Input('accordion', 'active_item')],
            State(suffix_for_type(LOAN.AMOUNT, LOAN.TYPE), 'value'),
            State(suffix_for_type(LOAN.AMOUNT, LOAN.SUBSIDY.TYPE), 'value'),
            prevent_initial_call=True,
        )
        def toggle_prepay_arrangement(_, amount, subsidy_amount):
            if _ and _[0] == LOAN.PREPAY.TYPE:
                return 'number', 1, (amount if amount else 0)
            else:
                return 'float', 0.01, 100

        @callback(
            Output(LOAN.RESULT.KWARGS, 'data',
                   allow_duplicate=True),  # type: ignore
            Input(suffix_for_type(ADDON.MEMORY, type), 'data'),
            State(LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True,
        )
        def update_result_for_prepay(arr, memory):
            memory['prepay_arr'] = {
                'amount': [*arr.values()],
                'time': [int(v) for v in arr.keys()]
            }

            return memory

        return layout

    # subsidy
    @ classmethod
    def subsidy(cls, type=LOAN.SUBSIDY.TYPE):
        layout = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Div(
                                    dbc.Button("Reset", id='Reset',
                                               color="primary", className="me-1")
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Subsidy Start timepoint'),
                                        dbc.Input(
                                            id=LOAN.SUBSIDY.START,
                                            type='number',
                                            step=1,
                                            value=kwargs_schema['subsidy_arr']['start'],
                                            min=0,
                                            max=24,
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Subsidy Amount'),  # 優惠貸款金額
                                        dbc.Input(
                                            id=suffix_for_type(
                                                LOAN.AMOUNT, type),
                                            type='number',
                                            step=1,
                                            value=kwargs_schema['subsidy_arr']['amount'],
                                            min=0,
                                        ),
                                    ]
                                ),
                                MortgageOptions.interest_rate(
                                    type=type,
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Subsidy tenure'),
                                        dbc.Input(
                                            id=LOAN.SUBSIDY.TENURE,
                                            type='number',
                                            step=1,
                                            value=kwargs_schema['subsidy_arr']['tenure'],
                                            min=0,
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Subsidy Grace Period'),
                                        dbc.Input(
                                            id=suffix_for_type(
                                                LOAN.GRACE, type),
                                            type='number',
                                            step=1,
                                            value=kwargs_schema['subsidy_arr']['grace_period'],
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
                                                type=LOAN.SUBSIDY.PREPAY.TYPE,
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
                    style={'width': '100%'},
                ),
            ]
        )

        @callback(
            Output({'index': ALL, 'type': suffix_for_type(
                ADDON.DROPDOWN.LIST, LOAN.TYPE)}, 'data'),
            Input(suffix_for_type('momory for the tenure', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def update_arrangement(memory):
            if len(memory) == 0:
                return PreventUpdate()
            else:
                return [[1, memory[-1] - 1]]

        @callback(
            Output({'index': ALL, 'type': suffix_for_type(
                ADDON.DROPDOWN.LIST, LOAN.SUBSIDY.TYPE)}, 'data'),
            Input(suffix_for_type('momory for the tenure', LOAN.TYPE), 'data'),
            Input(LOAN.SUBSIDY.START, 'value'),
            prevent_initial_call=True,
        )
        def update_subsidy_arrangement(
            memory,
            start
        ):
            if len(memory) == 0 or not start:
                return no_update
            else:
                return [[start, memory[-1] - 1]]

        @callback(
            Output(suffix_for_type(ADDON.DROPDOWN.LIST,
                   LOAN.SUBSIDY.PREPAY.TYPE), 'data'),  # type: ignore
            Input(LOAN.SUBSIDY.TENURE, 'value'),
            Input(LOAN.SUBSIDY.START, 'value'),
        )
        def update_subsidy_prepay_arrangement(
            period,
            start,
        ):
            if period and start:
                return [[start, period + start - 1]]
            else:
                return no_update

        @callback(
            [
                Output(suffix_for_type(ADDON.INPUT, LOAN.SUBSIDY.PREPAY.TYPE),
                       'disabled', allow_duplicate=True),  # type: ignore
                Output(suffix_for_type(ADDON.DROPDOWN.MENU, LOAN.SUBSIDY.PREPAY.TYPE),
                       'disabled', allow_duplicate=True),  # type: ignore
                Output(suffix_for_type(ADDON.ADD, LOAN.SUBSIDY.PREPAY.TYPE),
                       'disabled', allow_duplicate=True),  # type: ignore
                Output(suffix_for_type(ADDON.DELETE, LOAN.SUBSIDY.PREPAY.TYPE),
                       'disabled', allow_duplicate=True),  # type: ignore
                Output(suffix_for_type(ADDON.INPUT,
                       LOAN.SUBSIDY.PREPAY.TYPE), 'type'),
                Output(suffix_for_type(ADDON.INPUT,
                       LOAN.SUBSIDY.PREPAY.TYPE), 'step'),
                Output(suffix_for_type(ADDON.INPUT,
                       LOAN.SUBSIDY.PREPAY.TYPE), 'max'),
            ],
            Input(LOAN.SUBSIDY.PREPAY.OPTION, 'value'),
            Input(suffix_for_type(LOAN.AMOUNT, type), 'value'),
            prevent_initial_call=True
        )
        def control_disabled(value, subsidy_amount):
            if value[-1] == 1:
                return [False] * 4 + ['number', 1, (subsidy_amount if subsidy_amount else 0)]
            else:
                return [True] * 4 + ['number', 0, 0]

        @callback(
            Output(LOAN.RESULT.KWARGS, 'data',
                   allow_duplicate=True),  # type: ignore
            Input(suffix_for_type(LOAN.AMOUNT, type), 'value'),
            Input(suffix_for_type(LOAN.GRACE, type), 'value'),
            Input(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, type), 'value'),
            Input(suffix_for_type(ADDON.MEMORY, LOAN.SUBSIDY.PREPAY.TYPE), 'data'),
            Input(LOAN.SUBSIDY.START, 'value'),
            Input(LOAN.SUBSIDY.TENURE, 'value'),
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            Input(suffix_for_type(LOAN.INTEREST, type), 'value'),
            Input(suffix_for_type(ADDON.MEMORY, type), 'data'),
            State(LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True,
        )
        def update_result_for_subsidy(
            loan_amount,
            grace_period,
            repayment_options,
            prepay_arr,
            start,
            tenure,
            multi_stage_interest,
            interest,
            arr,
            memory
        ):
            # It is needed that all the sufficient parameters are given.
            if start and loan_amount and tenure and (multi_stage_interest if multi_stage_interest else interest):
                if (start > 0 and start <= 24) and loan_amount > 0:
                    memory['subsidy_arr'] = {
                        'amount': loan_amount,
                        'grace_period': grace_period,
                        'method': repayment_options,
                        'time': [[int(v) for v in arr.keys()] if multi_stage_interest[-1] == 1 else []][-1],
                        'interest': [[interest, *arr.values()] if multi_stage_interest[-1] == 1 else [interest]][-1],
                        'prepay_arr': {
                            'time': [int(v) for v in prepay_arr.keys()],
                            'amount': [*prepay_arr.values()],
                        },
                        'tenure': tenure,
                        'start': start
                    }
                    return memory
            else:
                raise PreventUpdate()

        @callback(
            Output(LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),
            [
                Output(suffix_for_type(LOAN.AMOUNT, type),
                       'value', allow_duplicate=True),
                Output(LOAN.SUBSIDY.START, 'value', allow_duplicate=True),
                Output(LOAN.SUBSIDY.TENURE, 'value', allow_duplicate=True),
                Output(suffix_for_type(LOAN.GRACE, type), 'value'),
                Output(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS,
                                       type), 'value', allow_duplicate=True),
                Output(suffix_for_type(LOAN.INTEREST, type),
                       'value', allow_duplicate=True),
                Output(suffix_for_type(ADDON.MEMORY, type),
                       'data', allow_duplicate=True),
                Output({'index': type, 'type': suffix_for_type(
                        ADDON.DROPDOWN.LIST, type)}, 'data', allow_duplicate=True),
                Output(suffix_for_type(
                    ADDON.MEMORY, LOAN.SUBSIDY.PREPAY.TYPE), 'data', allow_duplicate=True),
                Output(suffix_for_type(
                    ADDON.DROPDOWN.LIST, LOAN.SUBSIDY.PREPAY.TYPE), 'data', allow_duplicate=True),
            ],
            Input('Reset', 'n_clicks'),
            Input(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, type), 'value'),
            State(LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def reset_all(_, repayment_options, memory):
            if callback_context.triggered_id == "Reset":
                memory['subsidy_arr'] = {
                    'amount': 0,
                    'time': 0,
                    'tenure': 0,
                    'grace_period': 0,
                    'method': repayment_options,
                    'time': [],
                    'interest': [0],
                    'prepay_arr': {
                        'time': [],
                        'amount': [],
                    },
                }
                return [memory] + [0, 0, 0, 0, repayment_options, 0, {}, [0], {}, [[0]]]
            else:
                return no_update

        @callback(
            Output(LOAN.RESULT.DATAFRAME, 'data'),
            Input(LOAN.RESULT.KWARGS, 'data'),
        )
        def update_data_frame(kwargs):
            return calculator(**kwargs).to_dict(orient='tight')

        return layout


# layout
def layout():
    layout = html.Div(
        [
            dcc.Store(
                LOAN.RESULT.KWARGS,
                data=kwargs_schema
            ),
            dcc.Store(
                LOAN.RESULT.DATAFRAME,
                data={}
            ),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            MortgageOptions.amount,
                            MortgageOptions.interest_rate(
                                type=LOAN.TYPE,
                            ),
                            MortgageOptions.down_payment,
                            MortgageOptions.tenure(),
                            MortgageOptions.grace,
                            MortgageOptions.dropdown_refresh,

                            dbc.Col(
                                [
                                    AdvancedOptions.accordion(
                                        style={
                                            'width': '100%',
                                                     # 'display': 'inline-block',
                                                     'active-bg': 'red',
                                        },
                                        content=[
                                            {
                                                'id': title,
                                                'title': title,
                                                'children': children
                                            } for title, children in zip(
                                                [LOAN.PREPAY.TYPE,
                                                 LOAN.SUBSIDY.TYPE],
                                                [AdvancedOptions.prepayment(
                                                ),   AdvancedOptions.subsidy()]
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
    return layout


# py -m Dashboard.components.DataTable.controls
if __name__ == "__main__":
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
