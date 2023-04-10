# This file is for the tailor-made widgets for controls including refreshable dropdown, addon function for generating a dict for the combined input of payment arrangement.

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


class className:
    DROPDOWN_BUTTON = 'dropdown-button'

# build a refeshable dropdown that can refresh the options when the refresh button is clicked.


def refreshable_dropdown(
        label: str,
        # ['prepay', 'subsidy'] Consider the case of duplicate ids.
        type: str = 'prepay',
        placeholder: str = 'Choose methods of the payment',
        options: dict = amortization_types,
        disabled: bool = False,
):
    dropdown = html.Div(
        [
            dbc.Label(label),
            html.Div([
                html.Div(
                    [
                        dcc.Dropdown(
                            id=LOAN.DROPDOWN.REFRESHABLE + "_" + type,
                            options=[*options],
                            # options=to_dropdown_options([*options]),
                            value=[*options],
                            multi=True,
                            # searchable=True,
                            placeholder=placeholder,
                            disabled=disabled,
                            style={
                                "width": "67%",
                            }
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.Button(
                            'Refresh',
                            className=className.DROPDOWN_BUTTON,
                            id=LOAN.DROPDOWN.BUTTON + "_" + type,
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
        Output(LOAN.DROPDOWN.REFRESHABLE + "_" + type, 'value'),
        Input(LOAN.DROPDOWN.BUTTON + "_" + type, 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_options(_: int):
        return [*options]
    return dropdown

# Addons function for the payment arrangement.
# For further information, please refer to the documentation of the addon function in the file Amort\test\ADDON.py.


def addon(
        # Type need to be indicated within ['prepay', 'subsidy'] to distinguish the different dropdowns.
        type: str,
        dropdown_list: list,
        dropdown_label: str,
        placeholder: str,
        disabled: bool = False,


):

    layout = html.Div(
        [
            dcc.Store(id=suffix_for_type(ADDON.DROPDOWN.LIST, type),
                      data=[1] if dropdown_list is None else dropdown_list),
            dcc.Store(id=suffix_for_type(ADDON.DISABLED, type), data=disabled),
            # That's the outcome what we want.
            dcc.Store(id=suffix_for_type(ADDON.MEMORY, type), data={}),
            dcc.Store(id=suffix_for_type(ADDON.DROPDOWN.ITEMS, type), data={}),
            html.Div(id=suffix_for_type(ADDON.NEW, type)),
            html.Div(
                [
                    dbc.DropdownMenu(
                        [],
                        label=dropdown_label,
                        id=suffix_for_type(ADDON.DROPDOWN.MENU, type),
                        style={'width': "100%"},
                        disabled=disabled,
                    ),
                    dcc.Input(id=suffix_for_type(ADDON.INPUT, type),
                              type='number',
                              placeholder=placeholder,
                              disabled=disabled,
                              ),
                    dbc.Button(
                        id=suffix_for_type(ADDON.ADD, type),
                        color="primary",
                        children="Add",
                        disabled=disabled,
                    ),
                    dbc.Button(
                        id=suffix_for_type(ADDON.DELETE, type),
                        color="danger",
                        children="Delete",
                        disabled=disabled,
                    )
                ],
                style={'display': 'inline-flex'},
            ),
        ]
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
        Input(suffix_for_type(ADDON.DROPDOWN.LIST, type), 'data'),
    )
    def load_layout(
        memory,
        lst,
    ):
        lst = [str(element) for element in lst]
        dropdown_items = {f'{suffix_for_type(ADDON.DROPDOWN.MENU, type)}_{i+1}': item for i, item in enumerate(
            [str(v) for v in lst]) if item not in memory}
        return [dbc.DropdownMenuItem(
            dropdown_value,
            id={"index": dropdown_value,
                "type": suffix_for_type(ADDON.DROPDOWN.MENU, type)},
            # id=dropdown_key,
            style={'width': '100%'},
            n_clicks=0,
        ) for dropdown_value in dropdown_items.values()
        ], dropdown_items


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.

    @callback(
        Output(suffix_for_type(ADDON.DROPDOWN.MENU, type), 'label'),
        Input({"index": ALL, "type": suffix_for_type(
            ADDON.DROPDOWN.MENU, type)}, 'n_clicks'),
        State(suffix_for_type(ADDON.MEMORY, type), 'data'),
        State(suffix_for_type(ADDON.DROPDOWN.ITEMS, type), 'data'),
        State(suffix_for_type(ADDON.DROPDOWN.LIST, type), 'data'),
        # [Input(dropdown_key, 'n_clicks')
        #  for dropdown_key in dropdown_items.keys()],
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
                        style={"display": "inline"},
                    ),
                    html.Div(
                        [
                            html.Li([*memory][-1]),
                            html.Li([*memory.values()][-1])
                        ],
                        id={
                            "index": _,
                            "type": suffix_for_type(ADDON.OUTPUT, type)
                        },
                        style={"display": "inline", "margin": "10px"},
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
            style = {"display": "inline", "margin": "10px"}
        else:
            style = {
                "display": "inline",
                "margin": "10px",
                "text-decoration": "line-through",
                "color": "#888",
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
        for i, value in enumerate(state):
            if value:
                values_to_remove.insert(0, i)
        for i in values_to_remove:
            del patched_item[i]
            # remove corresponding items from the memory.
            del memory[list(memory.keys())[i]]
        return patched_item, memory

    return layout


# py -m Amort.dashboard.components.homepage.widgets
if __name__ == "__main__":
    from dash import Dash
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div(
        addon(
            type='prepay',
            dropdown_list=[1, 2, 3],
            dropdown_label="TimePoint",
            placeholder="Input the timepoint",
        )
    )
    app.run_server(debug=True)
