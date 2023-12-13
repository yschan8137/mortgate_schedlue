"""Build a graph for the loan"""
from itertools import accumulate, chain
from dash import Dash, dcc, callback, Output, Input, State, ALL, callback_context, no_update
from dash_iconify import DashIconify
import plotly.express as px
# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import time

from app.Dashboard.assets.ids import GRAPH, LOAN
from app.Loan import df_schema


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
)


def graph():
    """Build the graph"""
    layout = dmc.Container(
        [
            dmc.Group(
                [
                    dmc.Card(
                        [
                            dmc.Title('Test text', order=1),
                            dmc.Text(
                                children='',
                                id='right-text-board',
                                color='white',
                                size=60,
                                style={
                                    'width': 60,
                                }
                            )
                        ],
                        shadow='sm',
                        radius='md',
                        withBorder=True,
                        style={
                            'width': 300,
                            'height': 150,
                            'top': 5,
                            'background-color': '#AEB6BF',
                        }
                    ),
                    dmc.Card(
                        [
                            dmc.Title('Test text', order=1),
                            dmc.Group(
                                [
                                    dmc.Text(
                                        children='20',
                                        id='left-text-board',
                                        color='white',
                                        size=60,
                                        style={
                                            'width': 60,
                                        }
                                    ),
                                    DashIconify(
                                        icon="carbon:percentage",
                                        color='white',
                                        width=60,
                                    ),
                                ],
                                position='center',
                            )
                        ],
                        shadow='sm',
                        radius='md',
                        withBorder=True,
                        style={
                            'width': 300,
                            'height': 150,
                            'top': 5,
                            'background-color': '#AEB6BF',
                            'shadow-direction': 'top-left',
                        }
                    ),
                ],
                grow=True,
            ),
            dmc.Space(h=30),
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
                                    style={
                                        'width': '110px',
                                    },
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
                            'border': '1px solid #ccc',
                            'border-radius': '5px',
                        },
                    ),
                ],
                spacing=10,
                position='left',
                style={
                    'width': '100%',
                }
            ),
            dmc.LoadingOverlay(
                dcc.Graph(
                    id=GRAPH.LINE,
                    config={
                        'displayModeBar': False,
                        'responsive': True,
                        'doubleClick': 'reset+autosize',
                        'toImageButtonOptions': {
                            'format': 'svg',
                            'filename': 'custom_image',
                            'height': 600,
                            'width': 1000,
                            'scale': 1,
                        },

                    },
                    style={
                        'width': '100%',
                        'height': 600,
                        # make the graph object to be at the center of the container
                        'margin-left': 'auto',
                        'margin-right': 'auto',


                    },
                    selectedData={'points': [{'curveNumber': 0, 'pointNumber': 0}]},
                    figure= px.line(
                        {
                            'Time': [],
                            'Amount': [],
                            'methods': [],
                        }, 
                        x= "Time", 
                        y="Amount", 
                        color="methods", 
                        title="Life of Loan", 
                        width=1000, 
                        height=600,
                        log_y= True,
                        line_shape="spline",
                        render_mode="svg",
                        hover_name="methods",
                        template="plotly_white",
                    )
                ),
                id= 'loading-overlay',
                loaderProps={"variant": "oval",
                             "color": "blue", 
                             "size": "lg",
                             'is_loading': True,
                             },
                transitionDuration= 0.5,
            ),
        ],
        fluid=True,
        style={
            'width': '100%',
            'height': 'auto',
            'margin-top': '5px',
        }
    )

# options for dropdown menu
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
            columns_for_original_mortgate = [
                df_schema.level_2.PAYMENT,
                df_schema.level_2.PRINCIPAL,
                df_schema.level_2.INTEREST,
                df_schema.level_2.RESIDUAL,
            ]
            if accum and accum == 'cumulative':
                columns_for_original_mortgate = [
                    v for v in columns_for_original_mortgate if v != df_schema.level_2.RESIDUAL]
            dropdown = [
                dmc.MenuItem(
                    column,
                    id={
                        'index': column,
                        'type': GRAPH.DROPDOWN.ITEM
                    },
                ) for column in columns_for_original_mortgate if column != label
            ]  # avoid duplicate label
            return dropdown, {'display': 'block'}

