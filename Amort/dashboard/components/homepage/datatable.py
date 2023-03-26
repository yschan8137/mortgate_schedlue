
from dash import Dash, dcc, html, Input, Output, State, callback, register_page, page_registry, dash_table
import dash_bootstrap_components as dbc

from ..ids import *
from Amort.loan import calculator
from ..toolkit import convert_df_to_dash
from .controls import panel


class config:
    PAGE_SIZE = 50


# 設定data table的列數
rows_per_page = dbc.Row(
    [
        dbc.Label('Rows per pages'),
        dbc.Input(
            type='number',
            id=PAGE_SIZE,
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
    id=DATA_TABLE,
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
        Output(DATA_TABLE, 'data'),
        Output(DATA_TABLE, 'columns'),
        Output(DATA_TABLE, 'page_count'),
    ],
    [
        # Input(LOAN.PAYMENT_OPTIONS, 'value'),
        Input(LOAN.TOTAL_AMOUNT, 'value'),
        Input(LOAN.DOWN_PAYMENT_RATE, 'value'),
        Input(LOAN.PERIOD, 'value'),
        Input(LOAN.GRACE, 'value'),
        Input(LOAN.PREPAY.AMOUNT, 'value'),
        Input(LOAN.PREPAY.ARR, 'value'),
        Input(LOAN.SUBSIDY.AMOUNT, 'value'),
        Input(LOAN.SUBSIDY.INTEREST, 'value'),
        # Input(LOAN.SUBSIDY.METHOD, 'value'),
        Input(LOAN.SUBSIDY.TERM, 'value'),
        Input(LOAN.SUBSIDY.TIME, 'value'),
        Input(DATA_TABLE, 'page_current'),
        Input(PAGE_SIZE, 'value')  # 調整列數
    ]
)
def update_data_table(
    payment_options,
    loan_amount,
    down_rate,
    loan_period,
    grace_period,
    prepay_amount,
    prepay_arr,  # []
    subsidy_amount,  # []
    subsidy_interest,  # []
    subsidy_methods,  # []
    subsidy_term,
    subsidy_time,
    page_current,
    page_size_editable,
):
    if payment_options == []:
        return None, None, None
    else:
        df = calculator(
            interest_arr={'interest': [1.38]},
            total_amount=loan_amount,
            down_payment_rate=down_rate / 100,
            loan_period=loan_period,
            grace_period=grace_period,
            prepay_arr={
                'multi_arr': prepay_arr,
                'amount': [prepay_amount],  # [2_000_000, 200_0000]
            },
            subsidy_arr={
                'interest': [subsidy_interest],  # [1.01],
                'multi_arr': [],
                'time': subsidy_time,  # 24,
                'amount': subsidy_amount,  # 2_300_000,
                'term': subsidy_term,  # 20,
                'method': subsidy_methods,
            },
            method=payment_options
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
                    panel
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