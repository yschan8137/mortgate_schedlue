"""Build a graph for the loan"""
from itertools import accumulate
from dash import Dash, dcc, callback, Output, Input, State, ALL, callback_context, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import plotly.express as px
import dash_mantine_components as dmc
import numpy as np
from itertools import product

import sys
sys.path.append('./')

from app.Dashboard.assets.ids import GRAPH, LOAN
from app.Loan import df_schema, merge_sublist


def graph():
    """Build the graph"""
    layout = html.Div(
        [
            # dmc.Group(
                # [
                    # html.Div(
                        # dmc.LoadingOverlay(
                            # id= 'loading-overlay-for-general',
                            # children= [],
                            # loaderProps={
                                # "variant": "oval",
                                #  "color": "blue", 
                                #  "size": "lg",
                                #  'is_loading': True,
                            # },
                            # style= {
                                # 'margin-top': '10px',
                                # 'height': 130,
                            # },
                            # transitionDuration= 0.5,
                        # ),
                        # style={
                            # 'border-radius': '5px',
                            # 'border': '1px solid #ccc',
                            # 'border-radius': '5px',
                            # 'height': 150,
                            # 'background-color': 'white',
                        # },
                    # ),
                    # html.Div(
                        # dmc.LoadingOverlay(
                                # id= 'loading-overlay-for-details',
                                # children= [],
                            # loading_state= {
                                # 'is_loading': False,
                                # 'loading_type': 'overlay',
                                # 'prop_name': 'children',
                                # },
                            # loaderProps={
                                # "variant": "oval",
                                #  "color": "blue", 
                                #  "size": "lg",
                                #  'is_loading': True,
                            # },
                            # style= {
                                # 'margin-top': 'auto',
                                # 'margin-dottom': 'auto',
                                # 'height': 130,
                                # 'fontweight': 'bold',
                            # },
                            # transitionDuration= 0.5,
                        # ),
                        # style={
                            # 'border-radius': '5px',
                            # 'border': '1px solid #ccc',
                            # 'height': 150,
                            # 'background-color': 'white',
                        # },
                    # ),
                # ],
                # grow=True,
                # style= {
                    # 'margin-top': '10px',
                # }    
            # ),
            html.Div(
                children= [
                    dcc.Graph(
                        id= 'information-dashboard',
                        animation_options= dict(
                            frame= dict(
                                duration= 10,
                                redraw= True,
                            ),
                            transition= dict(
                                duration= 10,
                                easing= 'quad-in-out',
                            )
                        ),
                        animate= True,
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
                    )
                ],
                style= {
                    'height': '40%',
                    'top': 'auto',
                    'border-radius': '5px',
                    'border': '1px solid #ccc',
                    'background-color': 'white',
                    'box-shadow': '0 0 5px #ccc',
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
            html.Div(
                dmc.LoadingOverlay(
                    children= [
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
                                    # 'height': 'auto',
                                    'scale': 1,
                                },
                            },
                            style={
                                'width': '100%',
                                'height': '100%',
                            },
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

        return fig, chosen_figure, (DashIconify(icon="raphael:arrowdown") if chosen_figure != df_schema.level_0.TOTAL else None), False, ({"from": "teal", "to": "blue", "deg": 60} if chosen_figure == df_schema.level_0.TOTAL else {"from": "indigo", "to": "cyan"})

#3 callback for updating the information from hoverData
    # @callback(
        # Output('loading-overlay-for-general', 'children'),
        # Input(LOAN.RESULT.DATAFRAME, 'data'),
    # )
    # def update_general_info(
        # memory,
        # ):
        # bar_layout= dict(
            # showlegend= False,
            # margin= dict(l=20, r=10, t=35, b=50),
            # paper_bgcolor= 'rgba(0, 0, 0, 0)',
            # plot_bgcolor= 'rgba(0, 0, 0, 0)',
        # )
        # if memory:
            # bars_data = {
                # 'columns': [],
                # 'data': []
            # }
# 
            # for col in memory['data']['columns']:
                # if len(col) > 2 and col[0] == df_schema.level_0.TOTAL:
                    # bars_data['columns'].append(" + ".join([co for co in col if co != df_schema.level_0.TOTAL]))
                    # bars_data['data'].append(round(memory['data']['data'][-1][memory['data']['columns'].index(col)] / len(memory['data']['index'][1:-1])))
                # else:
                    # if col[1] == df_schema.level_2.PAYMENT:
                        # bars_data['columns'].append(col[0])
                        # bars_data['data'].append(round(memory['data']['data'][-1][memory['data']['columns'].index(col)] / len(memory['data']['index'][1:-1])))
            # 
            # if bars_data['columns'][0]:
                # figure= px.bar(
                    # bars_data,
                    # x= 'data',
                    # y= 'columns',
                    # text= 'data',
                    # text_auto= True,                
                    # color= 'columns',
                    # height= 180,
                    # title= '<b>Average Payment</b>',
                    # color_discrete_map= {
                        # df_schema.level_1.ETP: '#0C82DF',
                        # df_schema.level_1.EPP: '#F7DC6F',
                    # },
                    # hover_data= {
                        # 'columns': False,
                        # 'data': True,
                    # },
                    # hover_name= 'columns',
                # )
                # figure.update_layout(bar_layout)
                # figure.update_yaxes(
                    # visible= False,
                    # showticklabels= False,
                # )
                # figure.update_xaxes(
                    # range= [0, max(bars_data['data']) * 1.1],
                    # visible= False,
                    # showticklabels= False,
                # )
                # figure.update_traces(
                    # texttemplate='%{text:,}',
# 
                # )
            # else:
                # figure= px.bar()
                # figure.update_layout(bar_layout)
                # figure.update_yaxes(
                    # visible= False,
                    # showticklabels= False,
                # )
                # figure.update_xaxes(
                    # visible= False,
                    # showticklabels= False,
                # )
            # return dcc.Graph(
                    # figure= figure,
                    # animate= True,
                    # style={
                        # 'background-color': 'rgba(0, 0, 0, 0)',
                        # 'margin-top': '10px',
                        # 'width': '100%',
                    # },
                    # config={
                        # 'displayModeBar': False,
                        # 'doubleClick': 'reset+autosize',
                        # 'autosizable': True,
                        # 'editable': False,
                        # 'scrollZoom': False,
                        # 'staticPlot': False,
                    # }
            # )
        # else:
            # raise PreventUpdate

#4 callback for updating the detail information from hoverData
    # @callback(
        # Output('loading-overlay-for-details', 'children'),
        # Input(GRAPH.LINE, 'hoverData'),
        # State(LOAN.RESULT.DATAFRAME, 'data'),
        # State('menu-target', 'children')
    # )
    # def hover_data(
        # hover_data,
        # memory,
        # chosen_figure,
        # ):
        # bar_layout= dict(
            # showlegend= False,
            # margin= dict(l=20, r=10, t=35, b=40),
            # paper_bgcolor= 'rgba(0, 0, 0, 0)',
            # plot_bgcolor= 'rgba(0, 0, 0, 0)',
        # )
        # if memory:
            # timepoint= hover_data['points'][0]['x']
            # 
            # if timepoint != '0':
                # hovered_figure= hover_data['points'][0]['hovertext']
                # bar_data = {
                    # 'method': hovered_figure,
                    # 'items': ['principal', 'interest', 'residual'],
                    # 'data': [],
                    # 'index': 0,
                # }
                # principal = round(
                            # np.sum(
                                    # [
                                        # [da for col, da in zip(memory['data']['columns'], data) 
                                        #  if (
                                            #  (col[0]== df_schema.level_0.ORIGINAL and col[1]== hovered_figure.split(' + ')[0].split('(')[0] and col[2]== df_schema.level_2.PRINCIPAL) or
                                            #  (col[0]== df_schema.level_0.SUBSIDY and col[1]== hovered_figure.split('+')[0].split('(')[0] and col[2]== df_schema.level_2.PRINCIPAL)
                                            #  if len(col) > 2
                                            #  else col[0] == hovered_figure and col[1] == df_schema.level_2.PRINCIPAL
                                            # ) 
                                        #  ] 
                                        #  for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)+1]
                                    # ]
                                # )
                            # )
                # interest = round(
                            # np.sum(
                                    # [
                                        # [da for col, da in zip(memory['data']['columns'], data) 
                                        #  if (
                                            #  (col[0]== df_schema.level_0.ORIGINAL and col[1]== hovered_figure.split(' + ')[0].split('(')[0] and col[2]== df_schema.level_2.INTEREST) or
                                            #  (col[0]== df_schema.level_0.SUBSIDY and col[1]== hovered_figure.split('+')[0].split('(')[0] and col[2]== df_schema.level_2.INTEREST)
                                            #  if len(col) > 2
                                            #  else col[0] == hovered_figure and col[1] == df_schema.level_2.INTEREST
                                            # )
                                        #  ] 
                                        #  for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)+1]
                                    # ]
                                # )
                            # )
                # residual = round(
                    # np.sum(
                        # [
                            # data 
                            # for col, data in zip(
                                # memory['data']['columns'], 
                                # memory['data']['data'][memory['data']['index'].index(timepoint)]
                                # ) if (
                                        # (col[0]== df_schema.level_0.ORIGINAL and col[1]== hovered_figure.split(' + ')[0].split('(')[0] and col[2]== df_schema.level_2.RESIDUAL) or
                                        # (col[0]== df_schema.level_0.SUBSIDY and col[1]== hovered_figure.split('+')[0].split('(')[0] and col[2]== df_schema.level_2.RESIDUAL)                                        
                                        # if len(col) > 2
                                        # else col[0] == hovered_figure and col[1] == df_schema.level_2.RESIDUAL
                                    # )
                        # ]
                    # )
                # )
                # 
                # bar_data['data']= [principal, interest, residual]
# 
                # fig= px.bar(
                    # bar_data,
                    # x= 'data',
                    # y= 'index',
                    # text= 'data',
                    # text_auto= True,                
                    # color= 'items',
                    ## height= 180,
                    # orientation= 'h',
                    # title= '<b>Payment Breakdown</b>',
                    # color_discrete_map= {
                        # 'principal': '#FF7F50',
                        # 'interest': '#F7DC6F',
                        # 'residual': '#6495ED',
                    # },
                    # hover_data= {
                        # 'items': False,
                        # 'index': False,
                        # 'data': True,
                    # },
                    # hover_name= 'items',
                # )
                # fig.update_layout(bar_layout)
                # fig.update_yaxes(
                    # visible= False,
                    # showticklabels= False,
                # )
                # fig.update_xaxes(
                    # range= [0, sum(bar_data['data']) * 1.1],
                    # visible= False,
                    # showticklabels= False,
                # )
                # fig.update_traces(
                    # texttemplate='%{text:,}',
                    # width= 0.5,
                # )
                # return dcc.Graph(
                        # figure= fig,
                        # animate= True,
                        # style={
                            # 'background-color': 'rgba(0, 0, 0, 0)',
                            # 'margin-top': '10px',
                            # 'width': '100%', 
                        # },
                        # config={
                            # 'displayModeBar': False,
                            # 'doubleClick': 'reset+autosize',
                            # 'autosizable': True,
                            # 'editable': False,
                            # 'scrollZoom': False,
                            # 'staticPlot': False,
                        # }
                # )
            # else:
                # return dmc.Center(
                        # dmc.Text(
                        # 'Tap the graph for more details', 
                        # weight='bold', 
                        # variant="gradient",
                        # gradient={"from": "red", "to": "yellow", "deg": 45},
                        # style={
                            # 'width': '100%',
                            # 'height': '100%',
                            # "fontSize": 30,
                            # 'textAlign': 'center',
                            # 'margin-top': '50px',
                            # }, 
                    # )
                # )
        # else:
            # raise PreventUpdate
    @callback(
        Output('information-dashboard', 'figure'),
        Input(GRAPH.LINE, 'hoverData'),
        State(LOAN.RESULT.DATAFRAME, 'data'),
        State('menu-target', 'children')
    )
    def update_info(
        hover_data, 
        memory, 
        chosen_figure
        ):
        if memory:
            timepoint= hover_data['points'][0]['x']  
            if timepoint != '0':
                hovered_figure= hover_data['points'][0]['hovertext']
                bar_data = {
                    'method': [df_schema.level_1.EPP, df_schema.level_1.ETP],
                    'subsidy': [df_schema.level_1.EPP, df_schema.level_1.ETP],
                    'items': ['principal', 'interest', 'residual'],
                    'value': [],
                }
                # principal= [
                #         [
                #             [
                #                 da for col, da in zip(memory['data']['columns'], data) 
                #                 if (
                #                     (col[0] == df_schema.level_0.ORIGINAL and col[1] == name and col[2] == df_schema.level_2.PRINCIPAL) and
                #                     (col[0] == df_schema.level_0.SUBSIDY and col[1] == subsidy_name and col[2] == df_schema.level_2.PRINCIPAL)
                #                     if len(col) > 2
                #                     else col[0] == name and col[1] == df_schema.level_2.PRINCIPAL
                #                 )
                #             ][0] 
                #             for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)+1]
                #         ] for name in bar_data['method']
                # ]
                principal= [
                    [
                        [
                            data[n] for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)+1]
                         ] 
                         for n, col in enumerate(memory['data']['columns']) if (
                             (col[0] == df_schema.level_0.ORIGINAL and col[1] == name and col[2] == df_schema.level_2.PRINCIPAL) and
                             (col[0] == df_schema.level_0.SUBSIDY and col[1] == subsidy_name and col[2] == df_schema.level_2.PRINCIPAL)
                             if len(col) > 2
                             else (col[0] == name and col[1] == df_schema.level_2.PRINCIPAL 
                                   if name == subsidy_name else False
                                   )
                            )
                    ] for name, subsidy_name in product(bar_data['method'], bar_data['subsidy'])
                ]
                interest= [
                    [
                        [
                            data[n] for data in memory['data']['data'][1:memory['data']['index'].index(timepoint)+1]
                         ] 
                         for n, col in enumerate(memory['data']['columns']) if (
                             (col[0] == df_schema.level_0.ORIGINAL and col[1] == name and col[2] == df_schema.level_2.INTEREST) and
                             (col[0] == df_schema.level_0.SUBSIDY and col[1] == subsidy_name and col[2] == df_schema.level_2.INTEREST)
                             if len(col) > 2
                             else (col[0] == name and col[1] == df_schema.level_2.INTEREST 
                                   if name == subsidy_name else False
                                   )
                            )
                    ] for name, subsidy_name in product(bar_data['method'], bar_data['subsidy'])
                ]
                residual= [
                    [
                        data 
                        for col, data in zip(
                            memory['data']['columns'], 
                            memory['data']['data'][memory['data']['index'].index(timepoint)]
                            ) if (
                                    (col[0] == df_schema.level_0.ORIGINAL and col[1] == name and col[2] == df_schema.level_2.RESIDUAL) and
                                    (col[0] == df_schema.level_0.SUBSIDY and col[1] == subsidy_name and col[2] == df_schema.level_2.RESIDUAL for subsidy_name in bar_data['subsidy'])
                                if len(col) > 2
                                else (col[0] == name and col[1] == df_schema.level_2.RESIDUAL
                                      if name == subsidy_name else False
                                      )
                            )
                    ] for name, subsidy_name in product(bar_data['method'], bar_data['subsidy'])
                ]

                bar_data['value']= [round(np.sum(v)) for v in [*merge_sublist(principal), *merge_sublist(interest), *merge_sublist(residual)]]
                bar_data['method'] = bar_data['method'] * int(len(bar_data['value']) / len(bar_data['method']))
                bar_data['subsidy'] = bar_data['subsidy'] * int(len(bar_data['value']) / len(bar_data['subsidy']))
                bar_data['items'] = sorted(bar_data['items'] * int(len(bar_data['value']) / len(bar_data['items'])))
                fig= px.pie(
                    bar_data,
                    values='value',
                    names='items',
                    hole= 0.8,
                    opacity= 0.8,
                    color_discrete_sequence= px.colors.sequential.Teal,
                    template='seaborn',
                    facet_col= 'method',
                )
                fig.update_layout(
                    showlegend= True,
                    legend= dict(
                        orientation= 'v',
                        yanchor= 'bottom',
                        y= 1.02,
                        xanchor= 'right',
                        x= 1,
                    ),
                    margin= dict(l=20, r=10, t=35, b=40),
                    paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    plot_bgcolor= 'rgba(0, 0, 0, 0)',
                )
                fig.update_traces(
                    texttemplate='%{percent:.2%}',
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate= '%{label}: %{value:,}',
                    
                )
                return fig
            else:
                return {}
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
