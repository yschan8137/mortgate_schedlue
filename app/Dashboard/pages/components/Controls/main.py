
from dash import Dash, html, dcc, Input, Output, State, callback, Patch, MATCH
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dataclasses import dataclass
# import numpy as np
import time

from app.Dashboard.pages.components.ids import *
from app.Dashboard.pages.components.Controls.options import MortgageOptions, AdvancedOptions
from app.Dashboard.pages.components.Controls.widgets import new_checklist_item
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
            ),
        ]
    )
    # register the result for data convertions.
    @callback(
        Output(LOAN.RESULT.DATAFRAME, 'data'),
        Input(LOAN.RESULT.KWARGS, 'data'))
    def update_data_frame(kwargs):
        return calculator(**kwargs, thousand_sep= False).to_dict(orient='tight')
    
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
        cls.synchronize(index)

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
        cls.synchronize(index)

        return layout

    # synchronize the variables for Homepage to data page.
    @classmethod
    def synchronize(cls, index):
        @callback(
                [
                    Output({"index": index, "type": suffix_for_type(LOAN.AMOUNT, cls._MortgageOptions.type)}, 'value'),
                    Output({"index": index, "type": LOAN.DOWNPAYMENT}, 'value'),
                    Output({"index": index,"type": LOAN.TENURE}, 'value'),
                    Output({"index": index, "type": suffix_for_type(LOAN.GRACE, cls._MortgageOptions.type)}, 'value'),
                ],
                Input("url", 'pathname'),
                State(LOAN.RESULT.KWARGS, 'data'),
                # State('cache', 'data'),
        )
        def update_amount(
            url,
            kwargs,
            ):
            if not kwargs:#cache[-1] == 1: 
                # cache equals to 1 means the switching across pages has been done in previous steps.
                # It is not necessary to synchronize the variables in the same page. It would cause excess updates.
                raise PreventUpdate
            else:
                return [kwargs['total_amount'],
                        kwargs['down_payment_rate'], 
                        kwargs['tenure'], 
                        kwargs['grace_period'],
                        ]
            
        # synchronization of single stage interest rate options.
        @callback(
                Output({"index": index, "type": suffix_for_type(LOAN.INTEREST, cls._MortgageOptions.type)}, 'value'),
                Output({"index": index, "type": suffix_for_type(ADVANCED.TOGGLE.BUTTON, cls._MortgageOptions.type)}, 'value'),
                Input('url', 'pathname'),
                State(LOAN.RESULT.KWARGS, 'data'),
                State({"index": index, "type": suffix_for_type(ADVANCED.TOGGLE.BUTTON, cls._MortgageOptions.type)}, 'value'),

        )
        def update_interest(
            url,
            kwargs, 
            toggle_value,
            ):
            if not kwargs:
                raise PreventUpdate()
            else:
                if len(kwargs['interest_arr']['interest']) > 1:
                    toggle_value.append(1)
                    return kwargs['interest_arr']['interest'][0], toggle_value
                else:
                    toggle_value.append(0)
                    return kwargs['interest_arr']['interest'][0], toggle_value

        @callback(
            [
                Output({"index": index, "type": suffix_for_type(ADDON.MEMORY, cls._MortgageOptions.type)}, 'data', allow_duplicate= True),
                Output({"index": index, "type": suffix_for_type(ADDON.NEW, cls._MortgageOptions.type)}, 'children', allow_duplicate= True),
                Output({"index": index, "type": suffix_for_type(ADDON.COLLAPSE, cls._MortgageOptions.type)}, 'is_open', allow_duplicate= True),
            ],
            Input(LOAN.RESULT.DATAFRAME, 'data'),
            State(LOAN.RESULT.KWARGS, 'data'),
            State(LOAN.RESULT.KWARGS, 'modified_timestamp'),
            State({"index": index, "type": suffix_for_type(ADDON.MEMORY, cls._MortgageOptions.type)}, 'data'),
            prevent_initial_call=True
        )
        def specifies_and_value_of_interest(
            _,
            kwargs,
            timestamp,
            _memory,
            ):
            if len(kwargs['interest_arr']['interest']) == len(_memory.values()) + 1:
                raise PreventUpdate()
            else:
                patched_item = Patch()
                sorted_memory= {}
                memory= {}
                for t, i in zip(kwargs['interest_arr']['time'], kwargs['interest_arr']['interest'][1:]):
                    memory[str(t)]= i
                for k in [str(sorted_key) for sorted_key in sorted([int(key) for key in memory.keys()])]: 
                    sorted_memory[k]= memory[k]
                patched_item= [new_checklist_item(timestamp, type= cls._MortgageOptions.type, index= index, result= {k: v}) for (k, v) in sorted_memory.items()]
                return [sorted_memory, patched_item, True]
        

# py -m app.Dashboard.pages.components.Controls.main
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )
    app.layout = panel.front()
    app.run_server(debug=True)