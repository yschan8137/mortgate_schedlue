# This file is the collection of control components for the homepage.suffix_for_type(LOAN.TERM, type)

from dataclasses import dataclass
from gc import disable
from sre_constants import IN
from dash import Dash, html, dcc, Input, Output, State, callback, MATCH, ALL, ALLSMALLER
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from numpy import place

from .. import amortization_types
from .widgets import refreshable_dropdown, addon
from ..ids import *
from ..toolkit import suffix_for_type

# TODO:
# 1. resolve the issues of the missing id while accordion hasn't been toggled. 

@dataclass
class MortgageOptions:
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
                    id=LOAN.AMOUNT,
                    placeholder='Input the mortgage amount',
                    min=0,
                    step=1,
                    value=10_000_000,
                    style={
                        'width': "20%",
                        'textAlign': 'left'
                    },
                ),
                width=10
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
                        'width': "15%",
                    }
                ),
            )
        ]
    )

    # Mortgage Period
    @classmethod
    def term(cls, type): 
        return html.Div(
            [
                dcc.Store(suffix_for_type('momory for the term', type), data= []),
                # dcc.Store({'index': LOAN.TYPE, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.TYPE)}), # preloaded components
                # dcc.Store({'index': LOAN.SUBSIDY.TYPE, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.SUBSIDY.TYPE)}), # preloaded components
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
                        id={'index': LOAN.TYPE, 'type': suffix_for_type(LOAN.TERM, type)},
                        style={
                            'width': "10%",
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
                    id=LOAN.GRACE,
                    style={
                        'width': "10%",
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
                type= LOAN.OPTIONS,
                options=amortization_types
            )
        ]
    )
    #之前用dbc.Checklist好像無法再更新callback
    # 嘗試改成Input再加一個html.Div，記得刪掉value
    # 或dbc.Collapes
    @classmethod
    def interest_rate(
        cls,
        type: str = None,  # type: ignore
        label: str = 'Multistage Interest Rate',
        placeholder='Input the interest rate',
    ):
        layout = html.Div(
            [
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
                                    dropdown_label= label,
                                    pattern_matching= True, # avoid the errors regarding the nonexistent objects.
                                    placeholder= placeholder,
                            )
                        ],
                        style= {'display': 'none'},
                        id= suffix_for_type('toggle to show the options', type)
                    ),
                     html.Div(
                         [
                             dbc.Label('Applied Interest'),
                             dbc.Input(
                                 id=suffix_for_type(LOAN.INTEREST, type),
                                 type='number',
                                 step=1,
                                 value=0,
                                 min=0,
                             ),
                         ],
                         id= suffix_for_type('toggle to hide the options', type)
                     )
                     ],
                    # id=suffix_for_type(ADVANCED.TOGGLE.ITEMS, type),
                )
            ],
            className='mb-3'
        )
        @callback(
            Output(suffix_for_type('toggle to show the options', type), 'style'),
            Output(suffix_for_type('toggle to hide the options', type), 'style'),
            Output(suffix_for_type('momory for the term', LOAN.TYPE), 'data', allow_duplicate=True), # type: ignore
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            State({'index': ALL, 'type': suffix_for_type(LOAN.TERM, LOAN.TYPE)}, 'value'),
            State(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def toggle_options(
            value,
            term,
            memory):
            if value[-1] == 1:
                memory.append(term[0])
                return {'display': 'block'}, {'display': 'none'}, memory
            else:
                return {'display': 'none'}, {'display': 'block'}, memory
        # @callback(
            # Output(suffix_for_type(ADVANCED.TOGGLE.ITEMS, type), 'children'),
            # Output(suffix_for_type('momory for the term', LOAN.TYPE), 'data', allow_duplicate=True), # type: ignore
            # Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            # State({'index': ALL, 'type': suffix_for_type(LOAN.TERM, LOAN.TYPE)}, 'value'),
            # State(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            # prevent_initial_call=True,
        # )
        # def update_multistage_interest(
            # value, 
            # term,
            # memory
            # ):
            # if value[-1] == 1:
                # memory.append(term[0])
                # return 
            # else:
                # return 
                       

        return layout


@ dataclass
class AdvancedOptions:
    # collapser
    @ classmethod
    def collapser(cls, id, label, children, **style):
        layout = html.Div(
            [
                html.Div(
                    [
                        dbc.Button(
                            label,
                            id=f"bottun-{id}",
                            className="mb-3",
                            color="primary",
                            n_clicks=0,
                        )
                    ],
                    id=f"trigger-{id}",
                ),
                html.Div(
                    [
                        dbc.Collapse(
                            childrn=[c for c in [children]],
                            className="mb-3",
                            id=f"collapse-{id}",
                            is_open=False,
                        )
                    ],
                    id=f'toggle-for-{id}'
                ),
            ],
            style=style
        )

        @ callback(
            Output(f"collapse-{id}", "is_open"),
            Input(f"trigger-{id}", "n_clicks"),
            State(f"collapse-{id}", "is_open"),
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        return layout

    #  accordion
    @ classmethod
    def accordion(cls, **kwargs):
        """
        Arguments:
            - content(list): a list of items for the specification of title and children of the accordion as follows:
                [
                    {
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

        layout = html.Div(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            children=children,
                            title=title,
                        ) for title, children in zip(titles, childrens)
                    ],
                    id="accordion",
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
                    dropdown_label='Select Prepay Arrangement',
                    pattern_matching=True,
                    placeholder='Input Prepay Arrangement',
                )
            ]
        )

        @ callback(
            Output({'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, type)}, 'data'),
            Input({'index': ALL, 'type': suffix_for_type(LOAN.TERM, LOAN.TYPE)}, 'value'),
        )
        def update_prepay_arrangement(period):
            return [period[-1] + 1]
        return layout

    # subsidy

    @ classmethod
    def subsidy(cls, type=LOAN.SUBSIDY.TYPE):
        layout = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Label('Subsidy Amount'),  # 優惠貸款金額
                                dbc.Input(
                                    id=LOAN.SUBSIDY.AMOUNT,
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
                                    value=1,
                                    min=1,
                                    max=24,
                                )
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Label('Subsidy Term'),
                                dbc.Input(
                                    id= suffix_for_type(LOAN.TERM, type),
                                    type='number',
                                    step=1,
                                    value=20,
                                    min=1,
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
                            type=suffix_for_type(LOAN.OPTIONS, type),
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
                                        dropdown_label='Select Prepay Arrangement',
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
        )

        @callback(
            Output({'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.TYPE)}, 'data'),
            Input(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def update_arrangement(memory):
            # print('memory on controls line 416: ', memory)
            return [memory[-1] + 1]                                          

        @callback(
            Output({'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.SUBSIDY.TYPE)}, 'data'),
            Input(suffix_for_type('momory for the term', LOAN.TYPE), 'data'),
            prevent_initial_call=True,
        )
        def update_subsidy_arrangement(memory):
            # print('memory on controls line 425: ', memory)
            return [memory[-1] + 1]                                  

        @callback(
            Output(suffix_for_type(ADDON.DROPDOWN.LIST, LOAN.SUBSIDY.PREPAY.TYPE), 'data'), # type: ignore
            Input(suffix_for_type(LOAN.TERM,  type), 'value'),
            Input(LOAN.SUBSIDY.START, 'value'),
        )
        def update_subsidy_prepay_arrangement(
            period,
            start,
            ):
            return [period + start + 1]

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
        return layout


# py -m Amort.dashboard.components.homepage.controls
if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    app.layout = html.Div(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    MortgageOptions.amount,
                                    MortgageOptions.interest_rate(
                                        type= LOAN.TYPE,
                                        ),
                                    MortgageOptions.down_payment,
                                    MortgageOptions.term(type= LOAN.TYPE),
                                    MortgageOptions.grace,
                                    MortgageOptions.dropdown_refresh,
                                ]
                            ),
                            # 加入refreshabel_dropdown
                            html.Div(
                                [
                                    AdvancedOptions.accordion(
                                        style={
                                            'display': 'inline',
                                            'active-bg': 'red',

                                        },
                                        content=[
                                            {
                                                'title': title,
                                                'children': children
                                            } for title, children in zip(['Prepayment',  'Subsidy'], [AdvancedOptions.prepayment(),   AdvancedOptions.subsidy()])
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
