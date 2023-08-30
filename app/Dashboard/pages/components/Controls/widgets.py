# This file is for the tailor-made widgets for controls including OPTIONS dropdown, addon function for generating a dict for the combined input of payment arrangement.
from dash import Dash
from distutils.log import debug
from re import A, S
from dash import dcc, html, Input, Output, State, callback_context, MATCH, ALL, Patch, callback  # type: ignore
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app.Dashboard.pages.components.toolkit import to_dropdown_options, suffix_for_type
from app.Dashboard.pages.components.ids import *
from app.Dashboard.pages.components import amortization_types
import json


# Addons function for the payment arrangement.
# For further information, please refer to the documentation of the addon function in the file Amort\test\ADDON.py.
# code of the color: https://useaxentix.com/docs/general/colors/

def addon(
        # Type need to be indicated within ['prepay', 'subsidy'] to distinguish the different dropdowns.
        type: str,
        # dropdown_list: list,
        placeholder: str,
        dropdown_label: str= 'Time',
        pattern_matching=False,
        disabled: bool = False,
        index= ""
):
    """
    The addon function is used to generate a dict for the combined input of payment arrangement.
    The "suffix_for_type()" function is imported from the toolkit module to make format of the id match the type which specified in the argument, to distinguish the different dropdowns.

    Note that the there is no an argument for the dropdown list. It is needed to be generated by the callback function, 
    of which the id of the output is 'suffix_for_type(ADDON.DROPDOWN.LIST, type)' if the argument of the pattern_matching is off, 
    otherwise the id of the output is '{'index': type, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, type)}' if the argument of the pattern_matching is on.

    For example, the following codes show the callback function for the dropdown list while the pattern_matching is on:

    @callback(
        Output({'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, type)}, 'data'),
        Input(suffix_for_type(LOAN.TERM), 'value'),
    )
    def update_dropdown_list(term: int):
        return term

    """

    layout = html.Div(
        [
            dcc.Store(id={"index": index, "type": suffix_for_type(ADDON.DROPDOWN.LIST, type)},
                      data=0
                      ),
            dcc.Store(id={"index": index, "type": suffix_for_type(ADDON.DISABLED, type)}, data=disabled),
            # That's the outcome what we want.
            dcc.Store(id={"index": index, "type": suffix_for_type(ADDON.MEMORY, type)}, data={}),
            dcc.Store(id={"index": index, "type": suffix_for_type(ADDON.DROPDOWN.ITEMS, type)}, data={}),
            dbc.InputGroup(
                [
                    dbc.DropdownMenu(
                                [],
                                id={"index": index, "type": suffix_for_type(ADDON.DROPDOWN.MENU, type)},
                                disabled=disabled,
                                label= dropdown_label,
                                color='#4C9F85',
                                toggle_style= {
                                    'font-size': '14px',
                                }
                                # toggle_class_name= "fst-italic border border-1"
                            ),
                    dbc.Input(
                        id={"index": index, "type": suffix_for_type(ADDON.INPUT, type)},
                        type='number',
                        step=0.01,
                        value= 0,
                        min=0,
                        max=100,
                        placeholder=placeholder,
                        disabled=disabled,
                        style= {
                            'width': '28%',
                        }
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                id={"index": index, "type": suffix_for_type(ADDON.ADD, type)},
                                color="primary",
                                outline= False,
                                children=[html.I(className="bi bi-ui-checks")],
                                disabled=disabled,
                            ),
                            dbc.Button(
                                id={"index": index, "type": suffix_for_type(ADDON.DELETE, type)},
                                color="danger",
                                outline= False,
                                children=[
                                    html.I(className="bi bi-trash3"),
                                ],
                                disabled=disabled,
                            )
                        ]
                    )
                ],
                style= {
                    'display': 'flex',
                    'width': '100%',
                },
                className= 'mb-1'
            ),
            dbc.Collapse(
                id= {"index": index, "type": suffix_for_type(ADDON.COLLAPSE, type)},
                children=[
                    dbc.Card(
                        children= [dbc.CardBody(id= {"index": index, "type": suffix_for_type(ADDON.NEW, type)})],
                        style= {
                            'height': '150px',
                            'overflow': 'scroll',
                        }
                    )
                ],
                is_open=False,
                style= {
                    'width': '100%',
                }
            ),
        ],
    )


