from os import O_TRUNC
from dash import Dash, dcc, html, Input, Output, State, callback, callback_context, ALL, MATCH, Patch
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import json

# 2023/03/13-2023/03/20
# This is a custom component that allows you to add and delete items to a dictionary. The dictionary is stored in the memory of the browser. The dictionary is used to store the items that are added to the list of items. The list of items is a list of dbc.DropdownMenuItem components. The items in the list of items are selected by the user and are stored in the memory of the browser. The items in the memory are removed if the delete button is clicked, and the items in the memory are added to the list of items if the add button is clicked.


class ids_addon:
    NEW_ITEMS = 'new-items'
    ADD = 'addon function'
    DELETE = 'delete function'
    MEMORY = 'memory'
    INPUT = 'input'
    OUTPUT = 'output'

    class DROPDOWN:
        MENU = 'dropdown-menu'
        ITEMS = 'dropdown-items'

# addon function to create a custom component.


def addon(
        dropdown_list: list,
        dropdown_label: str,
        placeholder: str,
):
    dropdown_list = [str(element) for element in dropdown_list]

    def dropdown_key_format(n):
        return f'{ids_addon.DROPDOWN.MENU}_{n}'

    layout = html.Div(
        [
            dcc.Store(id=ids_addon.MEMORY, data={}),
            dcc.Store(id=ids_addon.DROPDOWN.ITEMS),
            html.Div(id=ids_addon.NEW_ITEMS),
            html.Div(
                [
                    dbc.DropdownMenu(
                        [],
                        label=dropdown_label,
                        id=ids_addon.DROPDOWN.MENU,
                        style={'width': "100%"}
                    ),
                    dcc.Input(id=ids_addon.INPUT, type='number',
                              placeholder=placeholder),
                    dbc.Button(
                        id=ids_addon.ADD,
                        color="primary",
                        children="Add"
                    ),
                    dbc.Button(
                        id=ids_addon.DELETE,
                        color="danger",
                        children="Delete"
                    )
                ],
                style={'display': 'inline-flex'}
            ),
        ]
    )

# Insert the list of DropdownMenuItem components as a callback function to enable the pattern matching function of the callback to work properly.
    @callback(
        Output(ids_addon.DROPDOWN.MENU, 'children'),
        Output(ids_addon.DROPDOWN.ITEMS, 'data'),
        Input(ids_addon.DROPDOWN.MENU, 'children'),
        Input(ids_addon.MEMORY, 'data')
    )
    def load_layout(
        dropdown_container,
        memory
    ):
        dropdown_items = {f'{ids_addon.DROPDOWN.MENU}_{i+1}': item for i, item in enumerate(
            [str(v) for v in dropdown_list]) if item not in memory}
        return [dbc.DropdownMenuItem(
            dropdown_value,
            id={"index": dropdown_value, "type": ids_addon.DROPDOWN.MENU},
            # id=dropdown_key,
            style={'width': '100%'},
            n_clicks=0,
        ) for (dropdown_key, dropdown_value) in dropdown_items.items()
        ], dropdown_items


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.


    @callback(
        Output(ids_addon.DROPDOWN.MENU, 'label'),
        Input({"index": ALL, "type": ids_addon.DROPDOWN.MENU}, 'n_clicks'),
        State(ids_addon.MEMORY, 'data'),
        State(ids_addon.DROPDOWN.ITEMS, 'data'),
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
                triggered_index = ids_addon.DROPDOWN.MENU + \
                    '_' + json.loads(dropdown_item)['index']
                if triggered_index in dropdown_items.keys():
                    return dropdown_items.get(triggered_index, '')
                else:
                    raise PreventUpdate


# callback for add button.

    @ callback(
        [
            Output(ids_addon.NEW_ITEMS, 'children', allow_duplicate=True),
            Output(ids_addon.INPUT, 'value'),
            Output(ids_addon.DROPDOWN.MENU, 'label', allow_duplicate=True),
            Output(ids_addon.MEMORY, 'data', allow_duplicate=True),
        ],
        Input(ids_addon.ADD, 'n_clicks'),
        [
            State(ids_addon.DROPDOWN.MENU, 'label'),
            State(ids_addon.INPUT, 'value'),
            State(ids_addon.MEMORY, 'data'),
            State(ids_addon.DROPDOWN.ITEMS, 'data'),
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
                            "type": ids_addon.OUTPUT
                        },
                        style={"display": "inline", "margin": "10px"},
                    ),
                ],
            )
        if (current_label and current_label != dropdown_label) and current_input:
            patched_item.append(new_checklist_item())
        return patched_item, "", dropdown_label, memory

    @ callback(
        Output({"index": MATCH, "type": ids_addon.OUTPUT}, "style"),
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
        Output(ids_addon.NEW_ITEMS, 'children', allow_duplicate=True),
        Output(ids_addon.MEMORY, 'data', allow_duplicate=True),
        Input(ids_addon.DELETE, 'n_clicks'),
        State({'index': ALL, 'type': 'done'}, 'value'),
        State(ids_addon.MEMORY, 'data'),
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


# py -m Amort.test.Addon
if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[
        dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
    app.layout = html.Div(
        [
            html.H1('test of addon function'),
            html.Hr(),
            addon(
                dropdown_list=[1, 2, 3],
                placeholder='Enter a number',
                dropdown_label='Select a number',
            )
        ]
    )

    app.run_server(debug=True)

# ClassName設定layout:
# https://dashcheatsheet.pythonanywhere.com/
