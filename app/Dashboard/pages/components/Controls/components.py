# This file is the collectikwargs_schemaon of control components for the homepage
import pandas as pd
from dataclasses import dataclass
from dash import Dash, html, dcc, Input, Output, State, MATCH, ALL, no_update, callback_context, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import datetime

from app.Dashboard.pages.components import amortization_types
from app.Dashboard.pages.components.Controls.widgets import refreshable_dropdown, addon
from app.Dashboard.assets import ids, specs
from app.Dashboard.pages.components.toolkit import suffix_for_type
from app.Dashboard.pages.components.toolkit import convert_df_to_dash
from app.Loan import default_kwargs

@dataclass
class MortgageOptions():
    type: str = ids.LOAN.TYPE
    index: str = ""
    kwargs_schema = default_kwargs
    width= specs.COMPONENTS.MORTGAGEOPTIONS.WIDTH

    # Mortgage Amount
    @classmethod
    def amount(cls):
        layout= html.Div(
                    [
                        dmc.NumberInput(
                            label="Mortgage Amount",
                            id= {"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, cls.type)},
                            value= cls.kwargs_schema['total_amount'],
                            placeholder= 'Enter the loan amount',
                            min= 0,
                            step= 1,
                            style={"width": cls.width},
                            required= True,
                            type= 'number',
                            size= 'md',
                        )
                    ]
                )

        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, cls.type)}, 'value'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _amount(total_amount, memory):
            if not total_amount:
                memory['total_amount'] = 0
            else:
                memory['total_amount'] = total_amount
            return memory
        
        return layout

    # Down Payment Rate
    @classmethod
    def down_payment(cls):
        layout = html.Div(
                     [
                         dmc.NumberInput(
                            id= {"index": cls.index, "type": ids.LOAN.DOWNPAYMENT},
                            label= 'Down Payment Rate',
                            style={"width": cls.width},
                            value= cls.kwargs_schema['down_payment_rate'],
                            # rightSection=DashIconify(icon="carbon:percentage"),
                            size= 'md',
                            step= 10,
                            min= 0,
                            max= 100,
                            type= 'number',
                            required= True,
                         ),
                     ]
                 )

        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": ids.LOAN.DOWNPAYMENT}, 'value'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _down_payment(downpayment_rate, memory):
            if not downpayment_rate:
                memory['down_payment_rate'] = 0
            else:
                memory['down_payment_rate'] = downpayment_rate
            return memory
        
        return layout

    # Mortgage Period
    @classmethod
    def tenure(cls, min= 1, max= 40):
        layout= html.Div(
            [
                dmc.Text(
                    'Tenure',
                    size= specs.COMPONENTS.MORTGAGEOPTIONS.TENURE.TEXT.SIZE,
                    weight= specs.COMPONENTS.MORTGAGEOPTIONS.TENURE.TEXT.WEIGHT,
                ),
                dmc.Slider(
                    id= {"index": cls.index, "type": ids.LOAN.TENURE},
                    value= cls.kwargs_schema['tenure'],
                    min= min,
                    max= max,
                    step= 1,
                    marks=[
                        {'value': v,  'label': str(v)} for v in [min, 10, 20, 30, max]
                    ],
                    size= specs.COMPONENTS.MORTGAGEOPTIONS.TENURE.SLIDER.SIZE,
                    style= {
                        'width': cls.width,
                    },

                ),
            ],
            style= {
                'margin-top': '10px',
                'margin-bottom': '20px',
            }
        )

        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": ids.LOAN.TENURE}, 'value'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _tenure(tenure, memory):
            if tenure:
                memory['tenure'] = tenure
            else:
                raise PreventUpdate
            return memory
        return layout

    # Grace Period
    @classmethod
    def grace(cls):
        layout= html.Div(
                [
                    dmc.NumberInput(
                       id= {"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, cls.type)},
                       label= 'Grace Period',
                       description= 'Mortgage grace period',
                       style={"width": cls.width},
                       value= cls.kwargs_schema['grace_period'],
                       size= 'md',
                       step= 1,
                       min= 0,
                       max= 5,
                       type= 'number',
                    ),
                    ]
                )   
        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, cls.type)}, 'value'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _grace(grace_period, memory):
            if not grace_period:
                memory['grace_period'] = 0
            else:
                memory['grace_period'] = grace_period
            return memory
        
        return layout

    # Date picker
    @classmethod
    def start_date(cls):
        layout=  html.Div(
            [
                dmc.DatePicker(
                    id= {"index": cls.index, "type": ids.LOAN.DATE},
                    placeholder= 'Select Date',
                    label= 'Start Time',
                    description="The start time of the repayment",
                    minDate= datetime.date(1992, 1, 1),
                    clearable= True,
                    size= 'md',
                    initialLevel= 'date',
                    dropdownPosition= 'start-bottom',
                    style= {
                        'width': cls.width
                    },                            
                )
            ]
        )
        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": ids.LOAN.DATE}, 'value'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _start_date(start_date, memory):
            if not start_date:
                memory['start_date'] = None
            else:
                memory['start_date'] = start_date
            return memory
        return layout
        

    # Payment Methods
    @classmethod
    def repayment_methods(cls):
        layout = html.Div(
                     [
                         refreshable_dropdown(
                             label='Payment methods',
                             type=ids.LOAN.TYPE,
                             options= amortization_types,
                             index= cls.index,
                         )
                     ]
                 )

        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, cls.type)}, 'value'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _payment_methods(repayment_methods, memory):
            if repayment_methods== memory['method']:
                raise PreventUpdate
            else:
                memory['method'] = repayment_methods
            return memory
        
        return layout

    @classmethod
    def interest_rate(
        cls,
        type: str = None,  # type: ignore
        label: str = 'Multistage Interest Rate',
        placeholder='key in a interest rate',
    ):
        layout = html.Div(
            [
                dmc.Text(
                    'Interest Rate',
                    size= specs.COMPONENTS.MORTGAGEOPTIONS.INTEREST.TEXT.SIZE,
                    weight= specs.COMPONENTS.MORTGAGEOPTIONS.INTEREST.TEXT.WEIGHT,
                ),
                dbc.Col(
                    dmc.SegmentedControl(
                        id= {"index": cls.index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, type)},
                        value="fixed",
                        data=[
                            {"value": "fixed", "label": "Fixed"},
                            {"value": "multiple", "label": "Multistages"},
                        ],
                        color= 'purple',
                        radius= 4,
                        size= 'sm',
                        style= specs.COMPONENTS.MORTGAGEOPTIONS.INTEREST.SEGMENT.STYLE | {'width': cls.width}
                    ),
                ),
                html.Div(
                        dmc.NumberInput(
                           id= {"index": cls.index, "type": suffix_for_type(ids.LOAN.INTEREST, type)},
                        #    label= 'Interest Rate',
                           style={"width": cls.width},
                           value= (cls.kwargs_schema['interest_arr']['interest'][0] if type == ids.LOAN.TYPE else cls.kwargs_schema['subsidy_arr']['interest_arr']['interest'][0]),
                           rightSection=DashIconify(icon="carbon:percentage"),
                           size= specs.COMPONENTS.MORTGAGEOPTIONS.INTEREST.SINGLE_STAGE.SIZE,
                           step= 0.01,
                           min=0,
                           max=100,
                           precision= 2,
                           type= 'float',
                           required= True,
                        ),
                        style= specs.COMPONENTS.MORTGAGEOPTIONS.INTEREST.SINGLE_STAGE.STYLE,
                        id= {"index": cls.index, "type": suffix_for_type(ids.ADDON.TOGGLE.SINGLE, type)},
                ),
                html.Div(
                    [
                        addon(
                            type=type,
                            pattern_matching=True,
                            placeholder=placeholder,
                            index= cls.index,
                        ),
                    ],
                    style= specs.COMPONENTS.MORTGAGEOPTIONS.INTEREST.MULTI_STAGES.STYLE,

                    id={"index": cls.index, "type": suffix_for_type(ids.ADDON.TOGGLE.MULTI, type)},
                ),
            ],
        )
        # Toggles for multi-stage interest rate options
        @callback(
            Output({"index": MATCH , "type": suffix_for_type(ids.ADDON.TOGGLE.MULTI, type)}, 'style', allow_duplicate= True),  
            Output({"index": MATCH , "type": suffix_for_type(ids.ADDON.TOGGLE.SINGLE, type)}, 'style', allow_duplicate= True),   
            Input({"index": MATCH , "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, type)}, 'value'),
            prevent_initial_call=True
        )
        def toggle_options(
            interest_stages_type,
        ):
            message = ''
            if interest_stages_type == 'multiple':
                return {'display': 'flex'}, {'display': 'none'}
            else:
                return {'display': 'none'}, {'display': 'flex'}

        @callback(
            Output({'index': cls.index, 'type': suffix_for_type(ids.ADDON.DROPDOWN.LIST, type)}, 'data', allow_duplicate= True), 
            Input(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def update_arrangement(memory):
            return [[1, memory['tenure'] - 1]]

        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, type)}, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.INTEREST, type)}, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, type)}, 'data'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def _interest_rate(interest_stages_type, interest, arr, memory):
            if not interest or ([*arr.keys()][-1] == ids.ADDON.LABEL.TIME if len(arr) > 0 else False):
                raise PreventUpdate
            elif type == ids.LOAN.TYPE:
                if interest_stages_type == 'multiple':
                    memory['interest_arr']['interest']= [interest, *arr.values()]
                    memory['interest_arr']['time']= [int(v) for v in arr.keys()]
                else: 
                    memory['interest_arr']['interest']= [interest]
                    memory['interest_arr']['time']= []
            elif type == ids.LOAN.SUBSIDY.TYPE:
                if interest_stages_type == 'multiple':
                    memory['subsidy_arr']['interest_arr']['interest'] = [interest, *arr.values()]
                    memory['subsidy_arr']['interest_arr']['time'] = [int(v) for v in arr.keys()]
                else:
                    memory['subsidy_arr']['interest_arr']['interest'] = [interest]
                    memory['subsidy_arr']['interest_arr']['time'] = []
            return memory

        return layout


