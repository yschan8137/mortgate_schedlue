import re
from dash import Dash, dcc, html, Input, Output, State, callback, callback_context, ALL, MATCH, Patch
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


class ids:
    NEW_ITEMS = 'new-items'
    ADD = 'addon function'
    DELETE = 'delete function'
    MEMORY = 'memory'
    INPUT = 'input'
    OUTPUT = 'output'

    class DROPDOWN:
        MENU = 'dropdown-menu'


def addon(
        dropdown_list: list,
        dropdown_label: str,
        placeholder: str,
):
    dropdown_list = [str(element) for element in dropdown_list]

    # global dropdown_items
    dropdown_items = {f'{ids.DROPDOWN.MENU}_{i}': item for i,
                      item in enumerate([str(v) for v in dropdown_list])}

    layout = html.Div(
        [
            dcc.Store(id=ids.MEMORY, data={}),
            html.Div(id=ids.NEW_ITEMS),
            html.Div(
                [
                    dbc.DropdownMenu(
                        [],
                        label=dropdown_label,
                        id=ids.DROPDOWN.MENU,
                        style={'width': "100%"}
                    ),
                    dcc.Input(id=ids.INPUT, type='number',
                              placeholder=placeholder),
                    dbc.Button(
                        id=ids.ADD,
                        color="primary",
                        children="Add"
                    ),
                    dbc.Button(
                        id=ids.DELETE,
                        color="danger",
                        children="Delete"
                    )
                ],
                style={'display': 'inline-flex'}
            ),
        ]
    )

# load for initial layout
    @callback(
        Output(ids.DROPDOWN.MENU, 'children'),
        Input(ids.DROPDOWN.MENU, 'children'),
        Input(ids.MEMORY, 'data')
    )
    def load_layout(
        dropdown_container,
        memory
    ):
        global dropdown_items
        dropdown_items = {f'{ids.DROPDOWN.MENU}_{i}': item for i, item in enumerate([str(v) for v in dropdown_list]) if item not in memory}
        return [dbc.DropdownMenuItem(
            dropdown_value,
            id={"index": dropdown_value, "type": ids.DROPDOWN.MENU},
            # id=dropdown_key,
            style={'width': '100%'},
            n_clicks=0,
        ) for (dropdown_key, dropdown_value) in dropdown_items.items()
        ]


# update the label of the dbc.DropdownMenu to selected children in dbc.DropdownMenuItem.

    @callback(
        Output(ids.DROPDOWN.MENU, 'label'),
        Input({"index": MATCH}, 'n_clicks'),
        Input(ids.DROPDOWN.MENU, 'children'),
        # [Input(dropdown_key, 'n_clicks')
        #  for dropdown_key in dropdown_items.keys()],
        prevent_initial_call=True
    )
    def update_dropdown_label(n_clicks, menu):
        ctx = callback_context
        print('triggered: ', ctx.triggered)
        if not ctx.triggered:
            raise PreventUpdate
        else:
            dropdown_key = ctx.triggered[0]['prop_id'].split('.')[0]
            if dropdown_key in dropdown_items.keys():
                return dropdown_items.get(dropdown_key, '')
            else:
                raise PreventUpdate


# callback for add button.


    @ callback(
        [
            Output(ids.NEW_ITEMS, 'children', allow_duplicate=True),
            Output(ids.INPUT, 'value'),
            Output(ids.DROPDOWN.MENU, 'label', allow_duplicate=True),
            Output(ids.MEMORY, 'data', allow_duplicate=True),
        ],
        Input(ids.ADD, 'n_clicks'),
        [
            State(ids.DROPDOWN.MENU, 'label'),
            State(ids.INPUT, 'value'),
            State(ids.MEMORY, 'data'),
        ],
        prevent_initial_call=True
    )
    def add_items(
        _,
        current_label,
        current_input,
        memory,
    ):
        global dropdown_items
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
                            "type": ids.OUTPUT
                        },
                        style={"display": "inline", "margin": "10px"},
                    ),
                ],
            )
        # to_delete = []
        # for k, v in dropdown_items.items():
            # if v in memory:
            # to_delete.append(k)
        # for k in to_delete:
            # del dropdown_items[k]
        # print('memory:', memory)
        if (current_label and current_label != dropdown_label) and current_input:
            patched_item.append(new_checklist_item())
        return patched_item, "", dropdown_label, memory

    @ callback(
        Output({"index": MATCH, "type": ids.OUTPUT}, "style"),
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
    @ callback(
        Output(ids.NEW_ITEMS, 'children', allow_duplicate=True),
        Input(ids.DELETE, 'n_clicks'),
        State({'index': ALL, 'type': 'done'}, 'value'),
        prevent_initial_call=True
    )
    def delete_items(_, state):
        patched_item = Patch()
        values_to_remove = []
        for i, value in enumerate(state):
            if value:
                values_to_remove.insert(0, i)
        for i in values_to_remove:
            del patched_item[i]
        return patched_item

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
