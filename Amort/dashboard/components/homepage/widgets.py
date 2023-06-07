# This file is for the tailor-made widgets for controls including OPTIONS dropdown, addon function for generating a dict for the combined input of payment arrangement.

from distutils.log import debug
from re import S
from dash import dcc, html, Input, Output, State, callback, callback_context, MATCH, ALL, Patch  # type: ignore
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from ..toolkit import to_dropdown_options, suffix_for_type
from ..ids import *
from ..ids import LOAN, ADDON
from .. import amortization_types
import json


# Addons function for the payment arrangement.
# For further information, please refer to the documentation of the addon function in the file Amort\test\ADDON.py.


def addon(
        # Type need to be indicated within ['prepay', 'subsidy'] to distinguish the different dropdowns.
        type: str,
        # dropdown_list: list,
        dropdown_label: str,
        placeholder: str,
        pattern_matching=False,
        disabled: bool = False,


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
            dcc.Store(id={False: suffix_for_type(ADDON.DROPDOWN.LIST, type),
                          True: {'index': type, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, type)}}[pattern_matching],
                      data=0
                      ),
            dcc.Store(id=suffix_for_type(ADDON.DISABLED, type), data=disabled),
            # That's the outcome what we want.
            dcc.Store(id=suffix_for_type(ADDON.MEMORY, type), data={}),
            dcc.Store(id=suffix_for_type(ADDON.DROPDOWN.ITEMS, type), data={}),
            html.Div(
                [
                    dbc.DropdownMenu(
                        [],
                        label=dropdown_label,
                        id=suffix_for_type(ADDON.DROPDOWN.MENU, type),
                        disabled=disabled,
                        color='green',
                        # style={'width': '30%'}
                    ),
                    # html.Div(
                    # [
                    dbc.Button(
                        id=suffix_for_type(ADDON.ADD, type),
                        color="primary",
                        children="Add",
                        disabled=disabled,
                    ),
                    dbc.Button(
                        id=suffix_for_type(ADDON.DELETE, type),
                        color="danger",
                        children="Del",
                        disabled=disabled,
                    )
                    # ],
                    # style={
                    # 'display': 'inline-flex',
                    # }
                    # ),
                ],
                style={
                    'display': 'inline-flex',
                }
            ),
            html.Div(
                dbc.Input(id=suffix_for_type(ADDON.INPUT, type),
                          type='number',
                          step=0.01,
                          min=0,
                          max=100,
                          placeholder=placeholder,
                          disabled=disabled,
                          ),
            ),
            html.Div(id=suffix_for_type(ADDON.NEW, type)),
        ],
        # make the width not exceed the width of the container.
        style={
            'width': '100%',
        },
    )


# Control the disabled status of the input and the add button.

    @callback(
        Output(suffix_for_type(ADDON.INPUT, type), 'disabled'),
        Output(suffix_for_type(ADDON.DROPDOWN.MENU, type), 'disabled'),
        Output(suffix_for_type(ADDON.ADD, type), 'disabled'),
        Output(suffix_for_type(ADDON.DELETE, type), 'disabled'),
        Input(suffix_for_type(ADDON.DISABLED, type), 'data'),
        prevent_initial_call=True
    )
    def control_disabled(disabled):
        return disabled, disabled, disabled, disabled
