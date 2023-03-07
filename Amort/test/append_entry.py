# 放棄以動態新增區塊的方式，改以單一區塊新增及刪除資料。
# 里程碑:
# (1) 運用InputGroup合併dropdown, input及增加減少按鈕。
# (2) 以callback的方式更新dropdown的label以及在新增區塊時動態更新dropdown list的選項。
# (3) 運用dcc.Store儲存資料。
# (4) 運用callback_context來判斷觸發callback的元件。
# (5) 製作tracer function捕捉背景layout特定component。
# (6) 運用全域賦值global。
# 未能克服：
# 未能擷取刪除的是第幾個產生的區塊，致難建立刪除功能的系統性調整架構。包括：
# 1. 刪除區塊後，無法控制前一個區塊list的值
# 2. 刪除區塊後，無法同步刪除memory對應的資料
# 3. 刪除區塊後，無法對應刪除dropdown_items的資料
from calendar import c
from distutils.log import debug
from pickletools import StackObject
from re import S
from subprocess import call
from traceback import print_tb
from dash import Dash, dcc, html, Input, Output, State, callback, callback_context, ALL, MATCH
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import json
# TODO:
# 2023/02/05
# [X] store the result
# 2023/02/08
# 01. [X] avoid duplicate elements in the timepoint list -> construct a dict which contains timepoint as the key and interest as the value.
# 02. [X] create delete function
# 2023/02/09
# [X] Delete the timepoints which interest rate has been set from timepoint items.
# 2023/02/10
# [X] use callback to update the dropdownmenu label.
# 2023/02/15
# [X] can't not trigger while entering in last container

# 2023/03/05
# [X]刪除第一個發生錯誤
# A nonexistent object was used in an `Input` of a Dash callback. The id of this object is `dropdown-list-subsidy-1` and the property is `n_clicks`.
# The string ids in the current layout are: [cache, memory, out-container, dropdown-menu, dropdown-list-subsidy-2, dropdown-list-subsidy-3, out-timepoint, out-interest]
# [X]memory最後一個即時儲存

# 2023/03/06
# 最後一個都會錯誤，試試看調正dropdown_items 或len(children)== len(dropdown_list)


class ids:
    ADD = 'add-button'
    MINUS = 'minus-button'
    MEMORY = 'memory'
    CACHE = 'cache'

    class INPUT:
        INTEREST = 'input-interest'
        TYPE = 'type-input'

    class DROPDOWN:
        MENU = 'dropdown-menu'
        LIST = 'dropdown-list'
        ITEMS = 'dropdown-items'

    class OUTPUT:
        CONTAINER = 'out-container'
        TIMEPOINT = 'out-timepoint'
        INTEREST = 'out-interest'


def ARR_addons(
        type: str,  # [prepay, subsidy]
        dropdown_list: list,
        dropdown_label: str,
        input_placeholder: str
) -> html.Div:

    dropdown_list = [str(element) for element in dropdown_list]
    def dropdown_key(key): return ids.DROPDOWN.LIST + \
        "-" + type + "-" + str(key)
    global dropdown_items
    dropdown_items = {dropdown_key(item): item for item in dropdown_list}
    def paired_id(type, index): return {'type': type, 'index': index}

    def tracer(children, component_id, property=None, exclude=None):
        # Mapping properties in the component with designated id.
        # Period: 2023/02/17-02/18, 2023/03/01-03/05
        result = [
            [
                [
                    [
                        # In case of Matching Pattern being used.
                        (chil['props']['id'] if chil['props']
                         ['id']['type'] == component_id else None)
                        if 'type' in chil['props']['id']
                        else (chil if chil['props']['id'] == component_id else None)
                        for chil in child['props']['children']
                        if isinstance(chil, dict) and 'id' in chil['props']
                    ]
                    if isinstance(child, dict) and (child['props']['id'] != component_id if 'id' in child['props'] and 'children' in child['props'] else 'children' in child['props'])
                    else (child['props'][property] if property in child['props'] else None)
                    # Inner layer #3
                    for child in childr['props']['children']
                ]
                if isinstance(childr, dict) and (childr['props']['id'] != component_id if 'id' in childr['props'] and 'children' in childr['props'] else 'children' in childr['props'])
                else (childr['props'][property] if property in childr['props'] else None)
                for childr in childre['props']['children']  # Inner layer #2
            ]
            for childre in children  # Outer layer
        ]
        # Extract desired output from nested list.
        out = []
        for res in result:
            for re in res:
                if [] not in re:
                    for r in re:
                        if r:
                            if isinstance(r, list):
                                for rr in r:
                                    if rr and rr != exclude:
                                        out.append(rr)
                            else:
                                if r != exclude:
                                    out.append(r)
        return out

    # Initial layout
    layout = html.Div(
        [
            dcc.Store(id=ids.CACHE),
            # {'store_type: ["", "local", "session"]}
            dcc.Store(id=ids.MEMORY, data={}),
            html.Div(
                children=[],
                id=ids.OUTPUT.CONTAINER
            ),
        ]
    )