# Control the disabled status of the input and the add button.
    @callback(
        Output({"index": MATCH, "type": suffix_for_type(ADDON.INPUT, type)}, 'disabled', allow_duplicate= True),
        Output({"index": MATCH, "type": suffix_for_type(ADDON.DROPDOWN.MENU, type)}, 'disabled', allow_duplicate= True),
        Output({"index": MATCH, "type": suffix_for_type(ADDON.ADD, type)}, 'disabled', allow_duplicate= True),
        Output({"index": MATCH, "type": suffix_for_type(ADDON.DELETE, type)}, 'disabled', allow_duplicate= True),
        Input({"index": MATCH, "type": suffix_for_type(ADDON.DISABLED, type)}, 'data'),
        prevent_initial_call=True
    )
    def control_disabled(disabled):
        return disabled, disabled, disabled, disabled

# Insert the list of DropdownMenuItem components as a callback function to enable the pattern matching function of the callback to work prope
    @callback(
        Output({"index": MATCH, "type": suffix_for_type(ADDON.DROPDOWN.MENU, type)}, 'children', allow_duplicate= True),
        Output({"index": MATCH, "type": suffix_for_type(ADDON.DROPDOWN.ITEMS, type)}, 'data', allow_duplicate= True),
        Input({"index": MATCH, "type": suffix_for_type(ADDON.MEMORY, type)}, 'data'),
        Input({"index": MATCH, "type": suffix_for_type(ADDON.DROPDOWN.LIST, type)}, 'data'),
        prevent_initial_call=True
    )
    def load_layout(
        memory,
        lst: list,
    ):
        if lst and len(lst[-1]) > 0:
            registered = [element for element in range(int(lst[-1][0]), int(lst[-1][-1]) + 1)]
        else:
            registered = []
        dropdown_items = {f'{{"index": {registered_item}, "type": {suffix_for_type(ADDON.DROPDOWN.MENU, type)}}}_{i + 1 + (registered[0] - 1)}': registered_item for i, registered_item in enumerate(
            [str(v) for v in registered]) if registered_item not in memory}
        return [
            dbc.DropdownMenuItem(
                dropdown_value,
                id={"index": dropdown_value,
                    "type": suffix_for_type(ADDON.DROPDOWN.MENUITEMS, type)
                },
                style={"maxWidth": "400px"},
                n_clicks=0,
            ) for dropdown_value in dropdown_items.values()
        ], dropdown_items


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.
    @callback(
        Output({"index": index, "type": suffix_for_type(ADDON.DROPDOWN.MENU, type)}, 'label', allow_duplicate= True),
        Input({"index": ALL, "type": suffix_for_type(ADDON.DROPDOWN.MENUITEMS, type)}, 'n_clicks'),
        State({"index": index, "type": suffix_for_type(ADDON.MEMORY, type)}, 'data'),
        State({"index": index, "type": suffix_for_type(ADDON.DROPDOWN.ITEMS, type)}, 'data'),
        State({"index": index, "type": suffix_for_type(ADDON.DROPDOWN.LIST, type)}, 'data'),
        prevent_initial_call=True
    )
    def update_dropdown_label(_, memory, dropdown_items, dropdown_list):
        ctx = callback_context
        if not ctx.triggered or (len(ctx.triggered) > 1):
            raise PreventUpdate
        else:
            if len(memory) == dropdown_list:
                return [v for v in dropdown_list if v not in memory][0]
            else:
                dropdown_item = ctx.triggered[0]['prop_id'].split('.')[0]
                registered_item= json.loads(dropdown_item)['index']
                triggered_index = f'{{"index": {registered_item}, "type": {suffix_for_type(ADDON.DROPDOWN.MENU, type)}}}_{registered_item}'
                if triggered_index in dropdown_items.keys():
                    return dropdown_items.get(triggered_index, '')
                else:
                    raise PreventUpdate


