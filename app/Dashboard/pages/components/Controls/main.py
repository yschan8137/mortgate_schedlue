
from dash import Dash, html, dcc, Input, Output, State, callback, no_update, MATCH, page_container
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dataclasses import dataclass
import numpy as np
from pkg_resources import PathMetadata

from app.Dashboard.pages.components.ids import *
from app.Dashboard.pages.components.Controls.options import MortgageOptions, AdvancedOptions
from app.Dashboard.pages.components.toolkit import suffix_for_type
from app.Loan.main import calculator

# dash bootstrap components template: https://hellodash.pythonanywhere.com/


def register():
    """
    Process the options inputs into a dataframe with the calculator function from the Loan module. 
    Then, convert the dataframe into dictionary form in oder to store it as a cache for further use in multiple pages.
    """
    layout= html.Div(
        [
            dcc.Store(
                LOAN.RESULT.KWARGS,
                data= {**panel._MortgageOptions.kwargs_schema},
            ),
            dcc.Store(
                LOAN.RESULT.DATAFRAME,
                data={},
                # storage_type= "memory"
            ),
            dcc.Store(
                'cache', 
                data= [0],
            )
        ]
    )
    # register the result for data convertions.
    @callback(
        Output(LOAN.RESULT.DATAFRAME, 'data',
                # allow_duplicate= True
                ),
        Input(LOAN.RESULT.KWARGS, 'data'),
        # prevent_initial_call= True
    )
    def update_data_frame(kwargs):
        return calculator(**kwargs).to_dict(orient='tight')
    
    # register the page name for synchronizing the variables across pages.
    @callback(
        Output('cache', 'data'),
        Input(LOAN.RESULT.KWARGS, 'data'),
        State('cache', 'data'),
        State('url', 'pathname'),
    )
    def update_n(
        _, 
        cache,
        pathname
        ):
        if pathname == '/data':
            cache.append(1)
        else:
            cache.append(0)
        return cache
    
    return layout