# Callback functions with order.
# 1. Create new blocks for addons functions.
# ------------------------------------------
# Excuted after the block is created.
# 2. Connect the selected dropdown list element with correspond number, and save it as a cache.
# 3. Update the cache to the dropdown label.
# 4. Save the results of label and input to the memory.
# ------------------------------------------
# 5. Show the results of label and input.

# 1 Create new blocks for addons functions.
    @callback(
        Output(ids.OUTPUT.CONTAINER, 'children'),
        Input(paired_id(ids.ADD, ALL), 'n_clicks'),
        Input(paired_id(ids.MINUS, ALL), 'n_clicks'),
        State(ids.OUTPUT.CONTAINER, 'children'),
    )
    def update_combination(
        n_clicks,
        delete,
        children,
    ) -> html.Div:
        if not n_clicks:
            n_clicks = 0
        else:
            n_clicks = [0 if n == None else n for n in n_clicks][-1]

        def new_element(existance):
            return html.Div(
                [  # children 1
                    dbc.InputGroup(
                        [  # children 1-1
                            dbc.DropdownMenu(
                                [  # children 1-1-1
                                    dbc.DropdownMenuItem(
                                        dropdown_value,
                                        id=dropdown_key,
                                        style={'width': '200px'},
                                        n_clicks=0,
                                    ) for (dropdown_key, dropdown_value) in {key: value for (key, value) in dropdown_items.items()}.items()
                                ],
                                label=dropdown_label,
                                id=ids.DROPDOWN.MENU,
                                style={'width': "100%"}
                            ),
                            dbc.Input(
                                id=paired_id(
                                    ids.INPUT.INTEREST, n_clicks),
                                placeholder=(
                                    input_placeholder if input_placeholder != None else ""),
                            ),
                            html.Div(
                                [  # children 1-1-2
                                    dbc.Button(
                                        className="bi-plus-lg rounded-circle",
                                        # outline= True,
                                        color="primary",
                                        id=paired_id(
                                            ids.ADD, n_clicks),
                                    ),
                                    dbc.Button(
                                        className="bi-trash rounded-circle",
                                        # outline= True,
                                        color="primary",
                                        id=paired_id(
                                            ids.MINUS, n_clicks),
                                    ),
                                ],
                                className="gx-2 gx-xl-5 h-50 d-inline-block m-2",
                            )
                        ],
                        class_name="mb-3"
                    ),
                    html.Div(
                        [
                            html.Ul(
                                children=[],
                                id=ids.OUTPUT.TIMEPOINT
                            ),
                            html.Ul(
                                children=[],
                                id=ids.OUTPUT.INTEREST,
                            )
                        ]
                    )
                ],
                id={'index': n_clicks},
            )

        if len(children) == 0:
            # renew the variable along with pages being refreshed.
            global existance
            existance = []
            children.append(new_element(dropdown_items))
        else:
            existance = tracer(children, ids.DROPDOWN.MENU,
                               'label', exclude=dropdown_label)
            if ctx_id := callback_context.triggered_id:
                if ctx_id['type'] == ids.ADD:
                    # Set an upper limit to the number of dropdowns.
                    if len(children) < len(dropdown_list):
                        for to_delete in [v for v in existance if v in dropdown_items.values()]:
                            dropdown_items.pop(dropdown_key(to_delete))
                        children.append(new_element(dropdown_items))

                if ctx_id['type'] == ids.MINUS:
                    if len(children) > 1:
                        children.pop(
                            [n for (n, de) in enumerate(delete) if de != None][0])
                        # Consider the case that either dropdown or input is empty.
                        global retrive
                        retrive = tracer(
                            children, ids.DROPDOWN.MENU, 'label', exclude=dropdown_label)
                        for to_retrive in [v for v in retrive if v not in dropdown_items.values()]:
                            dropdown_items[dropdown_key(
                                to_retrive)] = to_retrive
                    else:
                        pass
        return children