# Insert the list of DropdownMenuItem components as a callback function to enable the pattern matching function of the callback to work prope

    @callback(
        Output(suffix_for_type(ADDON.DROPDOWN.MENU, type), 'children'),
        Output(suffix_for_type(ADDON.DROPDOWN.ITEMS, type), 'data'),
        Input(suffix_for_type(ADDON.MEMORY, type), 'data'),
        Input({False: suffix_for_type(ADDON.DROPDOWN.LIST, type),
               True: {'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, type)}}[pattern_matching], 'data'),
        prevent_initial_call=True
    )
    def load_layout(
        memory,
        lst: list,
    ):
        lst = [element for element in range(
            int(lst[-1][0]), int(lst[-1][-1]) + 1)]
        dropdown_items = {f'{suffix_for_type(ADDON.DROPDOWN.MENU, type)}_{i+1}': item for i, item in enumerate(
            [str(v) for v in lst]) if item not in memory}
        return [dbc.DropdownMenuItem(
            dropdown_value,
            id={"index": dropdown_value,
                "type": suffix_for_type(ADDON.DROPDOWN.MENUITEMS, type)},
            style={"maxWidth": "400px"},
            n_clicks=0,
        ) for dropdown_value in dropdown_items.values()
        ], dropdown_items


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.


    @callback(
        Output(suffix_for_type(ADDON.DROPDOWN.MENU, type), 'label'),
        Input({"index": ALL, "type": suffix_for_type(
            ADDON.DROPDOWN.MENUITEMS, type)}, 'n_clicks'),
        State(suffix_for_type(ADDON.MEMORY, type), 'data'),
        State(suffix_for_type(ADDON.DROPDOWN.ITEMS, type), 'data'),
        State({False: suffix_for_type(ADDON.DROPDOWN.LIST, type),
               True: {'index': ALL, 'type': suffix_for_type(ADDON.DROPDOWN.LIST, type)}
               }[pattern_matching], 'data'),
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
                triggered_index = suffix_for_type(ADDON.DROPDOWN.MENU, type) + \
                    '_' + json.loads(dropdown_item)['index']
                if triggered_index in dropdown_items.keys():
                    return dropdown_items.get(triggered_index, '')
                else:
                    raise PreventUpdate


# callback for add button.

    @ callback(
        [
            Output(suffix_for_type(ADDON.NEW, type), 'children',
                   allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.INPUT, type), 'value'),
            Output(suffix_for_type(ADDON.DROPDOWN.MENU, type), 'label',
                   allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.MEMORY, type), 'data',
                   allow_duplicate=True),  # type: ignore
        ],
        Input(suffix_for_type(ADDON.ADD, type), 'n_clicks'),
        [
            State(suffix_for_type(ADDON.DROPDOWN.MENU, type), 'label'),
            State(suffix_for_type(ADDON.INPUT, type), 'value'),
            State(suffix_for_type(ADDON.MEMORY, type), 'data'),
            State(suffix_for_type(ADDON.DROPDOWN.ITEMS, type), 'data'),
        ],
        prevent_initial_call=True
    )
    def add_items(
        _,
        current_label,
        current_input,
        memory,
        dropdown_items
    ):
        patched_item = Patch()
        if current_input and current_label:
            memory[current_label] = float(current_input)

        dropdown_items = {key: value for key,
                          value in dropdown_items.items() if value not in memory}

        def new_checklist_item():
            return html.Div(
                [
                    dcc.Checklist(
                        options=[
                            {"label": "", "value": "done"}
                        ],
                        id={
                            "index": _,
                            "type": "done"
                        },
                        style={"display": "inline-block",
                               "margin-right": "15px"},
                    ),
                    html.Div(
                        [
                            html.Li('Apply', style={
                                    'display': 'inline-block',
                                    "margin-right": "5px",
                                    }
                                    ),
                            html.Li([*memory.values()][-1],
                                    style={
                                        'display': 'inline-block',
                                        "margin-right": "5px",
                            }
                            ),
                            html.Li('on', style={
                                    'display': 'inline-block',
                                    "margin-right": "5px",
                                    }
                                    ),
                            html.Li([*memory][-1],
                                    style={'display': 'inline-block'}
                                    ),

                        ],
                        id={
                            "index": _,
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
        if (current_label and current_label != dropdown_label) and current_input:
            patched_item.append(new_checklist_item())
        return patched_item, "", dropdown_label, memory

    @ callback(
        Output({"index": MATCH, "type": suffix_for_type(
            ADDON.OUTPUT, type)}, "style"),
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
        Output(suffix_for_type(ADDON.NEW, type), 'children',
               allow_duplicate=True),  # type: ignore
        Output(suffix_for_type(ADDON.MEMORY, type), 'data',
               allow_duplicate=True),  # type: ignore
        Input(suffix_for_type(ADDON.DELETE, type), 'n_clicks'),
        State({'index': ALL, 'type': 'done'}, 'value'),
        State(suffix_for_type(ADDON.MEMORY, type), 'data'),
        prevent_initial_call=True
    )
    def delete_items(_, state, memory):
        patched_item = Patch()
        values_to_remove = []
        if memory:
            for i, value in enumerate(state):
                if value:
                    values_to_remove.insert(0, i)
            for i in values_to_remove:
                del patched_item[i]
                # remove corresponding items from the memory.
                del memory[list(memory.keys())[i]]
            return patched_item, memory
        else:
            raise PreventUpdate

    return layout


# build a refeshable dropdown that can refresh the options when the refresh button is clicked.


def refreshable_dropdown(
        label: str,
        # ['prepay', 'subsidy'] Consider the case of duplicate ids.
        type: str = 'prepay',
        placeholder: str = 'Choose methods of the payment',
        options: dict = amortization_types,
        disabled: bool = False,
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
                            id=suffix_for_type(
                                ADVANCED.DROPDOWN.OPTIONS, type),
                            options=[*options],
                            value=[*options],
                            multi=True,
                            # searchable=True,
                            placeholder=placeholder,
                            disabled=disabled,
                            style={
                                "width": "100%",
                            }
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.Button(
                            'Refresh',
                            id=suffix_for_type(ADVANCED.DROPDOWN.BUTTON, type),
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
        Output(suffix_for_type(ADVANCED.DROPDOWN.OPTIONS, type), 'value'),
        Input(suffix_for_type(ADVANCED.DROPDOWN.BUTTON, type), 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_options(_: int):
        return [*options]
    return dropdown


# py -m Amort.dashboard.components.homepage.widgets
if __name__ == "__main__":
    from dash import Dash
    app = Dash(__name__, external_stylesheets=[
               dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
    app.layout = html.Div(
        [
            refreshable_dropdown(label='Test'),
            addon(
                type='test',
                # dropdown_list=[1, 2],
                dropdown_label="TimePoint",
                placeholder="Input the timepoint",
            )
        ]
    )
    app.run_server(debug=True)