# update the results
    @callback(
        Output(GRAPH.LINE, 'figure'),
        # Output('clientside-figure-storage', 'data'),
        Output('menu-target', 'children'),
        Output('menu-target', 'rightIcon'),
        Output('menu-target', 'loading'),
        Output('menu-target', 'gradient'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        Input({'index': ALL, 'type': GRAPH.DROPDOWN.ITEM}, 'n_clicks'),
        State('menu-target', 'children'),
    )
    def _graph(
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
                chosen_figure = df_schema.level_0.TOTAL
        # figure_config = {
        #     'data': [],
        #     'layout': {
        #         'modebar': {
        #             'bgcolor': 'rgba(255, 255, 255, 0.3)',
        #             'activecolor': 'gray',
        #             'orientation': 'v',
        #         },
        #         'paper_bgcolor': 'rgba(0,0,0,0)',
        #         'plot_bgcolor': 'rgba(255,255,255, 0.3)',
        #         'legend': {
        #             'groupclick': 'toggleitem',
        #             'orientation': 'h',
        #             'yanchor': 'bottom',
        #             'y': 1.01,
        #             'xanchor': 'right',
        #             'x': 1,
        #         },
        #         'margin': {'t': 30},
        #         'xaxis': {
        #             'title': 'Time',
        #             'showgrid': True,
        #             'gridwidth': 1,
        #             'gridcolor': 'LightGray',
        #         },
        #         'yaxis': {
        #             'title': 'Amount',
        #             'showgrid': True,
        #             'gridwidth': 1,
        #             'gridcolor': 'LightGray',
        #             'type': 'log',
        #                     'tickformat': ',.0f',
        #                     'rangemode': 'tozero',
        #         },
        #     },
        # }
        ns, cols = zip(*[(n, col) for n, col in enumerate(data['columns']) if chosen_figure in col])
        x_axis_value = data['index'][1:-1]
        
        # construct a dict for argumnets for px
        data_frame= {
            'Time': [],
            'Amount': [],
            'labels': [],
            'methods': [],
        }

        for n, col in zip(ns, cols):
            dff = [data[n] for data in data['data'][1:-1]]
            method = (" + ".join([co for co in col if co != chosen_figure]) if len(col) > 2 else col[0])
            if accum == 'cumulative':
                dff = [*accumulate(dff)]
            dff = [*map(lambda x: f"{round(x):,}", dff)]
            
            data_frame['Time'].extend(x_axis_value)
            data_frame['Amount'].extend(dff)
            data_frame['labels'].extend([method] * len(x_axis_value))
            data_frame['methods'].extend([method] * len(x_axis_value))
            
            # figure_config['data'].append(
            #     {
            #         'connectgaps': True,
            #         'hovertemplate': '''
            #             <br><b>%{text}</b>
            #             <br><b>Time</b>: %{x}<br>
            #             <b>Amount</b>: %{y:,}<extra></extra>
            #         ''',
            #         'legendgroup': chosen_figure,
            #         'legendgrouptitle': {'text': chosen_figure},
            #         'mode': 'lines',
            #         'name': method,
            #         'text': [method] * len(x_axis_value),
            #         'type': 'scatter',
            #         'stackgroup': (col[0] if accum == 'cumulative' else None),
            #         'x': x_axis_value,
            #         'y': dff,
            #     }
            # )
        # figure= go.Figure(figure_config)
        figure = px.line(
            data_frame, 
            x= "Time", 
            y="Amount", 
            color="methods", 
            title="Life of Loan", 
            width=1000, 
            height=600,
            log_y= True,
            line_shape="spline",
            render_mode="svg",
            hover_name="methods",
            template="plotly_white",
            
        )
        
        figure.update_layout(showlegend= False)
        return figure, chosen_figure, (DashIconify(icon="raphael:arrowdown") if chosen_figure != df_schema.level_0.TOTAL else None), False, ({"from": "teal", "to": "blue", "deg": 60} if chosen_figure == df_schema.level_0.TOTAL else {"from": "indigo", "to": "cyan"})
    # callback for updating the information from hoverData

    @callback(
        Output('right-text-board', 'children'),
        Input(GRAPH.LINE, 'hoverData'),
        State(LOAN.RESULT.DATAFRAME, 'data'),
        State('menu-target', 'children'),
    )
    def hover_data(hoverdata, memory, chosen_figure):
        if hoverdata:
            timepoint = hoverdata['points'][0]['x']
            hovered_text= hoverdata['points'][0]['hovertext']
            # residual_payments= [[da for col, da in zip(memory['data']['columns'], data) if col[1] == df_schema.level_2.RESIDUAL] for t, data in zip(memory['data']['index'], memory['data']['data']) if t == timepoint]
            # data_array= [[da for col, da in zip(memory['data']['columns'], data) if col[0]== hovered_text and col[1] == df_schema.level_2.PAYMENT] for t, data in zip(memory['data']['index'], memory['data']['data']) if t == timepoint]
            data_array= [*chain.from_iterable([da for col, da in zip(memory['data']['columns'], data) if col[0]== hovered_text and col[1]== df_schema.level_2.PAYMENT] for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)])]
            print(len(data_array))
            return round(sum(data_array)/len(data_array))


    return layout


# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    app.layout = graph()
    app.run_server(debug=True)