# 2 Connect the selected dropdown list element with correspond number, and save it as a cache.
    @callback(
        Output(ids.CACHE, 'data'),
        State(ids.OUTPUT.CONTAINER, 'children'),
        State(ids.CACHE, 'data'),
        [Input(dropdown_key, 'n_clicks') for dropdown_key in dropdown_items],
        prevent_initial_call=True,
    )
    def corresponding_value(children, cache, *args):
        ctx = callback_context
        if len(ctx.triggered) > 1:
            button_id = []
        else:
            button_id = ctx.triggered_id

        if button_id:
            if button_id in dropdown_items:
                return str(dropdown_items[button_id])


# 3 Update the label of the dropdown menu.

    @callback(
        Output(ids.DROPDOWN.MENU, 'label'),
        Input(ids.CACHE, 'data'),
        State(ids.OUTPUT.CONTAINER, 'children'),
        State(paired_id(ids.MINUS, ALL), 'n_clicks'),
        prevent_initial_call=True
    )
    def update_label(cache, children, _):
        if len(children) < len(dropdown_list):
            print('delete: ', tracer(children, ids.MINUS, 'index'))
            if cache:
                return cache
            else:
                return dropdown_label
        else:
            if len(existance) == len(dropdown_list):
                return existance[-1]
            else:
                return [v for v in dropdown_list if v not in existance][0]


# 4 Update the timepoint list.

    @callback(
        Output(ids.MEMORY, 'data'),
        State(ids.MEMORY, 'data'),
        Input(paired_id(ids.INPUT.INTEREST, ALL), 'value'),
        Input(ids.DROPDOWN.MENU, 'label'),
        Input(paired_id(ids.MINUS, ALL), 'n_clicks'),
        prevent_initial_call=True
    )
    def update_result(
        memory,
        input,
        label,
        _
    ):
        # print('label: ', label)
        # print('input: ', input)
        if label and label != dropdown_label:
            try:  # prevent wrong data type.'
                memory[label] = float(input[-1])
            except:
                memory[label] = None
        if ctx_id := callback_context.triggered_id:
            # print('ctx_id: ', ctx_id)
            if isinstance(ctx_id, dict):
                if ctx_id['type'] == ids.MINUS and len(memory) > 1:
                    # print(str([v for v in memory if int(v) not in retrive][-1]))
                    del memory[str(
                        [v for v in memory if v not in retrive][-1])]
        return memory

# 5 Update the appearence of the timepoint list.
    @callback(
        Output(ids.OUTPUT.TIMEPOINT, 'children'),
        Output(ids.OUTPUT.INTEREST, 'children'),
        Input(ids.MEMORY, 'data'),
        prevent_initial_call=True
    )
    def udpate_appearence(memory):
        # print('memory: ', memory)
        return html.Li([*memory]), html.Li([*memory.values()])
    return layout


# py -m Amort.test.append_entry
if __name__ == "__main__":
    from dash import Dash
    app = Dash(__name__, external_stylesheets=[
        dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
    app.layout = html.Div(
        ARR_addons(
            type='subsidy',
            dropdown_list=[1, 2, 3],
            dropdown_label="TimePoint",
            input_placeholder="Type some number"
        )
    )
    app.run_server(debug=True)
