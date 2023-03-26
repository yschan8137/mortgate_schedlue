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
                            # style={
                            # "display": "table-cell",
                            # "width": "310px",
                            # }
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
        type: str,  # ['prepay', 'subsidy']
        dropdown_list: list,
        dropdown_label: str,
        placeholder: str,
        disabled: bool = True,


):

    def dropdown_key_format(n):
        return f'{suffix_for_type(ADDON.DROPDOWN.MENU) + "_" + type}_{n}'

    layout = html.Div(
        [
            dcc.Store(id=suffix_for_type(suffix_for_type(
                ADDON.DROPDOWN.LIST)), data=dropdown_list),
            dcc.Store(id=suffix_for_type(ADDON.DISABLED), data=disabled),
            dcc.Store(id=suffix_for_type(ADDON.MEMORY), data={}),
            dcc.Store(id=suffix_for_type(ADDON.DROPDOWN.ITEMS), data={}),
            html.Div(id=suffix_for_type(ADDON.NEW_ITEMS)),
            html.Div(
                [
                    dbc.DropdownMenu(
                        [],
                        label=dropdown_label,
                        id=suffix_for_type(ADDON.DROPDOWN.MENU),
                        style={'width': "100%"},
                        disabled=disabled,
                    ),
                    dcc.Input(id=suffix_for_type(ADDON.INPUT),
                              type='number',
                              placeholder=placeholder,
                              disabled=disabled,
                              ),
                    dbc.Button(
                        id=suffix_for_type(ADDON.ADD),
                        color="primary",
                        children="Add",
                        disabled=disabled,
                    ),
                    dbc.Button(
                        id=suffix_for_type(ADDON.DELETE),
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
        Output(suffix_for_type(ADDON.INPUT), 'disabled'),
        Output(suffix_for_type(ADDON.DROPDOWN.MENU), 'disabled'),
        Output(suffix_for_type(ADDON.ADD), 'disabled'),
        Output(suffix_for_type(ADDON.DELETE), 'disabled'),
        Input(suffix_for_type(ADDON.DISABLED), 'data'),
        prevent_initial_call=True
    )
    def control_disabled(disabled):
        return disabled, disabled, disabled, disabled
# Insert the list of DropdownMenuItem components as a callback function to enable the pattern matching function of the callback to work prope

    @callback(
        Output(suffix_for_type(ADDON.DROPDOWN.MENU), 'children'),
        Output(suffix_for_type(ADDON.DROPDOWN.ITEMS), 'data'),
        Input(suffix_for_type(ADDON.DROPDOWN.MENU), 'children'),
        Input(suffix_for_type(ADDON.MEMORY), 'data'),
        State(suffix_for_type(ADDON.DROPDOWN.LIST), 'data'),
    )
    def load_layout(
        dropdown_container,
        memory,
        lst,
    ):
        lst = [str(element) for element in lst]
        dropdown_items = {f'{suffix_for_type(ADDON.DROPDOWN.MENU)}_{i+1}': item for i, item in enumerate(
            [str(v) for v in lst]) if item not in memory}
        return [dbc.DropdownMenuItem(
            dropdown_value,
            id={"index": dropdown_value,
                "type": suffix_for_type(ADDON.DROPDOWN.MENU)},
            # id=dropdown_key,
            style={'width': '100%'},
            n_clicks=0,
        ) for (dropdown_key, dropdown_value) in dropdown_items.items()
        ], dropdown_items


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.


    @callback(
        Output(suffix_for_type(ADDON.DROPDOWN.MENU), 'label'),
        Input({"index": ALL, "type": suffix_for_type(
            ADDON.DROPDOWN.MENU)}, 'n_clicks'),
        State(suffix_for_type(ADDON.MEMORY), 'data'),
        State(suffix_for_type(ADDON.DROPDOWN.ITEMS), 'data'),
        # [Input(dropdown_key, 'n_clicks')
        #  for dropdown_key in dropdown_items.keys()],
        prevent_initial_call=True
    )
    def update_dropdown_label(_, memory, dropdown_items):
        ctx = callback_context
        if not ctx.triggered or (len(ctx.triggered) > 1):
            raise PreventUpdate
        else:
            if len(memory) == dropdown_list:
                return [v for v in dropdown_list if v not in memory][0]
            else:
                dropdown_item = ctx.triggered[0]['prop_id'].split('.')[0]
                triggered_index = suffix_for_type(ADDON.DROPDOWN.MENU) + \
                    '_' + json.loads(dropdown_item)['index']
                if triggered_index in dropdown_items.keys():
                    return dropdown_items.get(triggered_index, '')
                else:
                    raise PreventUpdate


# callback for add button.

    @ callback(
        [
            Output(suffix_for_type(ADDON.NEW_ITEMS), 'children',
                   allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.INPUT), 'value'),
            Output(suffix_for_type(ADDON.DROPDOWN.MENU), 'label',
                   allow_duplicate=True),  # type: ignore
            Output(suffix_for_type(ADDON.MEMORY), 'data',
                   allow_duplicate=True),  # type: ignore
        ],
        Input(suffix_for_type(ADDON.ADD), 'n_clicks'),
        [
            State(suffix_for_type(ADDON.DROPDOWN.MENU), 'label'),
            State(suffix_for_type(ADDON.INPUT), 'value'),
            State(suffix_for_type(ADDON.MEMORY), 'data'),
            State(suffix_for_type(ADDON.DROPDOWN.ITEMS), 'data'),
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
                            "type": suffix_for_type(ADDON.OUTPUT)
                        },
                        style={"display": "inline", "margin": "10px"},
                    ),
                ],
            )
        if (current_label and current_label != dropdown_label) and current_input:
            patched_item.append(new_checklist_item())
        return patched_item, "", dropdown_label, memory

    @ callback(
        Output({"index": MATCH, "type": suffix_for_type(ADDON.OUTPUT)}, "style"),
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
        Output(suffix_for_type(ADDON.NEW_ITEMS), 'children',
               allow_duplicate=True),  # type: ignore
        Output(suffix_for_type(ADDON.MEMORY), 'data',
               allow_duplicate=True),  # type: ignore
        Input(suffix_for_type(ADDON.DELETE), 'n_clicks'),
        State({'index': ALL, 'type': 'done'}, 'value'),
        State(suffix_for_type(ADDON.MEMORY), 'data'),
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
