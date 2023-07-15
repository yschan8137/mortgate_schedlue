# This file is for the laypot of the app.py.

import dash_bootstrap_components as dbc
from Dashboard.components.DataTable.widgets import refreshable_dropdown
from Dashboard.components.ids import LOAN
from Dashboard.components import amortization_types


def main_items():
    layout = [
        # Mortgage Amount
        dbc.Row(
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
                            'width': "100%",
                            'textAlign': 'left'
                        },
                    ),
                    width=10
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
                            type='number',
                            name='Down Payment Rate',
                            required=True,
                            id=LOAN.DOWNPAYMENT,
                            min=0,
                            step=10,
                            value=20,
                            style={
                                'textAlign': 'left'
                            }
                        ), dbc.InputGroupText('%')
                        ],
                        class_name="mb-3",
                    ),
                )
            ]
        ),

        # Payment Methods
        refreshable_dropdown(
            label='Payment methods',
            options=amortization_types,
        ),

        # Mortgage Period
        dbc.Row(
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
                        id=LOAN.TENURE,
                        style={
                            'textAlign': 'left'
                        })
                )
            ]),
        # Grace Period
        dbc.Row(
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
                            'textAlign': 'left',
                        }
                    )
                )
            ]
        )
    ]
    return layout
