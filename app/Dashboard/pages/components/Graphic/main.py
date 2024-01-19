"""Build a graph for the loan"""
from itertools import accumulate
from dash import Dash, dcc, callback, Output, Input, State, ALL, callback_context, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
import dash_mantine_components as dmc
from plotly.subplots import make_subplots

import sys
sys.path.append('./')

from app.Dashboard.assets.ids import GRAPH, LOAN
from app.Loan import df_schema, merge_sublist

# TODO:
# 1. add a button to download the graph as a svg file
# 2. adjust the size of the pie charts
# 3. add subgroup for subsidy
# 

def graph():
    """Build the graph"""
    layout = html.Div(
        [
            dmc.LoadingOverlay(    
                html.Div(
                    id= 'information-dashboard',
                    children= [],
                    style= {
                        'display': 'flex',
                        'width': '100%',
                        'height': '100%',
                        'background-color': 'white',
                        'border-radius': '5px',
                        'border': '1px solid #ccc',
                        'box-shadow': '0 0 5px #ccc',
                    },
                ),
                loaderProps={"variant": "dots",
                             "color": "blue", 
                             "size": "lg",
                             'is_loading': True,
                             },
                transitionDuration= 0.5,
                style= {
                    'height': '40%',
                },
            ),
            dmc.Space(h=10),
            html.Div(
                [
                    dmc.Group(
                        [
                            dmc.Menu(
                                [
                                    dmc.MenuTarget(
                                        dmc.Button(
                                            id='menu-target',
                                            children=df_schema.level_2.PAYMENT,
                                            variant="gradient",
                                            gradient={"from": "indigo", "to": "cyan"},
                                            loading={'loading_type': 'overlay'},
                                            loaderPosition='center',
                                            loaderProps={"variant": "dots",
                                                         "color": "white", "size": "sm"},
                                        ),
                                    ),
                                    dmc.MenuDropdown(
                                        [],
                                        id='menu-dropdown',
                                    ),
                                ],
                                id=GRAPH.DROPDOWN.MENU,
                            ),
                            dmc.SegmentedControl(
                                id=GRAPH.ACCUMULATION,
                                value="regular",
                                data=[
                                    {"value": "regular", "label": "Regular"},
                                    {"value": "cumulative", "label": "Cumulative"},
                                ],
                                size='sm',
                                style={
                                    'background-color': "rgba(0, 62, 143, 0.29)",
                                    'box-shadow': '0 0 5px #ccc',
                                },
                            ),
                        ],
                        spacing=10,
                        position='left',
                    ),
                    dmc.Button(
                        'spreadsheet', 
                        id= 'detailed-table', 
                        variant="gradient",
                        size='sm',
                        gradient={"from": "indigo", "to": "cyan"},
                        leftIcon=DashIconify(icon="fluent:database-plug-connected-20-filled"),
                    )
                ],
                style={
                    'display': 'flex',
                    'justify-content': 'space-between',
                    'align-items': 'center',
                    'width': '100%',
                    'height': 'auto',
                }
            ),
            dmc.Space(h=10),
            dmc.LoadingOverlay(
                html.Div(
                    children= [],
                    id= GRAPH.LINE,
                ),
                loaderProps={"variant": "dots",
                             "color": "blue", 
                             "size": "lg",
                             'is_loading': True,
                             },
                transitionDuration= 0.5,
                style={
                    'height': 460,
                    'border-radius': '5px',
                    'border': '1px solid #ccc',
                    'background-color': 'white',
                    'box-shadow': '0 0 5px #ccc',
                },
            ),
        ],
        style={
            'width': '100%',
            'height': '95dvh',
            'margin-left': 'auto',
            'margin-right': 'auto',
        },
        className= 'custom-scrollbar',
    )