# callback for add button.
    @callback(
        [
            Output({"index": MATCH, "type": suffix_for_type(ADDON.NEW, type)}, 'children', allow_duplicate= True),
            Output({"index": MATCH, "type": suffix_for_type(ADDON.INPUT, type)}, 'value', allow_duplicate= True),
            Output({"index": MATCH, "type": suffix_for_type(ADDON.DROPDOWN.MENU, type)}, 'label', allow_duplicate= True),
            Output({"index": MATCH, "type": suffix_for_type(ADDON.MEMORY, type)}, 'data', allow_duplicate= True),
            Output({"index": MATCH, "type": suffix_for_type(ADDON.COLLAPSE, type)}, 'is_open', allow_duplicate= True),
        ],
        Input({"index": MATCH, "type": suffix_for_type(ADDON.ADD, type)}, 'n_clicks'),
        [
            State({"index": MATCH, "type": suffix_for_type(ADDON.DROPDOWN.MENU, type)}, 'label'),
            State({"index": MATCH, "type": suffix_for_type(ADDON.INPUT, type)}, 'value'),
            State({"index": MATCH, "type": suffix_for_type(ADDON.MEMORY, type)}, 'data'),
            State({"index": MATCH, "type": suffix_for_type(ADDON.COLLAPSE, type)}, 'is_open'),
        ],
        prevent_initial_call=True
    )
    def add_items(
        _,
        current_label,
        current_input,
        memory,
        is_open,
    ):
        patched_item = Patch()
        # patched_item= []
        if current_input and current_label and current_label!= dropdown_label:
            memory[current_label] = float(current_input)
        # dropdown_items = {key: value for key, value in dropdown_items.items() if value not in memory}
        
        # if (current_label and current_label != dropdown_label)  and current_input:
            # patched_item.append(new_checklist_item(_, type= type, result= {current_label: float(current_input)}))
            sorted_memory= {}
            for k in [str(sorted_key) for sorted_key in sorted([int(key) for key in memory.keys()])]: 
                sorted_memory[k]= memory[k]
            patched_item= [new_checklist_item(_, type= type, index= index, result= {k: v}) for (k, v) in sorted_memory.items()]
            if patched_item:
                is_open= True
            else:
                pass
            return patched_item, "", dropdown_label, memory, is_open
        else:
            raise PreventUpdate
        
    # mark the done items
    @callback(
        Output({"index": MATCH, "type": suffix_for_type(ADDON.OUTPUT, type)}, "style", allow_duplicate= True),
        Input({"index": MATCH, "type": "done"}, "value"),
        prevent_initial_call=True
    )
    def mark_done(done):
        if not done:
            style = {"display": "inline-block",
                     "margin": "5px", "margin-right": "5px"}
        else:
            style = {
                "display": "inline-block",
                "margin": "5px",
                "text-decoration": "line-through",
                "color": "#888",
                "margin-right": "5px",
            }
        return style

# callback for delete button
    @callback(
        Output({"index": index, "type": suffix_for_type(ADDON.NEW, type)}, 'children', allow_duplicate= True),
        Output({"index": index, "type": suffix_for_type(ADDON.MEMORY, type)}, 'data'),
        Output({"index": index, "type": suffix_for_type(ADDON.COLLAPSE, type)}, 'is_open'),
        Input({"index": index, "type": suffix_for_type(ADDON.DELETE, type)}, 'n_clicks'),
        State({'index': ALL, 'type': 'done'}, 'value'),
        State({"index": index, "type": suffix_for_type(ADDON.MEMORY, type)}, 'data'),
        State({"index": index, "type": suffix_for_type(ADDON.COLLAPSE, type)}, 'is_open'),
        prevent_initial_call=True
    )
    def delete_items(_, state, memory, is_open):
        patched_item = Patch()
        values_to_remove = []
        if memory:
            for i, value in enumerate([s for s in state if s]): # Errors occurred when multiple components were deployed and "None" were added in the state list. To address this problem, I filtered the state list to remove all instances of "None" and only kept the instances of "done".  
                if value:
                    values_to_remove.insert(0, i)
            for i in values_to_remove:
                del patched_item[i]
                # remove corresponding items from the memory.
                del memory[list(memory.keys())[i]]
            if not memory:
                is_open= False
            return patched_item, memory, is_open
        else:
            raise PreventUpdate

    return layout

