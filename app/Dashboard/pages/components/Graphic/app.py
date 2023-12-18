"""Build a graph for the loan"""
from itertools import accumulate
from dash import Dash, dcc, callback, Output, Input, State, ALL, callback_context, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import plotly.express as px
from plotly.subplots import make_subplots
import dash_mantine_components as dmc
import time
import numpy as np

from app.Dashboard.assets.ids import GRAPH, LOAN
from app.Loan import df_schema


def graph():
    """Build the graph"""
    layout = dmc.Container(
        [
            dmc.Group(
                [
                    html.Div(
                        dmc.LoadingOverlay(
                            children= [
                                dcc.Graph(
                                        id='bars-graph-for-gerneral',
                                        style={
                                            'background-color': 'rgba(0, 0, 0, 0)',
                                            'margin-top': '10px',
                                        },
                                        config={
                                            'displayModeBar': False,
                                            'doubleClick': 'reset+autosize',
                                            'autosizable': True,
                                            'editable': False,
                                            'scrollZoom': False,
                                            'staticPlot': False,
                                        }
                                ),
                            ],
                            loaderProps={
                                "variant": "oval",
                                 "color": "blue", 
                                 "size": "lg",
                                 'is_loading': True,
                            },
                            transitionDuration= 0.5,
                        ),
                        style={
                            'border-radius': '5px',
                            'border': '1px solid #ccc',
                            'border-radius': '5px',
                            'height': 150,
                        },
                    ),
                    html.Div(
                        dmc.LoadingOverlay(
                                children= [
                                    dcc.Graph(
                                        id='bars-graph-for-details',
                                        style={
                                            'background-color': 'rgba(0, 0, 0, 0)',
                                            'margin-top': '10px',
                                        },
                                        config={
                                            'displayModeBar': False,
                                            'doubleClick': 'reset+autosize',
                                            'autosizable': True,
                                            'editable': False,
                                            'scrollZoom': False,
                                            'staticPlot': False,
                                        }
                                )
                            ],
                            loaderProps={"variant": "oval",
                                 "color": "blue", 
                                 "size": "lg",
                                 'is_loading': True,
                            },
                            transitionDuration= 0.5,
                        ),
                        style={
                            'border-radius': '5px',
                            'border': '1px solid #ccc',
                            'border-radius': '5px',
                            'height': 150,
                        },
                    ),
                ],
                grow=True,
                style= {
                    'margin-top': '10px',
                }    
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
                        },
                    ),
                ],
                spacing=10,
                position='left',
                style={
                    'width': '100%',
                }
            ),
            html.Div(
                dmc.LoadingOverlay(
                    dcc.Graph(
                        id=GRAPH.LINE,
                        hoverData= {'points': [{'x': '0', 'hovertext': 'ETP'}]},
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
                        },
                    ),
                    id= 'loading-overlay',
                    loaderProps={"variant": "oval",
                                 "color": "blue", 
                                 "size": "lg",
                                 'is_loading': True,
                                 },
                    transitionDuration= 0.5,
                ),
                style={
                    'width': '100%',
                    'height': 600,
                },
            ),
        ],
        fluid=True,
        style={
            'width': '100%',
            'height': 'auto',
            'margin-top': '5px',
        }
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

