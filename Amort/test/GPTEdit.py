import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.Div("Dash Multi-Input To-Do List"),
        dcc.Input(id="new-item-input", placeholder="Enter a task"),
        dbc.DropdownMenu(
            id="category-dropdown",
            label="Select a category",
            children=[
                dbc.DropdownMenuItem("Work", id="work"),
                dbc.DropdownMenuItem("Personal", id="personal"),
                dbc.DropdownMenuItem("Shopping", id="shopping"),
            ],
        ),
        html.Button("Add", id="add-btn"),
        html.Button("Clear Done", id="clear-done-btn"),
        html.Div(id="list-container-div"),
        html.Div(id="totals-div"),
        html.Div(id="selected-category", style={"display": "none"}),
    ]
)

# Callback to handle the selected category from the DropdownMenu


@app.callback(
    Output("selected-category", "children"),
    Input("work", "n_clicks"),
    Input("personal", "n_clicks"),
    Input("shopping", "n_clicks"),
    prevent_initial_call=True,
)
def update_selected_category(work, personal, shopping):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        category = ctx.triggered[0]["prop_id"].split(".")[0]
        return category

# Callback to add a new item to the list


@app.callback(
    Output("list-container-div", "children", allow_duplicate=True),
    Output("new-item-input", "value", allow_duplicate=True),
    Output("selected-category", "children", allow_duplicate=True),
    Input("add-btn", "n_clicks"),
    State("new-item-input", "value"),
    State("selected-category", "children"),
    State("list-container-div", "children"),
    prevent_initial_call=True

)
def add_item(
    button_clicked,
    task_value,
    category_value,
    current_list
):
    if not task_value or not category_value:
        return dash.no_update, dash.no_update, dash.no_update

    def new_checklist_item():
        return html.Div(
            [
                dcc.Checklist(
                    options=[{"label": "", "value": "done"}],
                    id={"index": button_clicked, "type": "done"},
                    style={"display": "inline"},
                    labelStyle={"display": "inline"},
                ),
                html.Div(
                    [f"{task_value} ({category_value.capitalize()})"],
                    id={"index": button_clicked, "type": "output-str"},
                    style={"display": "inline", "margin": "10px"},
                ),
            ]
        )

    if current_list is None:
        current_list = []

    updated_list = current_list + [new_checklist_item()]
    return updated_list, "", None


# Other callback functions remain the same


if __name__ == "__main__":
    app.run_server(debug=True)
