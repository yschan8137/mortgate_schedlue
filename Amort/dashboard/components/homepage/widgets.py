# This file is for the tailor-made widgets for controls including refreshable dropdown, addon function for generating a dict for the combined input of payment arrangement.

from distutils.log import debug
from re import S
from dash import dcc, html, Input, Output, State, callback, callback_context, MATCH, ALL, Patch  # type: ignore
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from ..toolkit import to_dropdown_options
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
        dropdown_list: list,
        dropdown_label: str,
        placeholder: str,

):
    dropdown_list = [str(element) for element in dropdown_list]

    def dropdown_key_format(n):
        return f'{ADDON.DROPDOWN.MENU}_{n}'

    layout = html.Div(
        [
            dcc.Store(id=ADDON.MEMORY, data={}),
            dcc.Store(id=ADDON.DROPDOWN.ITEMS),
            html.Div(id=ADDON.NEW_ITEMS),
            html.Div(
                [
                    dbc.DropdownMenu(
                        [],
                        label=dropdown_label,
                        id=ADDON.DROPDOWN.MENU,
                        style={'width': "100%"}
                    ),
                    dcc.Input(id=ADDON.INPUT, type='number',
                              placeholder=placeholder),
                    dbc.Button(
                        id=ADDON.ADD,
                        color="primary",
                        children="Add"
                    ),
                    dbc.Button(
                        id=ADDON.DELETE,
                        color="danger",
                        children="Delete"
                    )
                ],
                style={'display': 'inline-flex'}
            ),
        ]
    )