#2 update the main graph
    @callback(
        Output(GRAPH.LINE, 'figure'),
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
                chosen_figure = df_schema.level_0.TOTAL
        
        ns, cols = zip(*[(n, col) for n, col in enumerate(data['columns']) if chosen_figure in col])
        x_axis_value = data['index'][1:-1]
        
        # construct the data frame for the graph
        data_frame_for_loan_timeSeries= {
            'Time': [],
            'Amount': [],
            'labels': [],
            'methods': [],
        }

        for n, col in zip(ns, cols): # n: index of the column, col: column name
            dff = [data[n] for data in data['data'][1:-1]]
            method = (" + ".join([co for co in col if co != chosen_figure]) if len(col) > 2 else col[0])
            if accum == 'cumulative':
                dff = [*accumulate(dff)]
            dff = [*map(lambda x: f"{round(x):,}", dff)]
            
            data_frame_for_loan_timeSeries['Time'].extend(x_axis_value)
            data_frame_for_loan_timeSeries['Amount'].extend(dff)
            data_frame_for_loan_timeSeries['labels'].extend([method] * len(x_axis_value))
            data_frame_for_loan_timeSeries['methods'].extend([method] * len(x_axis_value))
            
        fig = px.line(
            data_frame_for_loan_timeSeries, 
            x= "Time", 
            y="Amount", 
            color="methods", 
            title='<b>Life of Loan</b>', 
            width=1000, 
            height=600,
            log_y= True,
            line_shape="spline",
            render_mode="svg",
            hover_name="methods",
            template="plotly_white",
            color_discrete_map= {
                    df_schema.level_1.ETP: '#0C82DF',
                    df_schema.level_1.EPP: '#F7DC6F',
            },   
        )
        fig.update_layout(showlegend= False)

        return fig, chosen_figure, (DashIconify(icon="raphael:arrowdown") if chosen_figure != df_schema.level_0.TOTAL else None), False, ({"from": "teal", "to": "blue", "deg": 60} if chosen_figure == df_schema.level_0.TOTAL else {"from": "indigo", "to": "cyan"})

#3 callback for updating the information from hoverData
    @callback(
        Output('bars-graph-for-gerneral', 'figure'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
    )
    def update_general_info(
        memory
        ):
        bar_layout= dict(
            showlegend= False,
            margin= dict(l=20, r=10, t=35, b=50),
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
        )
        if memory:
            bars_data = {
                'columns': list({col[0] for col in memory['data']['columns']}),
                'data': []
            }
            if bars_data['columns'][0]:
                bars_data['data']= [
                    round([da for col, da in zip(memory['data']['columns'], memory['data']['data'][-1]) if col[0]== chosen_col and col[1]== df_schema.level_2.PAYMENT][0]/ len(memory['data']['index'][1:-1]))
                        for chosen_col in bars_data['columns']
                ]
                figure= px.bar(
                    bars_data,
                    x= 'data',
                    y= 'columns',
                    text= 'data',
                    text_auto= True,                
                    color= 'columns',
                    height= 180,
                    width= 530,
                    title= '<b>Average Payment</b>',
                    color_discrete_map= {
                        df_schema.level_1.ETP: '#0C82DF',
                        df_schema.level_1.EPP: '#F7DC6F',
                    },
                )
                figure.update_layout(bar_layout)
                figure.update_yaxes(
                    visible= False,
                    showticklabels= False,
                )
                figure.update_xaxes(
                    visible= False,
                    showticklabels= False,
                )
                figure.update_traces(
                    texttemplate='%{text:,}',

                )
            else:
                figure= px.bar()
                figure.update_layout(bar_layout)
                figure.update_yaxes(
                    visible= False,
                    showticklabels= False,
                )
                figure.update_xaxes(
                    visible= False,
                    showticklabels= False,
                )
            return figure
        else:
            raise PreventUpdate

#4 callback for updating the detail information from hoverData
    @callback(
        Output('bars-graph-for-details', 'figure'),
        Input(GRAPH.LINE, 'hoverData'),
        State(LOAN.RESULT.DATAFRAME, 'data'),
    )
    def hover_data(
        hover_data,
        memory
        ):
        bar_layout= dict(
            showlegend= False,
            margin= dict(l=20, r=10, t=35, b=50),
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
        )
        if memory:
            if hover_data:
                timepoint= hover_data['points'][0]['x']
                chosen_figure= hover_data['points'][0]['hovertext']
                bar_data = {
                    'names': chosen_figure,
                    'items': ['principal', 'interest', 'residual'],
                    'data': [],
                    'index': 0,
                }
                principal = round(
                            np.sum(
                                    [
                                        [da for col, da in zip(memory['data']['columns'], data) 
                                         if col[0]== chosen_figure and col[1]== df_schema.level_2.PRINCIPAL] 
                                         for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)+1]
                                    ]
                                )
                            )
                interest = round(
                            np.sum(
                                    [
                                        [da for col, da in zip(memory['data']['columns'], data) 
                                         if col[0]== chosen_figure and col[1]== df_schema.level_2.INTEREST] 
                                         for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)+1]
                                    ]
                                )
                            )
                residual = round([data for col, data in zip(memory['data']['columns'], memory['data']['data'][memory['data']['index'].index(timepoint)]) if col[0]== chosen_figure and col[1]== df_schema.level_2.RESIDUAL][0])
                bar_data['data']= [principal, interest, residual]

                fig= px.bar(
                    bar_data,
                    x= 'data',
                    y= 'index',
                    text= 'data',
                    text_auto= True,                
                    color= 'items',
                    height= 200,
                    width= 500,
                    orientation= 'h',
                    title= '''
                            <b>{} 
                            Time: {}</b>
                            '''.format(bar_data['names'], timepoint),
                    color_discrete_map= {
                        'principal': '#FF7F50',
                        'interest': '#F7DC6F',
                        'residual': '#6495ED',
                    },
                )
                fig.update_layout(bar_layout)
                fig.update_yaxes(
                    visible= False,
                    showticklabels= False,
                )
                fig.update_xaxes(
                    range= [0, (bar_data['data'][0] + bar_data['data'][2])* 1.1],
                    visible= False,
                    showticklabels= False,
                )
                fig.update_traces(
                    texttemplate='%{text:,}',
                    width= .3,
                )
                return fig
            else:
                fig= px.bar(
                    height= 300,
                    width= 500,
                )
                fig.update_layout(bar_layout)
                fig.update_yaxes(
                    visible= False,
                    showticklabels= False,
                )
                fig.update_xaxes(
                    visible= False,
                    showticklabels= False,
                )
                return fig
        else:
            raise PreventUpdate
       
       
    return layout
        
                
        
    return layout

# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    import dash_bootstrap_components as dbc
    app = Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.LUMEN, 
            dbc.icons.BOOTSTRAP
            ],
        suppress_callback_exceptions=True,
    )

    app.layout = graph()
    app.run_server(debug=True)