@dataclass
class panel:
    """
    The layout of the panels    
    """
    _MortgageOptions= MortgageOptions
    _AdvancedOptions= AdvancedOptions
    @classmethod
    def front(cls, href= None, index= APP.INDEX.HOME):
        cls._MortgageOptions.index = index
        layout= html.Div(
                    [
                        dbc.Row(
                            [cls._MortgageOptions.amount()],
                            align= 'center',
                            style= {
                                # 'width': '50%',
                            }
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        cls._MortgageOptions.tenure()
                                    ],
                                    style= {
                                        "width": "80%"
                                    }
                                ),
                                dbc.Col(
                                        [
                                        cls._MortgageOptions.interest_rate(type=LOAN.TYPE),
                                    ]
                                ),
                            ],
                            align= 'start',
                            className='pad-row'

                        ),
                        dbc.Row(
                            [
                                dbc.Col(cls._MortgageOptions.down_payment()),
                                dbc.Col(cls._MortgageOptions.grace()),
                            ],
                        ),
                        html.Div(dbc.Button(
                            "Enter",
                            id= {"index": cls._MortgageOptions.index, "type": CONTROLS.BUTTON},
                            style={
                                'margin-top': '20px',
                                'position': 'relative',
                            },
                            active= True,
                            href= href,
                            n_clicks= 0,           
                        ))
                    ],
                    # body=True,
                    style={
                        'width': '100%',
                        'height': '100%',
                        'box-shadow': '0 0 5px #ccc',
                        'background-color': '#f5f5f5',
                        'border': '1px solid #ccc',
                        'border-radius': '5px',
                        'box-shadow': '0 0 5px #ccc',
                        'font-size': '20px',
                        'font-weight': 'bold',
                        'padding': '20px',
                        'color': '#333',
                        'position': 'relative',
                        'z-index': '1',
                    },
                )

        return layout

    @classmethod
    def side(cls, index= APP.INDEX.DATA):
        cls._MortgageOptions.index = index
        cls._AdvancedOptions.index = index
        cls.timestamp = []
        layout = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                cls._MortgageOptions.amount(),
                                cls._MortgageOptions.interest_rate(
                                    type=LOAN.TYPE,
                                ),
                                cls._MortgageOptions.down_payment(),
                                cls._MortgageOptions.tenure(),
                                cls._MortgageOptions.grace(),
                                cls._MortgageOptions.repayment_methods(),
                                dbc.Col(
                                    [
                                        cls._AdvancedOptions.accordion(
                                            style={
                                                'width': '105%',
                                                'active-bg': 'red',
                                                'justify-content': 'center',
                                                'align-items': 'center',
                                            },
                                            content=[
                                                {
                                                    'id': title,
                                                    'title': title,
                                                    'children': children
                                                } for title, children in zip(
                                                    [LOAN.PREPAY.TYPE,
                                                     LOAN.SUBSIDY.TYPE],
                                                    [
                                                        cls._AdvancedOptions.prepayment(), 
                                                        cls._AdvancedOptions.subsidy()
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                    body=True,
                    style= {
                        'width': '100%',
                        'height': '100%',
                        'background-color': '#f5f5f5',
                        'border': '1px solid #ccc',
                        'border-radius': '5px',
                    }
                )
            ]
        )
        
        @callback(
                [
                    Output({"index": index, "type": suffix_for_type(LOAN.AMOUNT, cls._MortgageOptions.type)}, 'value'),
                    Output({"index": index, "type": LOAN.DOWNPAYMENT}, 'value'),
                    Output({"index": index,"type": LOAN.TENURE}, 'value'),
                    Output({"index": index, "type": suffix_for_type(LOAN.GRACE, cls._MortgageOptions.type)}, 'value'),
                ],
                Input(LOAN.RESULT.KWARGS, 'data'),
                State('cache', 'data'),
                State('url', 'pathname'),
        )
        def update_amount(
            kwargs,
            cache,
            pathname
            ):
            if not kwargs or cache[-1] == 1: 
                # if the cache is 1, which means the switching across pages has been done in previous steps.
                # It is not necessart to synchronize the variables in the same page. Also, it would cause excess updates.
                raise PreventUpdate
            else:
                return [kwargs['total_amount'],
                        kwargs['down_payment_rate'], 
                        kwargs['tenure'], 
                        kwargs['grace_period'],
                        # cache
                        ]

        return layout
        # @callback(
            # Output({"index": cls._MortgageOptions.index, "type": suffix_for_type(LOAN.INTEREST, cls._MortgageOptions.type)}, 'value'), 
            # Output({"index": cls._MortgageOptions.index, "type": suffix_for_type(ADDON.MEMORY, cls._MortgageOptions.type)}, 'data', allow_duplicate= True), 
            # Output({"index": cls._MortgageOptions.index, "type": suffix_for_type(ADVANCED.TOGGLE.BUTTON, cls._MortgageOptions.type)}, 'value'),
            # Input(LOAN.RESULT.KWARGS, 'data'),
            # State({"index": cls._MortgageOptions.index, "type": suffix_for_type(ADDON.MEMORY, cls._MortgageOptions.type)}, 'data'),
            # prevent_initial_call=True
        # )
        # def specifies_and_value_of_interest(
            # memory, 
            # arr
            # ):
            # if len(memory['interest_arr']['interest']) == 0:
                # raise PreventUpdate
            # else:
                # if len(memory['interest_arr']['interest']) > 1:
                    # for t, i in zip(memory['interest_arr']['time'], memory['interest_arr']['interest']):
                        # arr[t]= i
                    # return memory['interest_arr']['interest'][-1], arr, [1]
                # else:
                    # print(memory['interest_arr']['interest'])
                    # return memory['interest_arr']['interest'][-1], arr, [0]

        return layout

# py -m app.Dashboard.pages.components.Controls.main
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )
    app.layout = panel.front()
    app.run_server(debug=True)