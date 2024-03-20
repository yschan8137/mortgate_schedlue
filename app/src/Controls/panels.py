from dash import Dash, html, dcc, Input, Output, State, callback, MATCH, Patch, callback_context, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dataclasses import dataclass

from app.assets import ids, specs
from app.assets.locale import lan
from app.src.Controls.components import MortgageOptions, AdvancedOptions
from app.src.Controls.widgets import new_checklist_item
from app.src.toolkit import suffix_for_type
from Loan.main import calculator, df_schema
from app.src.DataTable import table as dataframe
from app.src.Graphic.main import graph
        
@dataclass
class panel():
    index= ids.APP.INDEX.HOME
    mortgage= MortgageOptions()
    advanced= AdvancedOptions()
    kwargs_schema= mortgage.kwargs_schema
    mortgage.update(index= index)
    advanced.update(index= index)
    
    @classmethod
    def register(cls):
        """
        Process the options inputs into a dataframe with the calculator function from the Loan module. 
        Then, convert the dataframe into dictionary form in oder to store it as a cache for further use in multiple pages.
        """
        layout= html.Div(
            [
                dcc.Store(
                    ids.LOAN.RESULT.KWARGS,
                    data= {**cls.kwargs_schema},
                ),
                dcc.Store(
                    'cache',
                    data= {}
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
            Output('cache', 'data'),
            Input(ids.LOAN.RESULT.KWARGS, 'data'),
            Input({'index': cls.index, 'type': 'locale-config'}, 'data'),
            State('cache', 'data'),
            prevent_initial_call=True
            )
        def update_data_frame(
            kwargs, 
            locale,
            cache,
            ):
            patched_memory= Patch()
            """
            轉成繁體會導致information-dashboard無法顯示，轉換回英文兩個圖都無法顯示。
            須找出kwargs及checked平行觸發的條件
            """
            ctx= callback_context.triggered_id
            kwargs_apart_from_subsudy = {k: v for (k, v) in kwargs.items() if k != 'subsidy_arr'}  
            if isinstance(ctx, dict) and ctx['type'] == 'locale-config':
                patched_memory['data'] = calculator(**kwargs, thousand_sep= False, locale= locale)
                return patched_memory, no_update
            else:
                if kwargs== cache:
                    raise PreventUpdate()
                else:                
                    condition_1 = ((subsidy_start:= kwargs['subsidy_arr']['start'] > 0) and subsidy_start <= 24)
                    condition_2 = (kwargs['subsidy_arr']['amount'] > 0)
                    condition_3 = (kwargs['subsidy_arr']['tenure'] > 0) 
                    condition_4 = (len([c for c in kwargs['subsidy_arr']['interest_arr']['interest'] if c]) > 0)
                    if (condition_1 or condition_2 or condition_3 or condition_4):
                        if (condition_1 and condition_2 and condition_3 and condition_4):
                            patched_memory['data'] = calculator(**kwargs, thousand_sep= False, locale= locale)
                            return patched_memory, no_update
                        else:
                            raise PreventUpdate()
                    else:
                        if len(cache)> 0 and (kwargs['subsidy_arr']['method'] != cache['subsidy_arr']['method']):
                                return no_update, kwargs        
                        else:
                            patched_memory['data'] = calculator(**kwargs_apart_from_subsudy, thousand_sep= False, locale= locale)
                            return patched_memory, kwargs
                
    
        @callback(
                Output(ids.LOAN.RESULT.KWARGS, 'data'),
                [
                    Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": ids.LOAN.DOWNPAYMENT}, 'value'),
                    Input({"index": cls.index, "type": ids.LOAN.TENURE}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, ids.LOAN.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": ids.LOAN.DATE}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, ids.LOAN.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.INTEREST, ids.LOAN.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.TYPE)}, 'data'),
                ],
                Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.PREPAY.TYPE)}, 'data'),
                [
                    Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.SUBSIDY.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, ids.LOAN.SUBSIDY.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, ids.LOAN.SUBSIDY.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.INTEREST, ids.LOAN.SUBSIDY.TYPE)}, 'value'),
                    Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.TYPE)}, 'data'),
                    Input(ids.LOAN.SUBSIDY.START, 'value'),
                    Input(ids.LOAN.SUBSIDY.TENURE, 'value'),
                ],
        )
        def update_kwargs(
            total_amount,
            downpayment_rate,
            tenure,
            grace_period,
            start_date,
            repayment_methods,
            interest,
            interest_arr,
            prepay_arr,
            subsidy_amount,
            subsidy_grace_period,
            subsidy_repayment_methods,
            subsidy_prepay_arr,
            subsidy_interest,
            subsidy_arr,
            subsidy_start,
            subsidy_tenure,
            ):
            patched_memory= Patch()
            if isinstance(triggered_id := callback_context.triggered_id, dict):
                if triggered_id['type'] == suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.TYPE):
                    patched_memory['total_amount'] = (total_amount if total_amount else 0)
                elif triggered_id['type'] == ids.LOAN.DOWNPAYMENT:
                    patched_memory['down_payment_rate'] = (downpayment_rate if downpayment_rate else 0)
                elif triggered_id['type'] == ids.LOAN.TENURE:
                    patched_memory['tenure'] = (tenure if tenure else 0)
                elif triggered_id['type'] == suffix_for_type(ids.LOAN.GRACE, ids.LOAN.TYPE):
                    patched_memory['grace_period'] = (grace_period if grace_period else 0)
                elif triggered_id['type'] == ids.LOAN.DATE:
                    if not start_date:
                        patched_memory['start_date'] = None
                    else:
                        patched_memory['start_date'] = start_date
                elif triggered_id['type'] == suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, ids.LOAN.TYPE):
                    patched_memory['method'] = repayment_methods
                elif triggered_id['type'] == suffix_for_type(ids.LOAN.INTEREST, ids.LOAN.TYPE) and interest:
                        patched_memory['interest_arr']['interest']= [interest]
                        patched_memory['interest_arr']['time']= []
                elif triggered_id['type'] == suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.TYPE):
                        patched_memory['interest_arr']['interest']= [interest, *interest_arr.values()]
                        patched_memory['interest_arr']['time']= [int(v) for v in interest_arr.keys()]
                elif triggered_id['type'] == suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.PREPAY.TYPE):
                    patched_memory['prepay_arr'] = {
                            'amount': [*prepay_arr.values()],
                            'time': [int(v) for v in prepay_arr.keys()]
                        }
                elif triggered_id['type'] == suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.SUBSIDY.TYPE):
                    patched_memory['subsidy_arr']['amount'] = (subsidy_amount if subsidy_amount else 0)
                elif triggered_id['type'] == suffix_for_type(ids.LOAN.GRACE, ids.LOAN.SUBSIDY.TYPE):
                    patched_memory['subsidy_arr']['grace_period'] = (subsidy_grace_period if subsidy_grace_period else 0)
                elif triggered_id['type'] == suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, ids.LOAN.SUBSIDY.TYPE):
                    patched_memory['subsidy_arr']['method'] = subsidy_repayment_methods
                elif triggered_id['type'] == suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.PREPAY.TYPE):
                    patched_memory['subsidy_arr']['prepay_arr'] = {
                            'amount': [*subsidy_prepay_arr.values()],
                            'time': [int(v) for v in subsidy_prepay_arr.keys()]
                        }
                elif triggered_id['type'] == suffix_for_type(ids.LOAN.INTEREST, ids.LOAN.SUBSIDY.TYPE) and subsidy_interest:
                        patched_memory['subsidy_arr']['interest_arr']['interest']= [subsidy_interest]
                        patched_memory['subsidy_arr']['interest_arr']['time']= []
                elif triggered_id['type'] == suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.TYPE):
                    patched_memory['subsidy_arr']['interest_arr']['interest']= [subsidy_interest, *subsidy_arr.values()]
                    patched_memory['subsidy_arr']['interest_arr']['time']= [int(v) for v in subsidy_arr.keys()]
            else:
                if callback_context.triggered_id == ids.LOAN.SUBSIDY.START:
                    patched_memory['subsidy_arr']['start'] = subsidy_start
                elif callback_context.triggered_id == ids.LOAN.SUBSIDY.TENURE:
                    patched_memory['subsidy_arr']['tenure'] = (subsidy_tenure if subsidy_tenure else 0)
                # reset the variables of the subsidy loan.
                elif triggered_id == 'Reset':
                    patched_memory['subsidy_arr'] = {
                          'amount': 0,
                          'start': 0,
                          'tenure': 0,
                          'grace_period': 0,
                          'interest_arr': {
                               'time': [],
                               'interest': [0],
                        },
                        'method': ['EQUAL_TOTAL', 'EQUAL_PRINCIPAL'],
                        'prepay_arr': {
                             'time': [],
                             'amount': [],
                        },
                    }  
            return patched_memory

