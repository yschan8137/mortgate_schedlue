from dash import Dash, html, dcc, Input, Output, State, callback, Patch, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dataclasses import dataclass


from app.Dashboard.assets import ids, specs
from app.Dashboard.pages.components.Controls.components import MortgageOptions, AdvancedOptions
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
                ids.LOAN.RESULT.KWARGS,
                data= {**panel._MortgageOptions.kwargs_schema},
            ),
            dcc.Store(
                ids.LOAN.RESULT.DATAFRAME,
                data={},
            ),
        ]
    )
    # register the result for data convertions.
    @callback(
        Output(ids.LOAN.RESULT.DATAFRAME, 'data'),
        Input(ids.LOAN.RESULT.KWARGS, 'data'))
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
    def front(cls, index= ids.APP.INDEX.HOME):
        cls._MortgageOptions.index = index
        cls._AdvancedOptions.index = index
        layout= dmc.Stack(
                    [
                        cls._MortgageOptions.amount(),
                        cls._MortgageOptions.tenure(),
                        cls._MortgageOptions.interest_rate(type=ids.LOAN.TYPE),
                        cls._MortgageOptions.down_payment(),
                        cls._MortgageOptions.grace(),
                        cls._MortgageOptions.start_date(),
                        cls._MortgageOptions.repayment_methods(),
                    ],
                    mb= 5,
                    ml= 0,
                    align="center",
                    spacing= 0,
                    style= specs.PANEL.FRONT.STYLE
                )
        # cls.synchronize(index)

        return layout

    @classmethod
    def _advancedoptions(cls):
        return dmc.Stack(
            [
                cls._AdvancedOptions.accordion(
                    style= specs.COMPONENTS.ADVANCEDOPTIONS.ACCORDION.STYLE,
                    content=[
                        {
                            'id': title,
                            'title': title,
                            'children': children,
                            'icons': {
                                'icon': icon,                                           
                                'name': title,
                            },
                        } for title, children, icon in zip(
                            [
                                ids.LOAN.PREPAY.TYPE, 
                                ids.LOAN.SUBSIDY.TYPE
                            ],
                            [
                                cls._AdvancedOptions.prepayment(), 
                                cls._AdvancedOptions.subsidy()
                            ],
                            [
                                DashIconify(
                                    icon="streamline:money-cash-coins-stack-accounting-billing-payment-stack-cash-coins-currency-money-finance",
                                    color=dmc.theme.DEFAULT_COLORS["blue"][6],
                                    width=20,
                                ),
                                DashIconify(
                                    icon="tabler:user",
                                    color=dmc.theme.DEFAULT_COLORS["red"][6],
                                    width=20,
                                ),
                            ]
                        )
                    ]
                )
            ],
            mb= 5,
            ml= 0,
            mr= 20,
            align="left",
            spacing= 0,
            style= specs.PANEL.ADVANCEDOPTIONS.STYLE,
            
        )
        return layout

    # synchronize the variables among pages.
    @classmethod
    def synchronize(cls, index):
        @callback(
                [
                    Output({"index": index, "type": suffix_for_type(ids.LOAN.AMOUNT, cls._MortgageOptions.type)}, 'value'),
                    Output({"index": index, "type": ids.LOAN.DOWNPAYMENT}, 'value'),
                    Output({"index": index,"type": ids.LOAN.TENURE}, 'value'),
                    Output({"index": index, "type": suffix_for_type(ids.LOAN.GRACE, cls._MortgageOptions.type)}, 'value'),
                ],
                Input("url", 'pathname'),
                State(ids.LOAN.RESULT.KWARGS, 'data'),
        )
        def update_amount(
            url,
            kwargs,
            ):
            if not kwargs:
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
                Output({"index": index, "type": suffix_for_type(ids.LOAN.INTEREST, cls._MortgageOptions.type)}, 'value'),
                Output({"index": index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, cls._MortgageOptions.type)}, 'value'),
                Input('url', 'pathname'),
                State(ids.LOAN.RESULT.KWARGS, 'data'),
                State({"index": index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, cls._MortgageOptions.type)}, 'value'),

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
                Output({"index": index, "type": suffix_for_type(ids.ADDON.MEMORY, cls._MortgageOptions.type)}, 'data', allow_duplicate= True),
                Output({"index": index, "type": suffix_for_type(ids.ADDON.NEW, cls._MortgageOptions.type)}, 'children', allow_duplicate= True),
                Output({"index": index, "type": suffix_for_type(ids.ADDON.COLLAPSE, cls._MortgageOptions.type)}, 'is_open', allow_duplicate= True),
            ],
            Input(ids.LOAN.RESULT.DATAFRAME, 'data'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            State(ids.LOAN.RESULT.KWARGS, 'modified_timestamp'),
            State({"index": index, "type": suffix_for_type(ids.ADDON.MEMORY, cls._MortgageOptions.type)}, 'data'),
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

# py -m app.Dashboard.pages.components.COMPONENTS.panels
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )
    app.layout = html.Div(
        [
            register(),
            panel._MortgageOptions.amount(),
            panel._MortgageOptions.tenure(),
            panel._advancedoptions(),
        ],
    )
    app.run_server(debug=True)