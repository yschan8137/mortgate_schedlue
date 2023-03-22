from dash import dcc, html, Input, Output, State, callback, callback_context, MATCH, ALL, Patch
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import json


def addon(
        dropdown_list: list,
        dropdown_label: str,
        placeholder: str,
):
    dropdown_list = [str(element) for element in dropdown_list]

    def dropdown_key_format(n):
        return f'{addon.DROPDOWN.MENU}_{n}'

    layout = html.Div(
        [
            dcc.Store(id=addon.MEMORY, data={}),
            dcc.Store(id=addon.DROPDOWN.ITEMS),
            html.Div(id=addon.NEW_ITEMS),
            html.Div(
                [
                    dbc.DropdownMenu(
                        [],
                        label=dropdown_label,
                        id=addon.DROPDOWN.MENU,
                        style={'width': "100%"}
                    ),
                    dcc.Input(id=addon.INPUT, type='number',
                              placeholder=placeholder),
                    dbc.Button(
                        id=addon.ADD,
                        color="primary",
                        children="Add"
                    ),
                    dbc.Button(
                        id=addon.DELETE,
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
        Output(addon.DROPDOWN.MENU, 'children'),
        Output(addon.DROPDOWN.ITEMS, 'data'),
        Input(addon.DROPDOWN.MENU, 'children'),
        Input(addon.MEMORY, 'data')
    )
    def load_layout(
        dropdown_container,
        memory
    ):
        dropdown_items = {f'{addon.DROPDOWN.MENU}_{i+1}': item for i, item in enumerate(
            [str(v) for v in dropdown_list]) if item not in memory}
        return [dbc.DropdownMenuItem(
            dropdown_value,
            id={"index": dropdown_value, "type": addon.DROPDOWN.MENU},
            # id=dropdown_key,
            style={'width': '100%'},
            n_clicks=0,
        ) for (dropdown_key, dropdown_value) in dropdown_items.items()
        ], dropdown_items


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.

    @callback(
        Output(addon.DROPDOWN.MENU, 'label'),
        Input({"index": ALL, "type": addon.DROPDOWN.MENU}, 'n_clicks'),
        State(addon.MEMORY, 'data'),
        State(addon.DROPDOWN.ITEMS, 'data'),
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
                triggered_index = addon.DROPDOWN.MENU + \
                    '_' + json.loads(dropdown_item)['index']
                if triggered_index in dropdown_items.keys():
                    return dropdown_items.get(triggered_index, '')
                else:
                    raise PreventUpdate


# callback for add button.


    @ callback(
        [
            Output(addon.NEW_ITEMS, 'children', allow_duplicate=True),
            Output(addon.INPUT, 'value'),
            Output(addon.DROPDOWN.MENU, 'label', allow_duplicate=True),
            Output(addon.MEMORY, 'data', allow_duplicate=True),
        ],
        Input(addon.ADD, 'n_clicks'),
        [
            State(addon.DROPDOWN.MENU, 'label'),
            State(addon.INPUT, 'value'),
            State(addon.MEMORY, 'data'),
            State(addon.DROPDOWN.ITEMS, 'data'),
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
                            "type": addon.OUTPUT
                        },
                        style={"display": "inline", "margin": "10px"},
                    ),
                ],
            )
        if (current_label and current_label != dropdown_label) and current_input:
            patched_item.append(new_checklist_item())
        return patched_item, "", dropdown_label, memory

    @ callback(
        Output({"index": MATCH, "type": addon.OUTPUT}, "style"),
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
        Output(addon.NEW_ITEMS, 'children', allow_duplicate=True),
        Output(addon.MEMORY, 'data', allow_duplicate=True),
        Input(addon.DELETE, 'n_clicks'),
        State({'index': ALL, 'type': 'done'}, 'value'),
        State(addon.MEMORY, 'data'),
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