# reset inputs for subsidy loan.
        @callback(
            [
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.SUBSIDY.TYPE)}, 'value', allow_duplicate=True),
                Output(ids.LOAN.SUBSIDY.START, 'value', allow_duplicate=True),
                Output(ids.LOAN.SUBSIDY.TENURE, 'value', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, ids.LOAN.SUBSIDY.TYPE)}, 'value'),
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.INTEREST, ids.LOAN.SUBSIDY.TYPE)}, 'value', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.TYPE)}, 'data', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data', allow_duplicate=True),
                Output({'index': cls.index, 'type': suffix_for_type(ids.ADDON.DROPDOWN.LIST, ids.LOAN.SUBSIDY.TYPE)}, 'data', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.LIST, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data', allow_duplicate=True),
            ],
            Input('Reset', 'n_clicks'),
            prevent_initial_call=True
        )
        def reset_all(
            _, 
            ):
            if callback_context.triggered_id == "Reset":
                return [0, 0, 0, 0, 0, {}, {}, [], []]
            else:
                raise PreventUpdate
        return layout
    
    @classmethod
    def locale_controller(cls):
        layout= html.Div(
            [
                dmc.Switch(
                    id= {'index': cls.index, 'type': "language-switch"},
                    offLabel= "EN",
                    onLabel= "繁",
                    size="lg",
                    checked= False, 
                    color= "indigo",
                    style= {
                        'margin-left': '95%',
                        'margin-top': 5,
                        'margin-bottom': 5,
                    },
                ),
                dcc.Store(
                    id= {'index': cls.index, 'type': 'locale-config'},
                    data= 'en'
                )
            ],
            style= {
            }
        )
        @callback(
                Output({'index': MATCH, 'type': 'locale-config'}, 'data'),
                Input({'index': MATCH, 'type': 'language-switch'}, 'checked'),
        )
        def update_locale_config(checked):
            if checked== 1:
                locale= 'zh_TW'
            else:
                locale= 'en'
            return locale
        
        @callback(
            [
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.TYPE)}, "label"),
                Output({"index": cls.index, "type": ids.LOAN.DOWNPAYMENT}, "label"),
                Output({"index": cls.index, "type": 'title_for_tenure'}, "children"),
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, ids.LOAN.TYPE)}, "label"),
                Output({"index": cls.index, "type": ids.LOAN.DATE}, "label"),
                Output({"index": cls.index, "type": ids.LOAN.DATE}, "description"),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, ids.LOAN.TYPE)}, "label"),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.BUTTON, ids.LOAN.TYPE)}, "children"),
                Output({"index": cls.index, "type": suffix_for_type('title_for_interest_rate', ids.LOAN.TYPE)}, "children"),
                Output({"index": cls.index, "type": 'title_for_prepay'}, "children"),
                Output('Reset', 'children'),
                Output({"index": cls.index, "type": suffix_for_type('label_for_start_point_of_subsidy', ids.LOAN.SUBSIDY.TYPE)}, "children"),
                Output({"index": cls.index, "type": suffix_for_type('label_for_amount_of_subsidy', ids.LOAN.SUBSIDY.TYPE)}, "children"),
                Output({"index": cls.index, "type": suffix_for_type('label_for_tenure_of_subsidy', ids.LOAN.SUBSIDY.TYPE)}, "children"),
                Output({"index": cls.index, "type": suffix_for_type('label_for_grace_period_of_subsidy', ids.LOAN.SUBSIDY.TYPE)}, "children"),
                Output(ids.LOAN.SUBSIDY.PREPAY.OPTION, "label"),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, ids.LOAN.SUBSIDY.TYPE)}, "label"),
                Output({"index": cls.index, "type": suffix_for_type('title_for_interest_rate', ids.LOAN.SUBSIDY.TYPE)}, "children"),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.MENU, ids.LOAN.TYPE)}, 'placeholder'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.MENU, ids.LOAN.PREPAY.TYPE)}, 'placeholder'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.MENU, ids.LOAN.SUBSIDY.TYPE)}, 'placeholder'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.MENU, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'placeholder'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, ids.LOAN.TYPE)}, 'data'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, ids.LOAN.SUBSIDY.TYPE)}, 'data'),
                Output('show-table', 'children'),
                Output('main-options', 'children'),
                Output('advanced-options', 'children'),
                Output(ids.GRAPH.ACCUMULATION, 'data'),
                Output('detailed-table', 'children'),
            ],
            Input({'index': cls.index, 'type': 'locale-config'}, 'data'),
            prevent_initial_call=True
        )
        def switch_language(locale):
            return [
                lan['controls']['components']['mortgage_amount'][locale],
                lan['controls']['components']['down_payment_rate'][locale],
                lan['controls']['components']['tenure'][locale],
                lan['controls']['components']['grace_period'][locale],
                lan['controls']['components']['select_date'][locale],
                lan['controls']['components']['the_start_time_of_the_repayment'][locale],
                lan['controls']['widgets']['repayment_methods'][locale],
                lan['controls']['widgets']['refresh'][locale],
                lan['controls']['components']['interest_rate'][locale],
                lan['controls']['components']['prepay_arrangement'][locale],
                lan['controls']['components']['reset'][locale],
                lan['controls']['components']['start_timepoint'][locale],
                lan['controls']['components']['subsidy_amount'][locale],
                lan['controls']['components']['subsidy_tenure'][locale],
                lan['controls']['components']['subsidy_grace_period'][locale],
                lan['controls']['components']['subsidy_prepayment'][locale],
                lan['controls']['widgets']['repayment_methods'][locale],
                lan['controls']['components']['interest_rate'][locale],
                lan['controls']['widgets']['time'][locale],
                lan['controls']['widgets']['time'][locale],
                lan['controls']['widgets']['time'][locale],
                lan['controls']['widgets']['time'][locale],
                [
                    {"value": "fixed", "label": lan['controls']['components']['segmentcontrol']['fixed'][locale]},
                    {"value": "multiple", "label": lan['controls']['components']['segmentcontrol']['multi_stages'][locale]},
                ],
                [
                    {"value": "fixed", "label": lan['controls']['components']['segmentcontrol']['fixed'][locale]},
                    {"value": "multiple", "label": lan['controls']['components']['segmentcontrol']['multi_stages'][locale]},
                ],
                dataframe.table(locale),
                lan['tablist']['Main'][locale],
                lan['tablist']['Subsidy'][locale],
                [
                    {"value": "regular", "label": {'en': "Regular", 'zh_TW': '一般'}[locale]},
                    {"value": "cumulative", "label": {'en': 'Cumulative', 'zh_TW': '累計'}[locale]},
                ],
                {'en': 'spreadsheet', 'zh_TW': '試算表'}[locale]
            ]
        return layout
    
    
    """
    The layout of the panels    
    """
    @classmethod
    def front(cls):
        layout= html.Div(
                    [
                        html.Div(
                            [
                                cls.mortgage.amount(),
                                cls.mortgage.tenure(),
                                cls.mortgage.interest_rate(type=ids.LOAN.TYPE),
                                cls.mortgage.down_payment(),
                                cls.mortgage.grace(),
                                cls.mortgage.start_date(),
                                cls.mortgage.repayment_methods()
                            ],
                            style= {
                                'border': '1px solid #e0e0e0',
                                'border-radius': 5,
                                'padding': 10,
                            }
                        ),
                        dmc.Space(h= 5),
                        html.Div(
                            cls.advanced.prepayment(),
                            style= {
                                'border': '1px solid #e0e0e0',
                                'border-radius': 5,
                                'padding': 10,
                            }
                        ),
                    ],
                    style= {
                        'width': '95%',
                        'height': 'auto',
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                    },
                    className= 'custom-scrollbar',
                )
        # cls.synchronize(index)
        return layout

    @classmethod
    def _advancedoptions(cls):
        layout= html.Div(
            [
                cls.advanced.accordion(
                    style= specs.COMPONENTS.ADVANCEDOPTIONS.ACCORDION.STYLE,
                    content=[
                        {
                            'title': title,
                            'children': children,
                            'icons': {
                                'icon': icon,                                           
                                'name': title,
                            },
                        } for title, children, icon in zip(
                            [
                                ids.LOAN.SUBSIDY.TYPE
                            ],
                            [
                                cls.advanced.subsidy()
                            ],
                            [
                                    DashIconify(
                                    icon="tabler:user",
                                    color=dmc.theme.DEFAULT_COLORS["red"][6],
                                ),
                            ]
                        )
                    ]
                )
            ],
            className= 'custom-scrollbar',
        )

        return layout

    # synchronize the variables among pages.
    @classmethod
    def synchronize(cls, index):
        @callback(
                [
                    Output({"index": index, "type": suffix_for_type(ids.LOAN.AMOUNT, cls.mortgage.type)}, 'value'),
                    Output({"index": index, "type": ids.LOAN.DOWNPAYMENT}, 'value'),
                    Output({"index": index,"type": ids.LOAN.TENURE}, 'value'),
                    Output({"index": index, "type": suffix_for_type(ids.LOAN.GRACE, cls.mortgage.type)}, 'value'),
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
                Output({"index": index, "type": suffix_for_type(ids.LOAN.INTEREST, cls.mortgage.type)}, 'value'),
                Output({"index": index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, cls.mortgage.type)}, 'value'),
                Input('url', 'pathname'),
                State(ids.LOAN.RESULT.KWARGS, 'data'),
                State({"index": index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, cls.mortgage.type)}, 'value'),

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
                Output({"index": index, "type": suffix_for_type(ids.ADDON.MEMORY, cls.mortgage.type)}, 'data', allow_duplicate= True),
                Output({"index": index, "type": suffix_for_type(ids.ADDON.NEW, cls.mortgage.type)}, 'children', allow_duplicate= True),
                Output({"index": index, "type": suffix_for_type(ids.ADDON.COLLAPSE, cls.mortgage.type)}, 'is_open', allow_duplicate= True),
            ],
            Input(ids.LOAN.RESULT.DATAFRAME, 'data'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            State(ids.LOAN.RESULT.KWARGS, 'modified_timestamp'),
            State({"index": index, "type": suffix_for_type(ids.ADDON.MEMORY, cls.mortgage.type)}, 'data'),
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
                patched_item= [new_checklist_item(timestamp, type= cls.mortgage.type, result= {k: v}) for (k, v) in sorted_memory.items()]
                return [sorted_memory, patched_item, True]    

# py -m app.Dashboard.pages.components.Controls.panels
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )
    app.layout = html.Div(
        [
            panel.register(),
            panel.mortgage.amount(),
            panel.mortgage.tenure(),
            panel._advancedoptions(),
        ],
    )
    app.run_server(debug=True)