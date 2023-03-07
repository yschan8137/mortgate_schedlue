from distutils.log import debug
from dash import dcc, html, Input, Output, State, callback, MATCH, ALL
import dash_bootstrap_components as dbc
from Amort.multipages.pages.toolkit import *
from Amort.multipages.pages import ids, amortization_types


def refreshable_dropdown(label, id, id_for_refreshment, disabled= False):
    dropdown = html.Div(
        [
            html.Div(
                [
                    dbc.Label(label),
                    dcc.Dropdown(
                        id= id,
                        options= to_dropdown_options([*amortization_types]),
                        value= amortization_types,
                        multi= True,
                        searchable= True,
                        placeholder= 'Choose methods for the payment',
                        disabled= disabled,
                    )
                ],
                style= {
                    "width": "50%",
                    "marginTop": "5px",
                    "marginBottom": "5px",
                }
            ),
            html.Div(
                [
                    html.Button(
                    'Refresh',
                    id= id_for_refreshment,
                    n_clicks= 0,
                    disabled= disabled,
                    )
                ],
                style= {
                    "marginTop": "8px",
                    "marginBottom": "5px",
                }
            ),
        ],
    )
    # Refresh the Dropdown of the Payment options
    @callback(
        Output(id, 'value'),
        Input(id_for_refreshment, 'n_clicks')
    )
    def refresh_options(_:int) -> list[str]:
        return amortization_types
    return dropdown

# addons function for the payment arrangement
def ARR_addons(
        type: str, # [prepay, subsidy]
        dropdown_items: list, 
        dropdown_label:str,
        input_id: str,
        input_placeholder:str
        ):

        id_of_add_button= ids.LOAN.ARR.ADD + "-" + type
        id_of_dropdown= ids.LOAN.ARR.DROPDOWN + "-" + type
        
        layout= html.Div(
            [
                dbc.InputGroup(
                    [
                        dcc.Store(id= 'memory'), #{'store_type: ["", "local", "session"]}
                        dbc.DropdownMenu(
                            [dbc.DropdownMenuItem(
                                item, 
                                id= id_of_dropdown + "-" + str(item),
                                ) for item in dropdown_items],
                            label= dropdown_label,
                            style= {
                                'width': "100%"
                            }
                        ),
                        dbc.Input(
                            id= input_id,
                            placeholder= (input_placeholder if input_placeholder!= None else ""),
                            value= [],
                        ),
                        dbc.Button(
                            'Add',
                            id= id_of_add_button,
                            n_clicks= 0,
                        ),
                    ],
                    class_name= "mb-3"
                ),
                html.Li(
                    children= [], 
                    id= 'output-ex3'
                )
            ]
        )
        # 2023/02/05 store the result 
        # https://dash.plotly.com/sharing-data-between-callbacks
        # https://dash.plotly.com/dash-core-components/store
        # 加入 dcc.Store(id='memory-output',data=[])
        
        @callback(
            Output('output-ex3', 'children'),
            Input(id_of_add_button, 'n_clicks'),
            Input(input_id, 'value'),
            State('output-ex3', 'children')
            # Input(id_of_dropdown, 'value'),
        )
        def update_arrangement_list(
            _, 
            input, 
            # dropdown,
            existing_output
            ):
            if _ == 0:
                interest= []
            else:
                interest.append(input)
            return interest
            # return existing_output.append(input)
                # time.append(dropdown)
            # return existing_output
        return layout