def new_checklist_item(triggered_index, type, index, result):
    return html.Div(
        [
            dcc.Checklist(
                options=[
                    {"label": "", "value": "done"}
                ],
                id={
                    "index": triggered_index,
                    "type": "done"
                },
                style={"display": "inline-block",
                       "margin-right": "5px"},
            ),
            html.Div(
                [
                    html.Li('Apply', style={
                            'display': 'inline-block',
                            "margin-right": "5px",
                            }
                            ),
                    html.Li([*result.values()][-1],
                            style={
                                'display': 'inline-block',
                                "margin-right": "5px",
                    }
                    ),
                    html.Li('from the', style={
                            'display': 'inline-block',
                            "margin-right": "5px",
                            }
                    ),
                    html.Li([*result][-1],
                            style={
                                'display': 'inline-block',
                                "margin-right": "1px",
                            }
                    ),
                    html.Li(('st' if c == "1" 
                                  else ('nd' if c == "2" else ('rd' if c == "3" else 'th'))) if len(c := [*result.keys()][-1]) == 1 else ('st' if c[-1] == '1' else ('nd' if c[-1] == '2' else ('rd' if c[-1] == '3' else 'th'))), 
                            style={
                            'display': 'inline-block',
                            "margin-right": "5px",
                            },
                    ),
                ],
                id={
                    "index": triggered_index,
                    "type": suffix_for_type(ADDON.OUTPUT, type)
                },
                style={
                    "display": "inline-block",
                    "margin": "5px",
                    'margin-right': '5px',
                    "maxWidth": "400px"
                },
            ),
        ],
    )


# build a refeshable dropdown that can refresh the options when the refresh button is clicked.
def refreshable_dropdown(
        label: str,
        # ['prepay', 'subsidy'] Consider the case of duplicate ids.
        type: str = 'prepay',
        placeholder: str = 'Choose methods of the payment',
        options: dict = amortization_types,
        disabled: bool = False,
        index= "",
        **kwargs
):
    """
    There are two dropdown components in the layout: one for the payment options and the other for refreshing the options accordingly. 
    Note that since there are two kinds of types, 'prepay' and 'subsidy', 
    the IDs of the components are formatted as {'index': type, 'type': original ID of the component} in order to separate the types within the layout.
    """
    dropdown = html.Div(
        [
            dbc.Label(label),
            html.Div([
                html.Div(
                    [
                        dcc.Dropdown(
                            id={"index": index, "type": suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, type)},
                            options=[*options],
                            value=[*options],
                            multi=True,
                            # searchable=True,
                            placeholder=placeholder,
                            disabled=disabled,
                            **kwargs
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.Button(
                            'Refresh',
                            id={"index": index, "type": suffix_for_type(ADVANCED.DROPDOWN.BUTTON, type)},
                            n_clicks=0
                        )
                    ]
                )
            ],
            ),
        ],
        className='mb-3'
    )

    # Refresh the Dropdown of the Payment options
    @callback(
        Output({"index": index, "type": suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, type)}, 'value'),
        Input({"index": index, "type": suffix_for_type(ADVANCED.DROPDOWN.BUTTON, type)}, 'n_clicks'),
    )
    def refresh_options(_: int):
        return [*options]
    return dropdown


# py -m app.Dashboard.components.Controls.widgets
if __name__ == "__main__":
    app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], 
           suppress_callback_exceptions=True
           )

    app.layout = html.Div(
        [
            refreshable_dropdown(
                label='Test for refreshable dropdown'),
            html.Hr(),
            html.H6('Test for addon'),
            addon(
                type='test',
                # dropdown_list=[1, 2],
                # dropdown_label="Time",
                placeholder="Input the timepoint",
            )
        ]
    )
    app.run_server(debug=True)
