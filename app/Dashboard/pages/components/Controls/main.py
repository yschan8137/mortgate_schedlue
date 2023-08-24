
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from dataclasses import dataclass, replace

from app.Dashboard.pages.components.ids import *
from app.Dashboard.pages.components.Controls.options import kwargs_schema, MortgageOptions, AdvancedOptions
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
                data=kwargs_schema,
            ),
            dcc.Store(
                LOAN.RESULT.DATAFRAME,
                data={}
            )
        ]
    )
    @callback(
        Output(LOAN.RESULT.DATAFRAME, 'data', allow_duplicate= True),
        Input(LOAN.RESULT.KWARGS, 'data'),
        prevent_initial_call= True
    )
    def update_data_frame(kwargs):
        return calculator(**kwargs).to_dict(orient='tight')
    
    return layout

@dataclass
class panel:
    """
    The layout of the panels    
    """
    @classmethod
    def front(cls, href= None, index= 'Homepage'):
        _MortgageOptions= MortgageOptions
        _MortgageOptions.index = index
        layout= html.Div(
                    [
                        register(),
                        dbc.Row(
                            [_MortgageOptions.amount],
                            align= 'center',
                            style= {
                                # 'width': '50%',
                            }
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        _MortgageOptions.tenure()
                                    ],
                                    style= {
                                        "width": "80%"
                                    }
                                ),
                                dbc.Col(
                                        [
                                        _MortgageOptions.interest_rate(type=LOAN.TYPE),
                                    ]
                                ),
                            ],
                            align= 'start',
                            className='pad-row'

                        ),
                        dbc.Row(
                            [
                                dbc.Col(_MortgageOptions.down_payment),
                                dbc.Col(_MortgageOptions.grace),
                            ],
                        ),
                        html.Div(dbc.Button(
                            "Enter",
                            id= CONTROLS.BUTTON,
                            style={
                                'margin-top': '20px',
                                # 'margin-bottom': '20px',
                                'position': 'relative',
                            },
                            active= True,
                            href= href,              
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
                    # className='pad-row',
                )

        return layout

    @classmethod
    def side(cls, index= 'Data page'):
        _MortgageOptions= MortgageOptions
        _MortgageOptions.index= index
        _AdvancedOptions= AdvancedOptions
        _AdvancedOptions.index= index
        layout = html.Div(
            [
                register(),
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                _MortgageOptions.amount,
                                _MortgageOptions.interest_rate(
                                    type=LOAN.TYPE,
                                ),
                                _MortgageOptions.down_payment,
                                _MortgageOptions.tenure(),
                                _MortgageOptions.grace,
                                _MortgageOptions.repayment_methods,
                                dbc.Col(
                                    [
                                        _AdvancedOptions.accordion(
                                            style={
                                                'width': '105%',
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
                                                    [_AdvancedOptions.prepayment(
                                                    ), _AdvancedOptions.subsidy()]
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
        return layout

# py -m app.Dashboard.pages.components.Controls.main
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )
    app.layout = panel.front()
    app.run_server(debug=True)