
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from dataclasses import dataclass

from app.Dashboard.components.ids import *
from app.Dashboard.components.Controls.options import kwargs_schema, MortgageOptions, AdvancedOptions
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
        Output(LOAN.RESULT.DATAFRAME, 'data'),
        Input(LOAN.RESULT.KWARGS, 'data'),
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
    def front(cls):
        layout= dbc.Card(
                    [
                        register(),
                        dbc.Row(
                            [MortgageOptions.amount],
                            align= 'center',
                            style= {
                                # 'width': '50%',
                            }
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        MortgageOptions.tenure()
                                    ],
                                    style= {
                                        "width": "80%"
                                    }
                                ),
                                dbc.Col(
                                        [
                                        MortgageOptions.interest_rate(type=LOAN.TYPE),
                                    ]
                                ),
                            ],
                            align= 'start',
                            className='pad-row'

                        ),
                        dbc.Row(
                            [
                                dbc.Col(MortgageOptions.down_payment),
                                dbc.Col(MortgageOptions.grace),
                            ],
                        ),
                        html.Div(dbc.Button(
                            'Enter',
                            style={
                                'margin-top': '20px',
                                # 'margin-bottom': '20px',
                                'position': 'relative',
                            },
                            active= True               
                        ))
                    ],
                    body=True,
                    style={
                        'width': '100%',
                        'height': '100%',
                        'background-color': '#f5f5f5',
                        'border': '1px solid #ccc',
                        'border-radius': '5px',
                        'box-shadow': '0 0 5px #ccc',
                        'font-size': '20px',
                        'font-weight': 'bold',
                        'color': '#333',
                        'position': 'relative',
                        'z-index': '1',
                    },
                    # className='pad-row',
                )

        return layout

    @classmethod
    def side(cls):
        layout = html.Div(
            [
                register(),
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
                                MortgageOptions.repayment_methods,

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

# py -m app.Dashboard.components.Controls.main
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.LITERA], 
           suppress_callback_exceptions=True
           )
    app.layout = panel.front()
    app.run_server(debug=True)