#1 options for dropdown menu of the main graph
    @callback(
        Output('menu-dropdown', 'children'),
        Output('menu-dropdown', 'style'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input('menu-target', 'children'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
    )
    def update_toggle_items(
        accum,
        label,
        data,
    ):
        data = data['data']
        level_0 = {c[0] for c in data['columns']}
        if df_schema.level_0.TOTAL in level_0:
            return [], {'display': 'none'}
        else:
            method_for_original_mortgate = [
                df_schema.level_2.PAYMENT,
                df_schema.level_2.PRINCIPAL,
                df_schema.level_2.INTEREST,
                df_schema.level_2.RESIDUAL,
            ]
            if accum and accum == 'cumulative':
                method_for_original_mortgate = [
                    v for v in method_for_original_mortgate if v != df_schema.level_2.RESIDUAL]
            dropdown = [
                dmc.MenuItem(
                    column,
                    id={
                        'index': column,
                        'type': GRAPH.DROPDOWN.ITEM
                    },
                ) for column in method_for_original_mortgate if column != label
            ]  # avoid duplicate label
            return dropdown, {'display': 'block'}

#2 update the main graph
    @callback(
        Output(GRAPH.LINE, 'children'),
        Output('menu-target', 'children'),
        Output('menu-target', 'rightIcon'),
        Output('menu-target', 'loading'),
        Output('menu-target', 'gradient'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        Input({'index': ALL, 'type': GRAPH.DROPDOWN.ITEM}, 'n_clicks'),
        State('menu-target', 'children'),
    )
    def update_graph(
        accum,
        data,
        _,
        label,
    ):
        ctx = callback_context
        data = data['data']
        
        if isinstance(ctx.triggered_id, dict):
            chosen_figure = ctx.triggered_id['index']
        else:
            # type: ignore
            if df_schema.level_0.TOTAL not in [col[0] for col in data['columns']]:
                if accum == 'cumulative':
                    if label == df_schema.level_2.RESIDUAL:
                        chosen_figure = df_schema.level_2.PAYMENT
                    else:
                        chosen_figure = label
                else:
                    chosen_figure = (
                        label if label != df_schema.level_0.TOTAL else df_schema.level_2.PAYMENT)
            else:
                chosen_figure = df_schema.level_0.TOTAL # 總計
        
        ns, cols = zip(*[(n, col) for n, col in enumerate(data['columns']) if chosen_figure in col])
        x_axis_value = data['index'][1:-1]
        
        # construct the data frame for the graph
        data_frame_for_loan_timeSeries= {
            'Time': [],
            'Amount': [],
            'methods': [],
        }

        for n, col in zip(ns, cols): # n: index of the column; col: column name
            dff = [data[n] for data in data['data'][1:-1]]
            method = (" + ".join([co for co in col if co != chosen_figure]) if len(col) > 2 else col[0])

            if accum == 'cumulative':
                dff = [*accumulate(dff)]
            dff = [*map(lambda x: f"{round(x):,}", dff)]
            
            data_frame_for_loan_timeSeries['Time'].extend(x_axis_value)
            data_frame_for_loan_timeSeries['Amount'].extend(dff)
            data_frame_for_loan_timeSeries['methods'].extend([method] * len(x_axis_value))
            
        fig = px.line(
            data_frame_for_loan_timeSeries,
            x= "Time", 
            y= "Amount", 
            color="methods", 
            title='<b>Life of Loan</b>', 
            log_y= True,
            line_shape="spline",
            render_mode="svg",
            hover_name= "methods",
            template="plotly_white", # ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
            color_discrete_map= {
                    df_schema.level_1.ETP: '#0C82DF',
                    df_schema.level_1.EPP: '#F7DC6F',
            },
        )
        fig.update_layout(showlegend= False)

        return dcc.Graph(
            figure= fig,
            # id=GRAPH.LINE,
            hoverData= {'points': [{'x': '0', 'hovertext': 'ETP'}]},
            config={
                'displayModeBar': False,
                'responsive': True,
                'doubleClick': 'reset+autosize',
                'toImageButtonOptions': {
                    'format': 'svg',
                    'filename': 'custom_image',
                    'scale': 1,
                },
            },
            style={
                'width': '100%',
                'height': '100%',
            },
        ), chosen_figure, (DashIconify(icon="raphael:arrowdown") if chosen_figure != df_schema.level_0.TOTAL else None), False, ({"from": "teal", "to": "blue", "deg": 60} if chosen_figure == df_schema.level_0.TOTAL else {"from": "indigo", "to": "cyan"})

    @callback(
        Output('information-dashboard', 'children'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
    )
    def update_info(
        memory, 
        ):
        if memory:
            memory = memory['data']

            demostrated_items= [df_schema.level_2.PAYMENT, df_schema.level_2.PRINCIPAL, df_schema.level_2.INTEREST]
            pie_data = {}
            payment= {}
            for key, value in {k: round(v) for k, v in zip(map(lambda x: tuple(x), memory['columns']), memory['data'][-1]) if k[-1] in demostrated_items}.items():
                if key[-2] not in pie_data.keys():
                    pie_data.update({key[-2]: {'labels': [], 'values': [], 'names': []}}) # initialize the dictionary
                if key[-1] == df_schema.level_2.PAYMENT:
                    if key[-2] not in payment.keys():
                        payment.update({key[-2]: {'labels': [], 'values': [], 'names': []}}) # initialize the dictionary
                    payment[key[-2]]['labels'].append(key[-1])
                    payment[key[-2]]['values'].append(value)
                    payment[key[-2]]['names'].append((key[0] if key[0] != key[-2] else None))
                else:
                    pie_data[key[-2]]['labels'].append(key[-1])
                    pie_data[key[-2]]['values'].append(value)
                    pie_data[key[-2]]['names'].append((key[0] if key[0] != key[-2] else None))

            fig = None
            fig_main= None
            fig_sub= None
            for col, method in enumerate(pie_data.keys()):
                if len(pie_data[method]['names']) == 2:
                    if not fig:
                        fig = make_subplots(rows=1, cols=len(pie_data.keys()), specs=[[{'type':'domain'}, {'type':'domain'}]])
                    fig.add_trace(
                        go.Pie(
                            labels= pie_data[method]['labels'],
                            values= pie_data[method]['values'],
                            title= f"""<b>{method}</b><br>{round(payment[method]['values'][0] // len(memory['data'][1:-1])): ,}/月""",
                            name= "",
                            titlefont= dict(size= 20, color= 'dark grey'),
                            marker= dict(colors= px.colors.qualitative.D3),
                            textfont= dict(size= 15),
                            textinfo= 'percent',
                            textposition= 'inside',
                            hoverinfo= 'label+value',
                            hovertemplate= '%{label}: %{value:,.0f}',
                            showlegend= False,
                            hole= .7,

                        ),
                            1, 
                            col + 1,
                    )
                    fig.update_traces(
                        hole= .7,
                        hoverinfo="label+percent+name",
                    )
                    fig.update_layout(
                        title_text="<b>Total Payment</b>", 
                        title_font_size= 20,
                        title_x= 0.5,
                        margin=dict(l=20, r=20, t=60, b=30),
                    )

                else:
                    for name in pie_data[method]['names']:
                        if name == df_schema.level_0.ORIGINAL:
                            if not fig_main:
                                fig_main = make_subplots(rows=1, cols=len(pie_data.keys()), specs=[[{'type':'domain'}, {'type':'domain'}]])
                            fig_main.add_trace(
                                go.Pie(
                                    labels= pie_data[method]['labels'],
                                    values= pie_data[method]['values'],
                                    title= f"""<b>{method}</b><br>{round([v for c, v in zip(zip(payment[method]['labels'], payment[method]['names']), payment[method]['values'])  if c[0] == df_schema.level_2.PAYMENT and c[1] == name][0] // len(memory['data'][1:-1])): ,}/月""",
                                    name= "",
                                    titlefont= dict(size= 20, color= 'dark grey'),
                                    marker= dict(colors= px.colors.qualitative.D3),
                                    textfont= dict(size= 15),
                                    textinfo= 'percent',
                                    textposition= 'inside',
                                    hoverinfo= 'label+value',
                                    hovertemplate= '%{label}: %{value:,.0f}',
                                    showlegend= False,
                                ),
                                    1, 
                                    col + 1,
                            )
                            fig_main.update_traces(
                                hole= .7,
                                hoverinfo="label+percent+name",
                            )
                            fig_main.update_layout(
                                title_text="<b>Original Loan</b>", 
                                title_font_size= 20,
                                title_x= 0.5,
                                margin=dict(l=20, r=20, t=60, b=30),
                            )
                        elif name == df_schema.level_0.SUBSIDY:
                            if not fig_sub:
                                fig_sub = make_subplots(rows=1, cols=len(pie_data.keys()), specs=[[{'type':'domain'}, {'type':'domain'}]])
                            fig_sub.add_trace(
                                go.Pie(
                                    labels= pie_data[method]['labels'],
                                    values= pie_data[method]['values'],
                                    title= f"""<b>{method}</b><br>{round([v for c, v in zip(zip(payment[method]['labels'], payment[method]['names']), payment[method]['values']) if c[0] == df_schema.level_2.PAYMENT and c[1] == name][0] // len([v for v in map(lambda x: [x[n] > 0 for n, c in enumerate(memory['columns']) if c[-3] == name and c[-2] == method and c[-1] == df_schema.level_2.PAYMENT][0], memory['data'][1:-1]) if v])): ,}/月""",
                                    name= "",
                                    titlefont= dict(size= 20, color= 'dark grey'),
                                    marker= dict(colors= px.colors.carto.Antique),
                                    textfont= dict(size= 15),
                                    textinfo= 'percent',
                                    textposition= 'inside',
                                    hoverinfo= 'label+value',
                                    hovertemplate= '%{label}: %{value:,.0f}',
                                    showlegend= False,
                                ),
                                    1, 
                                    col + 1,
                            )
                            fig_sub.update_traces(
                                hole= .7,
                                hoverinfo="label+percent+name",
                            )
                            fig_sub.update_layout(
                                title_text="<b>Subsidy Loan</b>", 
                                title_font_size= 20,
                                title_x= 0.5,
                                margin=dict(l=20, r=20, t=80, b=60),
                            )
            return [
                dcc.Graph(
                    figure= fig,
                    style={
                        'background-color': 'rgba(0, 0, 0, 0)',
                        'width': '100%',
                        'height': '100%',
                    },
                    config={
                        'displayModeBar': False,
                        'doubleClick': 'reset+autosize',
                        'autosizable': True,
                        'editable': False,
                        'scrollZoom': False,
                        'staticPlot': False,
                        'responsive': True,
                    }
                ) for fig in [f for f in[fig, fig_main, fig_sub] if f]
            ]
        else:
            raise PreventUpdate

       
    return layout

# python app/Dashboard/pages/components/Graphic/main.py
# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    import dash_bootstrap_components as dbc
    from app.Dashboard.pages.components.Controls.panels import panel
    app = Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.LUMEN, 
            dbc.icons.BOOTSTRAP,
            "app/Dashboard/assets/style.css",
            ],
        suppress_callback_exceptions=True,
    )

    app.layout = html.Div(
        [
            html.Div(
                [
                    panel.front(),
                    panel._advancedoptions()
                ]
            ),
            panel.register(),
            graph()
        ],
        style= {
            'display': 'flex',
        },
        className= 'custom-scrollbar',
    )
    app.run_server(
        # debug=True
        )