# Insert the list of DropdownMenuItem components as a callback function to enable the pattern matching function of the callback to work prope
    @callback(
        Output(ADDON.DROPDOWN.MENU, 'children'),
        Output(ADDON.DROPDOWN.ITEMS, 'data'),
        Input(ADDON.DROPDOWN.MENU, 'children'),
        Input(ADDON.MEMORY, 'data')
    )
    def load_layout(
        dropdown_container,
        memory
    ):
        dropdown_items = {f'{ADDON.DROPDOWN.MENU}_{i+1}': item for i, item in enumerate(
            [str(v) for v in dropdown_list]) if item not in memory}
        return [dbc.DropdownMenuItem(
            dropdown_value,
            id={"index": dropdown_value, "type": ADDON.DROPDOWN.MENU},
            # id=dropdown_key,
            style={'width': '100%'},
            n_clicks=0,
        ) for (dropdown_key, dropdown_value) in dropdown_items.items()
        ], dropdown_items


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.


    @callback(
        Output(ADDON.DROPDOWN.MENU, 'label'),
        Input({"index": ALL, "type": ADDON.DROPDOWN.MENU}, 'n_clicks'),
        State(ADDON.MEMORY, 'data'),
        State(ADDON.DROPDOWN.ITEMS, 'data'),
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
                triggered_index = ADDON.DROPDOWN.MENU + \
                    '_' + json.loads(dropdown_item)['index']
                if triggered_index in dropdown_items.keys():
                    return dropdown_items.get(triggered_index, '')
                else:
                    raise PreventUpdate


# callback for add button.

    @ callback(
        [
            Output(ADDON.NEW_ITEMS, 'children',
                   allow_duplicate=True),  # type: ignore
            Output(ADDON.INPUT, 'value'),
            Output(ADDON.DROPDOWN.MENU, 'label',
                   allow_duplicate=True),  # type: ignore
            Output(ADDON.MEMORY, 'data', allow_duplicate=True),  # type: ignore
        ],
        Input(ADDON.ADD, 'n_clicks'),
        [
            State(ADDON.DROPDOWN.MENU, 'label'),
            State(ADDON.INPUT, 'value'),
            State(ADDON.MEMORY, 'data'),
            State(ADDON.DROPDOWN.ITEMS, 'data'),
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
                            "type": ADDON.OUTPUT
                        },
                        style={"display": "inline", "margin": "10px"},
                    ),
                ],
            )
        if (current_label and current_label != dropdown_label) and current_input:
            patched_item.append(new_checklist_item())
        return patched_item, "", dropdown_label, memory

    @ callback(
        Output({"index": MATCH, "type": ADDON.OUTPUT}, "style"),
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
        Output(ADDON.NEW_ITEMS, 'children',
               allow_duplicate=True),  # type: ignore
        Output(ADDON.MEMORY, 'data', allow_duplicate=True),  # type: ignore
        Input(ADDON.DELETE, 'n_clicks'),
        State({'index': ALL, 'type': 'done'}, 'value'),
        State(ADDON.MEMORY, 'data'),
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


class advanced_items:
    @classmethod
    def prepay_plan(cls):
        layout = [
            dbc.Col(
                [
                    dbc.Label('Advanced Options', size='md'),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    dbc.Checklist(
                                        options=[
                                            {'label': 'Prepay Plan', 'value': 0},
                                        ],
                                        id=LOAN.PREPAY.OPTION,
                                        switch=True,
                                        inline=True,
                                        value=[]
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.Label('Prepay Amount'),
                                        dbc.Input(
                                            id=LOAN.PREPAY.AMOUNT,
                                            type='number',
                                            step=1,
                                            value=[0],
                                            min=[0],
                                            disabled=True,
                                        ),
                                        dbc.Label('Prepay Arrangement'),
                                        dbc.Input(
                                            id=LOAN.PREPAY.ARR,
                                            value=[0],
                                            disabled=True,
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
                Output(LOAN.PREPAY.ARR, 'disabled'),
                Output(LOAN.PREPAY.AMOUNT, 'disabled')
            ],
            Input(LOAN.PREPAY.OPTION, 'value')
        )
        def enable_prepay_options(option):
            if option == [0]:
                return [False] * 2
            else:
                return [True] * 2

    @classmethod
    def subsidy_plan(cls):
        layout = [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dbc.Checklist(
                                options=[
                                    {'label': 'Subsidy loan', 'value': 0}
                                ],
                                id=LOAN.SUBSIDY.OPTION,
                                switch=True,
                                inline=True,
                                value=[]
                            ),
                        ),
                        dbc.CardBody(
                            [
                                dbc.Label('Timepoint of Application'),
                                dbc.Input(
                                    id=LOAN.SUBSIDY.TIME,
                                    value=0,
                                    step=1,
                                    disabled=True,
                                ),
                                dbc.Label('Amount'),
                                dbc.Input(
                                    id=LOAN.SUBSIDY.AMOUNT,
                                    value=0,
                                    step=1,
                                    disabled=True,
                                ),
                                dbc.Label('Term'),
                                dbc.Input(
                                    id=LOAN.SUBSIDY.TERM,
                                    value=20,
                                    step=1,
                                    disabled=True,
                                ),
                                refreshable_dropdown(
                                    label='Payment method',
                                    options=amortization_types,
                                    disabled=False
                                )
                            ]
                        ),
                    ],
                    class_name="mb-3",
                    outline=True,
                )
            )
        ]
        # Activate the subsidy options

        @callback(
            [
                Output(LOAN.SUBSIDY.INTEREST, 'disabled'),
                Output(LOAN.SUBSIDY.AMOUNT, 'disabled'),
                Output(LOAN.SUBSIDY.METHOD, 'disabled'),
                Output(LOAN.SUBSIDY.TERM, 'disabled'),
                Output(LOAN.SUBSIDY.TIME, 'disabled'),
            ],
            Input(LOAN.SUBSIDY.OPTION, 'value')
        )
        def enable_subsidy_options(option):
            if option == [0]:
                return [False] * 5
            else:
                return [True] * 5
        return layout


# py -m Amort.dashboard.components.homepage.widgets
if __name__ == "__main__":
    from dash import Dash
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div(
        addon(
            dropdown_list=[1, 2, 3],
            dropdown_label="TimePoint",
            placeholder="Input the timepoint",
        )
    )
    app.run_server(debug=True)
