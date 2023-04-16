
from dash import Dash, dcc, html, Input, Output, State, callback, register_page, page_registry, dash_table
import dash_bootstrap_components as dbc

from ..ids import LOAN, DATATABLE, ADDON, ADVANCED
from Amort.loan import calculator
from ..toolkit import convert_df_to_dash
from .controls import MortgageOptions, AdvancedOptions
from ..toolkit import suffix_for_type


class config:
    PAGE_SIZE = 50


# 設定data table的列數
rows_per_page = dbc.Row(
    [
        dbc.Label('Rows per pages'),
        dbc.Input(
            type='number',
            id=DATATABLE.PAGE.SIZE,
            value=12,
            min=1,
            max=481,
            step=1,
            style={
                'textAlign': 'left'
            }
        )
    ],
    style={
        'display': 'inline-block',
        'verticalAlign': 'right',
        'marginLeft': '90%'  # 把物件推到右邊去
    },
)


# data table
datatable = dash_table.DataTable(
    id=DATATABLE.TABLE,
    columns=[],
    data=[],
    merge_duplicate_headers=True,
    editable=True,
    page_current=0,
    page_size=config.PAGE_SIZE,
    page_count=0,
    page_action='custom',
    sort_action='custom',
    # sort_mode='single',
    sort_by=[],
    style_table={
        'overflow': 'scroll',
        'margin': '1%',
    },
    style_header={'border': '1px solid black'},
    style_cell={'border': '1px solid grey'},
)


# data table
@callback(
    [
        Output(DATATABLE.TABLE, 'data'),
        Output(DATATABLE.TABLE, 'columns'),
        Output(DATATABLE.TABLE, 'page_count'),
    ],
    [
        Input(LOAN.AMOUNT, 'value'),
        # input for multistages interest.
        Input(suffix_for_type(ADDON.MEMORY, 'loan'), 'value'),
        Input(LOAN.DOWNPAYMENT, 'value'),
        Input(LOAN.PERIOD, 'value'),
        Input(LOAN.GRACE, 'value'),
        Input(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, 'loan'), 'value'),
        # input for prepayment arrangement.
        Input(suffix_for_type(ADDON.MEMORY, 'prepay'), 'value'),
        Input(LOAN.SUBSIDY.AMOUNT, 'value'),
        # Input(LOAN.SUBSIDY.INTEREST, 'value'),
        # input for interest arrangement of subsidy.
        Input(suffix_for_type(ADDON.MEMORY, 'subsidy'), 'value'),
        Input(LOAN.SUBSIDY.START, 'value'),
        Input(LOAN.SUBSIDY.TERM, 'value'),
        Input(LOAN.SUBSIDY.GRACE, 'value'),
        Input(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, 'subsidy'), 'value'),
        Input(DATATABLE.TABLE, 'page_current'),
        Input(DATATABLE.PAGE.SIZE, 'value')  # 調整列數
    ]
)
def update_datatable(
    loan_amount,
    loan_interest_arr,
    loan_down_rate,
    loan_period,
    loan_grace_period,
    loan_payment_options,
    prepay_arr,  # {'amonut': [], 'multi_arr': []}
    subsidy_amount,
    subsidy_interest_arr,  # {'interest': [], 'multi_arr': []} #思考切換單一及多段利率的方法
    subsidy_start_time,
    subsidy_term,
    subsidy_grace_period,
    subsidy_payment_options,
    page_current,
    page_size_editable,
):
    if loan_payment_options == []:
        return None, None, None
    else:
        df = calculator(
            interest_arr={'interest': [1.38]},
            total_amount=loan_amount,
            downpayment=loan_down_rate / 100,
            loan_period=loan_period,
            grace_period=loan_grace_period,
            prepay_arr={
                'multi_arr': prepay_arr['multi_arr'],
                'amount': prepay_arr['amount'],  # [2_000_000, 200_0000]
            },
            subsidy_arr={
                'interest': subsidy_interest_arr['interest'],  # [1.01],
                'multi_arr': [],
                'time': subsidy_start_time,  # 24,
                'amount': subsidy_amount,  # 2_300_000,
                'term': subsidy_term,  # 20,
                'method': subsidy_payment_options,
            },
            method=loan_payment_options
        )
        page_size_editable = (
            page_size_editable if page_size_editable > 0 else 1)
        df_dash = convert_df_to_dash(df.iloc[page_current*page_size_editable: (page_current + 1) * page_size_editable]
                                     )

        pages = round((len(df.values) - 2) / page_size_editable, 0) + 1

        return df_dash[1],  df_dash[0], pages


# py -m Amort.dashboard.components.homepage.datatable
if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
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
                                                    AdvancedOptions.accordion(
                                                        content=[
                                                            {
                                                                'title': title,
                                                                'children': children
                                                            } for title, children in zip(['Prepayment',     'Subsidy'], [AdvancedOptions.prepayment(),   AdvancedOptions.subsidy()])
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
                ),
                dbc.Col(
                    [
                        rows_per_page,
                        datatable
                    ],
                    xs=8,
                    sm=8,
                    md=8,
                    lg=10,
                    xl=10,
                )
            ],
            align='center'
        ),
        fluid=True
    )
    app.run_server(debug=True)
