# This file is the collection of control components for the homepage.

from dataclasses import dataclass
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

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
                    id=LOAN.TOTAL_AMOUNT,
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
                        id=LOAN.DOWN_PAYMENT_RATE,
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
    period = html.Div(
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
                    id=LOAN.PERIOD,
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


@ dataclass
class AdvanceOptions:
    # collapser
    @ classmethod
    def collapser(cls, id, label, children):
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
                    id=f"trigger-{id}"
                ),
                html.Div(
                    [
                        dbc.Collapse(
                            children,
                            className="mb-3",
                            id=f"collapse-{id}",
                            is_open=False,
                        )
                    ],
                    id=f'toggle-to-show-{id}'
                ),
            ],
        )

        @callback(
            Output(f"collapse-{id}", "is_open"),
            Input(f"trigger-{id}", "n_clicks"),
            State(f"collapse-{id}", "is_open"),
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        return layout

    # prepayment

    @classmethod
    def prepayment(cls, type='prepay'):
        layout = dbc.Card(
            [
                # dbc.CardHeader(
                # dbc.Checklist(
                # options=[
                # {'label': 'Prepay Plan', 'value': 0},
                # ],
                # id=LOAN.PREPAY.OPTION,
                # switch=True,
                # inline=True,
                # value=[]
                # )
                # ),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Label(
                                    'Prepay Arrangement',
                                    size='md',
                                ),
                                # dbc.Input(
                                # id=LOAN.PREPAY.AMOUNT,
                                # type='number',
                                # step=1,
                                # value=[0],
                                # min=[0],
                                # disabled=True,
                                # )
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

        # @callback(
        # Output(LOAN.PREPAY.AMOUNT, 'disabled'),
        # Output(suffix_for_type(ADDON.DISABLED, type),
        #    'data'),  # refer to widgets.py
        # Input(LOAN.PREPAY.OPTION, 'value')
        # )
        # def prepay_option(value):
        # if value:
        # return False  # , False
        # else:
        # return True  # , True

        @callback(
            Output(suffix_for_type(ADDON.DROPDOWN.LIST, type), 'data'),
            Input(LOAN.PERIOD, 'value'),
        )
        def update_prepay_arrangement(period):
            return [v for v in range(1, period + 1)]
        return layout

    # subsidy

    @classmethod
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
                        html.Div(
                            [
                                dbc.Label('Applied Interest'),
                                dbc.Input(
                                    id=LOAN.SUBSIDY.INTEREST,
                                    type='number',
                                    step=1,
                                    value=0,
                                    min=0,
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Label('Subsidy Prepay Arrangement'),
                                html.Div([
                                    addon(
                                        type=type,
                                        dropdown_list=[],
                                        dropdown_label='Select Subsidy Arrangement',
                                        placeholder='Input Subsidy Arrangement',
                                    )
                                ],
                                    id=LOAN.SUBSIDY.ARR,
                                )]),
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
                                dbc.Label('Subsidy Period'),
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
                            options=amortization_types)
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

        # )
        # @callback(
        # Output(LOAN.SUBSIDY.AMOUNT, 'disabled'),
        # Output(LOAN.SUBSIDY.ARR, 'disabled'),
        # Input(LOAN.SUBSIDY.OPTION, 'value')
        # )
        # # def subsidy_option(value):
        # if value:
        # return False, False
        # else:
        # return True, True
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
                                    MortgageOptions.down_payment,
                                    MortgageOptions.grace,
                                    MortgageOptions.period,
                                    MortgageOptions.dropdown_refresh,
                                ]
                            ),
                            # 加入refreshabel_dropdown
                            html.Div(
                                [
                                    AdvanceOptions.collapser(
                                        id='prepayment', label='Prepayment', children=AdvanceOptions.prepayment()),
                                    AdvanceOptions.collapser(
                                        id='subsidy', label='Subsidy', children=AdvanceOptions.subsidy()),
                                ],
                                style={
                                    'display': 'inline-flex',
                                    'flex-direction': 'column',
                                },
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