def main_items():
    layout = [
        # Mortgage Amount
        dbc.Row(
            [
                dbc.Label(
                    'Mortgage Amount',
                    size= 'md'
                    ),
                dbc.Col(
                    dbc.Input(
                        type= 'number',
                        name= 'Mortgage Amount',
                        required= True,
                        id= ids.LOAN.TOTAL_AMOUNT,
                        placeholder= 'Input the mortgage amount',
                        min= 0,
                        step = 1,
                        value= 10_000_000,
                        style= {
                            'width': "100%",
                            'textAlign': 'left'
                            },
                        ),
                        width= 10
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
                            type= 'number',
                            name= 'Down Payment Rate',
                            required= True,
                            id= ids.LOAN.DOWN_PAYMENT_RATE,
                            min= 0,
                            step= 10,
                            value= 20,
                            style= {
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
        refreshable_dropdown(label= 'Payment methods', id= ids.LOAN.PAYMENT_OPTIONS,id_for_refreshment= ids.LOAN.REFRESH_ALL_OPTIONS),
        
        # Mortgage Period
        dbc.Row(
            [
                dbc.Label(
                    'Mortgate Term', 
                    size= 'md'
                    ),
                dbc.Col(
                    dbc.Input(
                        min= 1,
                        max= 40,
                        value= 30,
                        step= 1,
                        type= 'number',
                        id= ids.LOAN.PERIOD,
                        style= {
                            'textAlign': 'left'
                        })
                    )
        ]),
        # Grace Period
        dbc.Row(
            [
                dbc.Label(
                    'Grace Period',
                    size= 'md'
                    ),
                dbc.Col(
                    dbc.Input(
                        min= 0,
                        max= 5,
                        step= 1,
                        value= 0,
                        type= 'number',
                        id= ids.LOAN.GRACE,
                        style= {
                            'textAlign': 'left',
                        })
                    )  
            ]
        )
    ]
    return layout 

# Advanced Options
class advanced_items:        
    @classmethod
    def prepay_plan(cls):
        layout= [
            dbc.Col(
                [
                    dbc.Label('Advanced Options', size= 'md'),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    dbc.Checklist(
                                        options= [
                                            {'label': 'Prepay Plan', 'value': 0},
                                        ],
                                        id= ids.LOAN.PREPAY.OPTION,
                                        switch= True,
                                        inline= True,
                                        value= []
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.Label('Prepay Amount'),
                                        dbc.Input(
                                            id= ids.LOAN.PREPAY.AMOUNT,
                                            type= 'number',
                                            step= 1,
                                            value= [0],
                                            min= [0],
                                            disabled= True,
                                        ),
                                        dbc.Label('Prepay Arrangement'),
                                        dbc.Input(
                                            id= ids.LOAN.PREPAY.ARR,
                                            value= [0],
                                            disabled= True,
                                        )
                                    ]
                                ),
                            ],
                            class_name="mb-3",
                        )
                    )
                ]
            )
        ]
        # Activate the prepay options
        @callback(
            [
                Output(ids.LOAN.PREPAY.ARR, 'disabled'),
                Output(ids.LOAN.PREPAY.AMOUNT, 'disabled')
            ],
            Input(ids.LOAN.PREPAY.OPTION, 'value')
        )
        def enable_prepay_options(option):
            if option == [0]:
                return [False] * 2
            else:
                return [True] * 2

    @classmethod
    def subsidy_plan(cls):
        layout= [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dbc.Checklist(
                                    options= [
                                        {'label': 'Subsidy loan', 'value': 0}
                                    ],
                                    id= ids.LOAN.SUBSIDY.OPTION,
                                    switch= True,
                                    inline= True,
                                    value= []
                                ),
                        ),
                        dbc.CardBody(
                            [
                                # dbc.Label('Subsidy Loan applied interest'),
                                # dbc.Checklist(
                                #     options= [
                                #         {'label': 'Adjustable-rate', 'value':   0}
                                #     ],
                                #     id= ids.LOAN.SUBSIDY.INTEREST_OPTION,
                                #     switch= True,
                                #     inline= True,
                                #     value= [],
                                #     class_name= "mb-3"
                                # ),
                                # dbc.Row(
                                #     [
                                #         dbc.Col(
                                #             dbc.Input(
                                #                 children= [],
                                #                 id= ids.LOAN.SUBSIDY.ARR,
                                #                 disabled= True,
                                #             ),
                                #         ),
                                #         dbc.Col(
                                #             dbc.Input(
                                #                 children= [],
                                #                 id= ids.LOAN.SUBSIDY.INTEREST,
                                #                 # value= [0],
                                #                 step= 0.01,
                                #                 disabled= True,
                                #             ),
                                #             class_name= '"w-100 bg-light border"'
                                #         ),
                                #         dbc.Col(
                                #             dbc.Button(
                                #                 'Add',
                                #                 id= ids.LOAN.SUBSIDY.ADD,
                                #                 n_clicks= 0,
                                #             ), 
                                #             class_name= "ms-5"
                                #         ),
                                #     ],
                                #     class_name= "d-flex flex-wrap    align-items-start mb-3"                                         
                                # ),
                                dbc.Label('Timepoint of Application'),
                                dbc.Input(
                                    id= ids.LOAN.SUBSIDY.TIME,
                                    value= 0,
                                    step= 1,
                                    disabled= True,
                                ),
                                dbc.Label('Amount'),
                                dbc.Input(
                                    id= ids.LOAN.SUBSIDY.AMOUNT,
                                    value= 0,
                                    step= 1,
                                    disabled= True,
                                ),
                                dbc.Label('Term'),
                                dbc.Input(
                                    id= ids.LOAN.SUBSIDY.TERM,
                                    value= 20,
                                    step= 1,
                                    disabled= True,
                                ),
                                refreshable_dropdown(label= 'Payment method',   id= ids.LOAN.SUBSIDY.METHOD,  id_for_refreshment= ids.LOAN.SUBSIDY. REFRESH_ALL_OPTIONS)
                            ]
                        ),
                    ],  
                    class_name= "mb-3",
                    outline= True,
                )
            )
        ]
        # Activate the subsidy options
        @callback(
            [
                Output(ids.LOAN.SUBSIDY.INTEREST, 'disabled'),
                Output(ids.LOAN.SUBSIDY.AMOUNT, 'disabled'),
                Output(ids.LOAN.SUBSIDY.METHOD, 'disabled'),
                Output(ids.LOAN.SUBSIDY.TERM, 'disabled'),
                Output(ids.LOAN.SUBSIDY.TIME, 'disabled'),
            ],
            Input(ids.LOAN.SUBSIDY.OPTION, 'value')
        )
        def enable_subsidy_options(option):
            if option == [0]:
                return [False] * 5
            else:
                return [True] * 5
        return layout

# py -m Amort.multipages.pages.controls
if __name__ == "__main__":
    from dash import Dash
    app = Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])
    app.layout = html.Div(
        # main_items(),
        # advanced_items.subsidy_plan(),
        ARR_addons(
            type= 'subsidy',
            dropdown_items= [1, 2 ,3],
            dropdown_label= "TimePoint",
            input_id= ids.LOAN.SUBSIDY.INTEREST,
            input_placeholder= None
            )
    )
    app.run_server(debug= True)