@ dataclass
class AdvancedOptions(MortgageOptions):
    index: str= ""
    #  accordion
    @ classmethod
    def accordion(cls, **kwargs):
        """
        Arguments:
            - content(list): a list of items for the specification of title and children of the accordion as follows:
                [
                    {
                        'id': The id of the accordion,
                        'title': The title of the accordion,
                        'children': The content children in the accordion
                        'icons(dict)': Embad icon into right section of the accordion control. 
                                      The format would be a dict as {'icon': [DashIconify icons], 'name': corresponding tile of the accordion control}  
                                      
                    },
                ...
                ]
            - style(dict): the style of the accordion
        """
        titles = [c.get('title', None) for c in kwargs.get('content', [])]
        childrens = [c.get('children', None) for c in kwargs.get('content', [])]
        style = kwargs.get('style', None)
        icon= [c.get('icons', {}).get('icon', None) for c in kwargs.get('content', [])]
        name= [c.get('icons', {}).get('name', None) for c in kwargs.get('content', [])]
        layout = html.Div(
            [
                dmc.AccordionMultiple(
                    [
                        dmc.AccordionItem(
                            children=[
                                dmc.AccordionControl(
                                    title,
                                    icon= (icon if name== title else None),
                                    style= {
                                        'font-weight': 'bold',
                                        'font-size': '18px'
                                    },
                                ),
                                dmc.AccordionPanel(children)
                            ],
                            value= title,
                            id='accordion-{}'.format(title),
                            style={
                                'align-items': 'center',
                                'justify-content': 'left',
                                'background-color': 'transparent',
                            },
                        ) for title, children, icon, name in zip(titles, childrens, icon, name)
                    ],
                    style=style,
                ),
            ],
        )

        return layout

    # prepayment
    @ classmethod
    def prepayment(cls, type=ids.LOAN.PREPAY.TYPE):
        layout = html.Div(
            [
                dbc.Label(
                    'Prepay Arrangement',
                    size=specs.COMPONENTS.ADVANCEDOPTIONS.PREPAY.LABEL.SIZE,
                ),
                addon(
                    type=type,
                    pattern_matching=True,
                    placeholder='Input Prepay Arrangement',
                    index= cls.index,
                )
            ],
            style= specs.COMPONENTS.ADVANCEDOPTIONS.PREPAY.STYLE,
        )

        @callback(
            Output({'index': cls.index, 'type': suffix_for_type(ids.ADDON.DROPDOWN.LIST, type)}, 'data'), 
            Input(ids.LOAN.RESULT.KWARGS, 'data'),
        )
        def update_prepay_arrangement(memory):
            return [[1, memory['tenure'] - 1]]

        # Toggle the addon setting for prepay
        @callback(
            Output({"index": MATCH, "type": suffix_for_type(ids.ADDON.INPUT, type)}, 'type'), 
            Output({"index": MATCH, "type": suffix_for_type(ids.ADDON.INPUT, type)}, 'step'),
            Output({"index": MATCH, "type": suffix_for_type(ids.ADDON.INPUT, type)}, 'max'),
            [
                Input({"index": MATCH, "type": suffix_for_type(ids.ADDON.INPUT, type)}, 'value'),
                State({"index": MATCH, "type": suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.TYPE)}, 'value'), # Since the amount is simply an object, not a method in MortgageOptions class. This makes it unable to update the "index" attribute. Thus the "index" is set to be empty to prevent errors regarding nooexisting callback objexts.
                State({"index": MATCH, "type": suffix_for_type(ids.LOAN.AMOUNT, ids.LOAN.SUBSIDY.TYPE)}, 'value'),
            ],
        )
        def toggle_prepay_arrangement(
            _, 
            amount, 
            subsidy_amount
            ):
            if _ and callback_context.triggered_id== {"index": cls.index, "type": suffix_for_type(ids.ADDON.INPUT, type)}:
                return 'number', 1, (amount if amount else 0)
            else:
                return 'float', 0.01, 100

        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, type)}, 'data'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True,
        )
        def update_result_for_prepay(arr, memory):
            memory['prepay_arr'] = {
                'amount': [*arr.values()],
                'time': [int(v) for v in arr.keys()]
            }
            return memory

        return layout

    # subsidy
    @ classmethod
    def subsidy(cls, type=ids.LOAN.SUBSIDY.TYPE):
        layout = html.Div(
            [
                html.Div(
                    dmc.Button(
                        "Reset", 
                        id='Reset',
                        variant= specs.COMPONENTS.ADVANCEDOPTIONS.SUBSIDY.VARIANT,
                        gradient= specs.COMPONENTS.ADVANCEDOPTIONS.SUBSIDY.GRADIENT,
                        n_clicks= 0,
                )
                ),
                html.Div(
                    [
                        dbc.Label('Start timepoint'),
                        dbc.Input(
                            id=ids.LOAN.SUBSIDY.START,
                            type='number',
                            step=1,
                            value= cls.kwargs_schema['subsidy_arr']['start'],
                            min=0,
                            max=24,
                        )
                    ],
                ),
                html.Div(
                    [
                        dbc.Label('Subsidy Amount'),  # 優惠貸款金額
                        dbc.Input(
                            id={"index": cls.index ,"type": suffix_for_type(ids.LOAN.AMOUNT, type)},
                            type='number',
                            step=1,
                            value= cls.kwargs_schema['subsidy_arr']['amount'],
                            min=0,
                        ),
                    ],
                ),
                html.Div(
                    [
                        dbc.Label('Subsidy tenure'),
                        dbc.Input(
                            id=ids.LOAN.SUBSIDY.TENURE,
                            type='number',
                            step=1,
                            value= cls.kwargs_schema['subsidy_arr']['tenure'],
                            min=0,
                        )
                    ],
                ),
                MortgageOptions.interest_rate(
                    type=type,
                ),
                html.Div(
                    [
                        dbc.Label('Subsidy Grace Period'),
                        dbc.Input(
                            id={"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, type)},
                            type='number',
                            step=1,
                            value= cls.kwargs_schema['subsidy_arr']['grace_period'],
                            min=0,
                        )
                    ],
                ),
                refreshable_dropdown(
                    label='Subsidy Payment methods',
                    type= ids.LOAN.SUBSIDY.TYPE,
                    options= amortization_types,
                    index= cls.index),
                html.Div(
                    [
                        dbc.Checklist(
                            options=[
                                {'label': 'Prepayment', 'value': 1},
                            ],
                            value=[0],
                            id=ids.LOAN.SUBSIDY.PREPAY.OPTION,
                            inline=True,
                        ),
                        html.Div(
                            children=addon(
                                # addition of extra string to avoid conflict with other addons
                                type=ids.LOAN.SUBSIDY.PREPAY.TYPE,
                                # dropdown_label='Time',
                                placeholder='Input Prepay Arrangement',
                                disabled=True,
                                index= cls.index,
                            ),
                            id=ids.LOAN.SUBSIDY.PREPAY.ARR
                        ),
                    ],
                ),
            ],
            style= specs.COMPONENTS.ADVANCEDOPTIONS.STYLE
        )

        @callback(
            Output({'index': cls.index, 'type': suffix_for_type(ids.ADDON.DROPDOWN.LIST, ids.LOAN.SUBSIDY.TYPE)}, 'data'), 
            Input(ids.LOAN.SUBSIDY.TENURE, 'value'),
            Input(ids.LOAN.SUBSIDY.START, 'value'),
        )
        def update_subsidy_arrangement(
            period,
            start
        ):
            if (period and period > 0) and (start and start > 0):
                return [[start, period + start - 1]]
            else:
                raise PreventUpdate()

        @callback(
            Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.LIST, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data', allow_duplicate= True),  # type: ignore
            Input(ids.LOAN.SUBSIDY.TENURE, 'value'),
            Input(ids.LOAN.SUBSIDY.START, 'value'),
            prevent_initial_call=True,
        )
        def update_subsidy_prepay_arrangement(
            period,
            start,
        ):
            if (period and period > 0) and (start and start > 0):
                return [[start, period + start - 1]]
            else:
                raise PreventUpdate()

        @callback(
            [
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.INPUT, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'disabled'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.MENU, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'disabled'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.ADD, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'disabled'), 
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DELETE, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'disabled'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.INPUT, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'type'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.INPUT, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'step'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.INPUT, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'max'),
            ],
            Input(ids.LOAN.SUBSIDY.PREPAY.OPTION, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, type)}, 'value'),
        )
        def control_disabled(value, subsidy_amount):
            if value[-1] == 1:
                return [False] * 4 + ['number', 1, (subsidy_amount if subsidy_amount else 0)]
            else:
                return [True] * 4 + ['number', 0, 0]
        
        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),  # type: ignore
            Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, type)}, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, type)}, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, type)}, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data'),
            Input(ids.LOAN.SUBSIDY.START, 'value'),
            Input(ids.LOAN.SUBSIDY.TENURE, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, type)}, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.LOAN.INTEREST, type)}, 'value'),
            Input({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, type)}, 'data'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True,
        )
        def update_result_for_subsidy(
            loan_amount,
            grace_period,
            repayment_options,
            prepay_arr,
            start,
            tenure,
            interest_stages_type,
            interest,
            arr,
            memory
        ):
            # It is neccessary that all the sufficient parameters are given.
            if start and loan_amount and tenure and interest and (interest > 0) and (interest_stages_type if interest_stages_type else interest > 0):
                if (start > 0 and start <= 24) and loan_amount > 0:
                    memory['subsidy_arr'] = {
                        'amount': loan_amount,
                        'grace_period': grace_period,
                        'method': repayment_options,
                        'interest_arr': {
                            'time': [[int(v) for v in arr.keys()] if interest_stages_type == 'multiple' else []][-1],
                            'interest': [[interest, *arr.values()] if interest_stages_type == 'multiple' else [interest]][-1],
                        },
                        'prepay_arr': {
                            'time': [int(v) for v in prepay_arr.keys()],
                            'amount': [*prepay_arr.values()],
                        },
                        'tenure': tenure,
                        'start': start
                    }
                    return memory
            else:
                raise PreventUpdate()

        # Reset all inputs of subsidy
        @callback(
            Output(ids.LOAN.RESULT.KWARGS, 'data', allow_duplicate=True),
            [
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, type)}, 'value', allow_duplicate=True),
                Output(ids.LOAN.SUBSIDY.START, 'value', allow_duplicate=True),
                Output(ids.LOAN.SUBSIDY.TENURE, 'value', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, type)}, 'value'),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, type)}, 'value', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.LOAN.INTEREST, type)}, 'value', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, type)}, 'data', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.MEMORY, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data', allow_duplicate=True),
                Output({'index': cls.index, 'type': suffix_for_type(ids.ADDON.DROPDOWN.LIST, type)}, 'data', allow_duplicate=True),
                Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.LIST, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data', allow_duplicate=True),
            ],
            Input('Reset', 'n_clicks'),
            Input({"index": cls.index, "type": suffix_for_type(ids.ADVANCED.DROPDOWN.OPTIONS, type)}, 'value'),
            State(ids.LOAN.RESULT.KWARGS, 'data'),
            prevent_initial_call=True
        )
        def reset_all(_, repayment_options, memory):
            if callback_context.triggered_id == "Reset":
                memory['subsidy_arr'] = {
                    'amount': 0,
                    'start': 0,
                    'tenure': 0,
                    'grace_period': 0,
                    'method': repayment_options,
                    'interest_arr': {
                        'time': [],
                        'interest': [0],
                    },
                    'prepay_arr': {
                        'time': [],
                        'amount': [],
                    },
                }
                return [memory] + [0, 0, 0, 0, repayment_options, 0, {}, {}, [], []] 
            else:
                return no_update

        return layout

# py -m app.Dashboard.pages.components.COMPONENTS.options
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )
    app.layout= html.Div(
        [
            MortgageOptions.amount(),
            MortgageOptions.tenure(),
            MortgageOptions.down_payment(),
            MortgageOptions.grace(),
            MortgageOptions.interest_rate(
                type= ids.LOAN.TYPE
            ),
            html.Hr(),
            AdvancedOptions.prepayment(),
            AdvancedOptions.subsidy(),
        ]
    )
    app.run_server(debug=True)