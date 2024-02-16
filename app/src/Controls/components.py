# This file is the collectikwargs_schemaon of control components for the homepage
from dataclasses import dataclass
from dash import Dash, html, Input, Output, MATCH, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import datetime

from app.assets.locale import lan
from app.src.Controls.widgets import refreshable_dropdown, addon
from app.src.toolkit import suffix_for_type
from app.assets import ids, specs
from Loan import default_kwargs, amortization_methods


@dataclass
class MortgageOptions:
    index: str = ""
    type: str = ids.LOAN.TYPE
    kwargs_schema = default_kwargs
    width= '100%'

    # To enble the update of all attributes of the class, including index and type.
    @classmethod
    def update(cls, **kwargs):
        for key, value in kwargs.items():
            setattr(cls, key, value)
            
    # Mortgage Amount
    @classmethod
    def amount(cls):
        layout= html.Div(
                    [
                        dmc.NumberInput(
                            label= lan['controls']['components']['mortgage_amount']['en'],
                            id= {"index": cls.index, "type": suffix_for_type(ids.LOAN.AMOUNT, cls.type)},
                            value= cls.kwargs_schema['total_amount'],
                            placeholder= 'Enter the loan amount',
                            min= 0,
                            step= 1,
                            style={
                                "width": cls.width,
                                'item-align': 'center',
                                'font-weight': 'bold',
                                },
                            styles= {
                                'label': {
                                    'font-weight': 'bold',
                                    'font-size': '16px',
                                    'margin-bottom': 5,
                                    'margin-top': 5,
                                },
                            },
                            required= True,
                            type= 'number',
                            size= 'md',
                        )
                    ]
                )
        return layout

    # Down Payment Rate
    @classmethod
    def down_payment(cls):
        layout = html.Div(
                     [
                         dmc.NumberInput(
                            id= {"index": cls.index, "type": ids.LOAN.DOWNPAYMENT},
                            label= lan['controls']['components']['down_payment_rate']['en'],
                            style={
                                "width": cls.width
                            },
                            styles= {
                                'label': {
                                    'font-weight': 'bold',
                                    'font-size': '16px',
                                    'margin-bottom': 5,
                                    'margin-top': 5,
                                },
                            },
                            value= cls.kwargs_schema['down_payment_rate'],
                            size= 'md',
                            step= 10,
                            min= 0,
                            max= 100,
                            type= 'number',
                            required= True,
                         ),
                     ]
                 )
        return layout

    # Mortgage Period
    @classmethod
    def tenure(cls, min= 1, max= 40):
        layout= html.Div(
            [
                dmc.Title(
                    lan['controls']['components']['tenure']['en'],
                    id= {"index": cls.index, "type": 'title_for_tenure'},
                    order= 4,
                    style= {
                        'font-weight': 'bold',
                        'font-size': '16px',
                        'margin-bottom': 5,
                        'margin-top': 5,
                    },
                    # className= 'mb-2, mt-2',
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
        return layout

    # Grace Period
    @classmethod
    def grace(cls):
        layout= html.Div(
                [
                    dmc.NumberInput(
                       id= {"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, cls.type)},
                       label= lan['controls']['components']['grace_period']['en'],
                       style={"width": cls.width},
                       styles= {
                            'label': {
                                'font-weight': 'bold',
                                'font-size': '16px',
                            },
                       },
                       value= cls.kwargs_schema['grace_period'],
                       size= 'md',
                       step= 1,
                       min= 0,
                       max= 5,
                       type= 'number',
                    ),
                    ]
                )
        return layout

    # Date picker
    @classmethod
    def start_date(cls):
        layout=  html.Div(
            [
                dmc.DatePicker(
                    id= {"index": cls.index, "type": ids.LOAN.DATE},
                    placeholder= lan['controls']['components']['select_date']['en'],
                    label= lan['controls']['components']['start_date']['en'],
                    description= lan['controls']['components']['the_start_time_of_the_repayment']['en'],
                    minDate= datetime.date(1992, 3, 7),
                    clearable= True,
                    size= 'md',
                    initialLevel= 'date',
                    dropdownPosition= 'start-bottom',
                    style= {
                        'width': cls.width
                    },
                    styles= {
                        'label': {
                            'font-weight': 'bold',
                            'font-size': '16px',
                        },
                    },                            
                )
            ]
        )
        return layout
        

    # Payment Methods
    @classmethod
    def repayment_methods(cls):
        layout = html.Div(
                     [
                         refreshable_dropdown(
                             label= lan['controls']['components']['payment_methods']['en'],
                             type= ids.LOAN.TYPE,
                             options= amortization_methods,
                             index= cls.index,
                             value= cls.kwargs_schema['method'],
                         )
                     ],
                     style= {
                        'font-weight': 'bold',
                        'font-size': '16px',
                        'margin-top': 5,
                        'margin-bottom': 5,
                     }
                 )
        return layout

    @classmethod
    def interest_rate(
        cls,
        # index: str = "", # To address the issue of heritance of MortgageOptions class
        type: str = None,  # type: ignore
        placeholder= lan['controls']['components']['key_in_an_interest_rate']['en'],
    ):
        layout = html.Div(
            [
                dmc.Title(
                    id= {"index": cls.index, "type": suffix_for_type('title_for_interest_rate', type)},
                    children= lan['controls']['components']['interest_rate']['en'],
                    order= 4,
                    style= {
                        'font-weight': 'bold',
                        'font-size': '16px',
                        'margin-bottom': 5,
                        'margin-top': 5,
                    },
                ),
                html.Div(
                    [
                        dbc.Col(
                            dmc.SegmentedControl(
                                id= {"index": cls.index, "type": suffix_for_type(ids.ADVANCED.TOGGLE.BUTTON, type)},
                                value="fixed",
                                data=[
                                    {"value": "fixed", "label": lan['controls']['components']['segmentcontrol']['fixed']['en']},
                                    {"value": "multiple", "label": lan['controls']['components']['segmentcontrol']['multi_stages']['en']},
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
                                    index= cls.index,
                                ),
                            ],
                            style= specs.COMPONENTS.MORTGAGEOPTIONS.INTEREST.MULTI_STAGES.STYLE,

                            id={"index": cls.index, "type": suffix_for_type(ids.ADDON.TOGGLE.MULTI, type)},
                        )
                    ],
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
            Output({'index': cls.index, 'type': suffix_for_type(ids.ADDON.DROPDOWN.LIST, type)}, 'data'), 
            Input(ids.LOAN.RESULT.KWARGS, 'data'),
        )
        def update_arrangement(memory):
            if type== ids.LOAN.TYPE:
                return [[1, memory['tenure'] - 1]]
            elif type== ids.LOAN.SUBSIDY.TYPE:
                return [[memory['subsidy_arr']['start'], memory['subsidy_arr']['start'] + memory['tenure'] - 1]]
        return layout
        
@dataclass
class AdvancedOptions(MortgageOptions):
    index= ""
    #  accordion
    @classmethod
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
                                        'font-size': '16px'
                                    },
                                ),
                                dmc.AccordionPanel(children),
                            ],
                            value= title,
                            id='accordion-{}'.format(title),
                            style={
                                'align-items': 'center',
                                'justify-content': 'left',
                                'width': '100%',
                            },
                            className= 'custom-scrollbar',
                        ) for title, children, icon, name in zip(titles, childrens, icon, name)
                    ],
                    style=style,
                    value= titles
                ),
            ],
        )

        return layout

    # prepayment
    @ classmethod
    def prepayment(cls, type=ids.LOAN.PREPAY.TYPE):
        layout = html.Div(
            [
                dmc.Title(
                    lan['controls']['components']['prepay_arrangement']['en'],
                    id= {"index": cls.index, "type": 'title_for_prepay'},
                    order= 4,
                    style= {
                        'font-weight': 'bold',
                        'font-size': '16px',
                        'margin-bottom': 5,
                        'margin-top': 5,
                    },
                ),
                addon(
                    type=type,
                    index= cls.index,
                    input_type= 'number',
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
        return layout

    # subsidy
    @ classmethod
    def subsidy(cls, type=ids.LOAN.SUBSIDY.TYPE):
        layout = html.Div(
            [
                html.Div(
                    [
                        dmc.Button(
                            lan['controls']['components']['reset']['en'],
                            id='Reset',
                            variant= specs.COMPONENTS.ADVANCEDOPTIONS.SUBSIDY.VARIANT,
                            gradient= specs.COMPONENTS.ADVANCEDOPTIONS.SUBSIDY.GRADIENT,
                            n_clicks= 0,
                            style= {
                                'margin-bottom': 5,
                                'margin-top': 5,
                            },
                        )
                    ]
                ),
                html.Div(
                    [
                        dmc.Title(
                            lan['controls']['components']['start_timepoint']['en'],
                            id= {"index": cls.index, "type": suffix_for_type('label_for_start_point_of_subsidy', type)},
                            order= 4,
                            style= {
                                'font-weight': 'bold',
                                'font-size': '16px',
                                'margin-bottom': 5,
                                'margin-top': 5,
                            },
                        ),
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
                        dmc.Title(
                            lan['controls']['components']['subsidy_amount']['en'],
                            id= {"index": cls.index, "type": suffix_for_type('label_for_amount_of_subsidy', type)},
                            order= 4,
                            style= {
                                'font-weight': 'bold',
                                'font-size': '16px',
                                'margin-bottom': 5,
                                'margin-top': 5,
                            },
                        ),  # 優惠貸款金額
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
                        dmc.Title(
                            lan['controls']['components']['subsidy_tenure']['en'],
                            id= {"index": cls.index, "type": suffix_for_type('label_for_tenure_of_subsidy', type)},
                            order= 4,
                            style= {
                                'font-weight': 'bold',
                                'font-size': '16px',
                                'margin-bottom': 5,
                                'margin-top': 5,
                            },
                        ),
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
                    type= type,
                    
                ),
                html.Div(
                    [
                        dmc.Title(
                            lan['controls']['components']['subsidy_grace_period']['en'],
                            id= {"index": cls.index, "type": suffix_for_type('label_for_grace_period_of_subsidy', type)},
                            order= 4,
                            style= {
                                'font-weight': 'bold',
                                'font-size': '16px',
                                'margin-bottom': 5,
                                'margin-top': 5,
                            },
                        ),
                        dbc.Input(
                            id={"index": cls.index, "type": suffix_for_type(ids.LOAN.GRACE, type)},
                            type='number',
                            step=1,
                            value= cls.kwargs_schema['subsidy_arr']['grace_period'],
                            min=0,
                        ),
                    ],
                ),
                refreshable_dropdown(
                    label= lan['controls']['components']['subsidy_payment_methods']['en'],
                    type= ids.LOAN.SUBSIDY.TYPE,
                    value= cls.kwargs_schema['subsidy_arr']['method'],
                    options= amortization_methods,
                    index= cls.index
                ),
                html.Div(
                    [
                        dmc.Checkbox(
                            label= lan['controls']['components']['subsidy_prepayment']['en'],
                            id=ids.LOAN.SUBSIDY.PREPAY.OPTION,
                            checked= False,
                            styles= {
                                'label': {
                                    'font-weight': 'bold',
                                    'font-size': '16px',
                                },
                                'checked': {
                                    'backgroundColor': 'purple',
                                },
                            },
                            style= {
                                'margin-top': 5,
                                'margin-bottom': 5,
                            },
                        ),
                        html.Div(
                            children=addon(
                                # addition of extra string to avoid conflict with other addons
                                type=ids.LOAN.SUBSIDY.PREPAY.TYPE,
                                input_type='number',
                                disabled=True,
                                index= cls.index,
                            ),
                            id=ids.LOAN.SUBSIDY.PREPAY.ARR
                        ),
                    ],
                ),
            ],
            style= {
                'width': '100%',
                'display': 'flex',
                'flex-direction': 'column',
                'background-color': 'transparent',
                'align-items': 'left',
                'margin-top': 10,
                'margin-bottom': 10,
            },
        )

        @callback(
            Output({"index": cls.index, "type": suffix_for_type(ids.ADDON.DROPDOWN.LIST, ids.LOAN.SUBSIDY.PREPAY.TYPE)}, 'data'),
            Input(ids.LOAN.SUBSIDY.TENURE, 'value'),
            Input(ids.LOAN.SUBSIDY.START, 'value'),
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
            ],
            Input(ids.LOAN.SUBSIDY.PREPAY.OPTION, 'checked'),
            prevent_initial_call=True
        )
        def control_disabled(
            checked, 
            ):
            if checked== True:
                return [False] * 4
            else:
                return [True] * 4 
            
        return layout


# py -m app.src.Controls.components
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