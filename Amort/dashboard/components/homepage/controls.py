# This file is the collection of control components for the homepage.

from dataclasses import dataclass
from gc import disable
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from numpy import place

from .. import amortization_types
from .widgets import refreshable_dropdown, addon
from ..ids import *
from ..toolkit import suffix_for_type

# Mortgage Amount


@dataclass
class MortgageOptions:
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
    term = html.Div(
        [
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
                    id=LOAN.TERM,
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
                type='loan',
                options=amortization_types
            )
        ]
    )

    @classmethod
    def interest_rate(
        cls,
        type: str = None,  # type: ignore
        label: str = 'Multistage Interest Rate',
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
                    [],
                    id=suffix_for_type(ADVANCED.TOGGLE.ITEMS, type),
                )
            ],
            className='mb-3'
        )

        @callback(
            Output(suffix_for_type(ADVANCED.TOGGLE.ITEMS, type), 'children'),
            Input(suffix_for_type(ADVANCED.TOGGLE.BUTTON, type), 'value'),
            State((LOAN.SUBSIDY.TERM if type == 'subsidy' else LOAN.TERM), 'value'),
        )
        def update_multistage_interest(value, period):
            if not period:
                raise ValueError('''
                    Errors caused by absence the id of the term of the ordinary or subsidy loan.
                    Please check the functions of 'MortgageOptions.term' and/or 'AdvancedOptions.subsidy()' are in the contorol options.
                '''
                                 )
            if value[-1] == 1:
                return addon(
                    type=type,  # type: ignore
                    dropdown_list=[c for c in range(1, period)],
                    dropdown_label='Multistage Interest Rate',
                    placeholder='Input the interest rate',
                )
            else:
                return html.Div(
                    [
                        dbc.Label('Applied Interest'),
                        dbc.Input(
                            id=suffix_for_type(LOAN.INTEREST, type),
                            type='number',
                            step=1,
                            value=0,
                            min=0,
                        ),
                    ]
                )

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
            - away_open(bool): whether the accordion is always open
        """
        titles = [c.get('title', None) for c in kwargs.get('content', [])]
        childrens = [c.get('children', None)
                     for c in kwargs.get('content', [])]
        style = kwargs.get('style', None)
        away_open = kwargs.get('away_open', False)

        layout = html.Div(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            children=children,
                            title=title
                        ) for title, children in zip(titles, childrens)
                    ],
                    id="accordion",
                    always_open=away_open,
                    start_collapsed=True,
                    flush=True,
                ),
            ],
            style=style,
        )

        return layout

    # prepayment

    @ classmethod
    def prepayment(cls, type='prepay'):
        layout = dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Label(
                                    'Prepay Arrangement',
                                    size='md',
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                addon(
                                    type=type,
                                    dropdown_list=[],
                                    dropdown_label='Select Prepay Arrangement',
                                    placeholder='Input Prepay Arrangement',
                                )
                            ],
                            id=LOAN.PREPAY.ARR,
                        )
                    ]
                ),
            ],
            className="mb-3 w-100",
        )

        @ callback(
            Output(suffix_for_type(ADDON.DROPDOWN.LIST, type), 'data'),
            Input(LOAN.TERM, 'value'),
        )
        def update_prepay_arrangement(period):
            return [v for v in range(1, period + 1)]
        return layout

    # subsidy

    @ classmethod
    def subsidy(cls, type='subsidy'):
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
                            type=type,
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
                                    id=LOAN.SUBSIDY.TERM,
                                    type='number',
                                    step=1,
                                    value=1,
                                    min=1,
                                )
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Label('Subsidy Grace Period'),
                                dbc.Input(
                                    id=LOAN.SUBSIDY.GRACE,
                                    type='number',
                                    step=1,
                                    value=0,
                                    min=0,
                                )
                            ]
                        ),
                        refreshable_dropdown(
                            label='Subsidy Payment methods',
                            type='subsidt',
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
                                        type=type,
                                        dropdown_list=[],  # type: ignore
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

        @ callback(
            Output(suffix_for_type(ADDON.DROPDOWN.LIST, type), 'data'),
            Input(LOAN.SUBSIDY.TERM, 'value'),
            Input(LOAN.SUBSIDY.START, 'value'),
        )
        def update_subsidy_arrangement(period, start):
            return [v for v in range(start, period + start + 1)]
        # NOTE: 目前顯示標準為整個借貸週期，須評估實際計算是否須另外減start

        @callback(
            Output(suffix_for_type(ADDON.INPUT, type),
                   'disabled', allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.DROPDOWN.MENU, type),
                   'disabled', allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.ADD, type), 'disabled',
                   allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.DELETE, type), 'disabled',
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
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    MortgageOptions.amount,
                                    MortgageOptions.interest_rate(),
                                    MortgageOptions.down_payment,
                                    MortgageOptions.term,
                                    MortgageOptions.grace,
                                    MortgageOptions.dropdown_refresh,
                                ]
                            ),
                            # 加入refreshabel_dropdown
                            html.Div(
                                [
                                    AdvancedOptions.accordion(
                                        content=[
                                            {
                                                'title': title,
                                                'children': children
                                            } for title, children in zip(['Prepayment',     'Subsidy'], [AdvancedOptions.prepayment(),   AdvancedOptions.subsidy()])
                                        ]
                                    )
                                    # AdvanceOptions.collapser(
                                    # id='prepayment', label='Prepayment',  children=AdvanceOptions.prepayment(), style= {'display': 'inline'}),
                                    # AdvanceOptions.collapser(
                                    # id='subsidy', label='Subsidy',    children=AdvanceOptions.subsidy(), style=  {'display': 'inline'}),
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
