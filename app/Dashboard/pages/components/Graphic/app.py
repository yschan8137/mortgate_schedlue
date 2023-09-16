import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input, State, MATCH, ALL, no_update, callback_context
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from itertools import product
import math

import numpy as np

from app.Dashboard.pages.components.Controls.main import panel
from app.Dashboard.pages.components.ids import GRAPH, LOAN
from app.Loan import *



# reference: https://towardsdatascience.com/how-to-make-multi-index-index-charts-with-plotly-4d3984cd7b09#2e1b
# https://plotly.com/python/line-and-scatter/

app = Dash(__name__, 
       external_stylesheets=[dbc.themes.LUMEN, dbc.icons.BOOTSTRAP],
       suppress_callback_exceptions=True,
       ) 

# enable horizontal scrolling: https://community.plotly.com/t/horizontal-scroll-bootstrap-modal-component/43547
def graph():
    layout= dbc.Container(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Checklist(
                            id= GRAPH.ACCUMULATION,
                            options= [{'label': GRAPH.ACCUMULATION, 'value': 1}],
                        value= [],
                        switch= True,
                        className= 'mb-3',
                        ),
                        width= 4,
                        style= {
                            # 'position': 'absolute',
                            'margin-left': '6%',
                        }
                    ),
                    dbc.Col(
                        dbc.DropdownMenu(
                            id= GRAPH.DROPDOWN.MENU,
                            # className= 'mb-2',
                            color= '#BCDFFB',
                            style={
                                'width': '100%',
                                "borderColor": "#ff0000",

                            },
                            toggle_style={
                                'width': '100px',
                                "color": "#162126", 
                                'font-weight': 'bold',
                                # 'text-align': '',
                            },
                            toggleClassName="border None text-align justify middle",
                        ),
                        style={
                            'position': 'absolute',
                            'left': '77%',
                            'bottom': '82%'
                        }
                    )
                ],
                # justify="between",
                style= {
                }
            ),
            dbc.Col(
                dcc.Graph(
                    id= GRAPH.LINE,
                    # animate= True,
                    # animation_options= {
                        # 'frame': {'redraw': False, }, 
                        # 'transition': {
                            # 'duration': 500, 
                            # 'ease': 'cubic-in-out', 
                        # },
                    # },
                ),
                style= {
                }
            ),

        ],
        fluid=True,
        className= 'bm-2',
        # style= {
            # "overflow-x": "scroll",
        # }
    )

# options for dropdown menu
    @callback(
        Output(GRAPH.DROPDOWN.MENU, 'children'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        Input(GRAPH.DROPDOWN.MENU, 'label')
    )
    def update_toggle_items(
        accum, 
        resource_data,
        label
        ):
        init_columns= [
            df_schema.level_2.PAYMENT, 
            df_schema.level_2.PRINCIPAL, 
            df_schema.level_2.INTEREST, 
            df_schema.level_2.RESIDUAL,
        ]
        if accum and accum == [1]:
            init_columns= [v for v in init_columns if v != df_schema.level_2.RESIDUAL]
        return [dbc.DropdownMenuItem(children= column, id= {'index': column, 'type': GRAPH.DROPDOWN.ITEM}) for column in init_columns if column != label]

# update label of the dropdown menu
    @callback(
        Output(GRAPH.DROPDOWN.MENU, 'label'),
        Input(GRAPH.LINE, 'figure'),
    )
    def update_label_for_dropdownmune(fig):
        return [*{data['legendgroup'] for data in fig['data']}][0]



# update the results
    @callback(
        Output(GRAPH.LINE, 'figure'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        Input({'index': ALL, 'type': GRAPH.DROPDOWN.ITEM}, 'n_clicks'),
        State(GRAPH.LINE, 'figure'),
    )
    def _graph(
        accum, 
        resource_data,
        _,
        fig
        ):
        ctx= callback_context
        if isinstance(ctx.triggered_id, dict):
            chosen_figure= ctx.triggered_id['index']
        else:
            chosen_figure= df_schema.level_2.PAYMENT
        df = pd.DataFrame.from_dict(resource_data, 'tight')[1:-1]
        fig= go.Figure()
        # fig= make_subplots(
            # rows= 1,#len(init_columns), 
            # cols= len(init_columns),#1, 
            # start_cell="top-left", 
            # subplot_titles= ['<b>' + title + '<b>' for title in init_columns],
            # specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]],
        # )
        for method in [df_schema.level_1.ETP, df_schema.level_1.EPP]:
            dff = df[method]
            if accum and accum == [1]:
                dff = dff.cumsum().apply(lambda x: round(x))
            # for r, item in zip(range(1, len(init_columns) + 1), init_columns):
            
            filtered_dff= dff[chosen_figure].apply(lambda x: round(x, 0))
            fig.add_trace(
                go.Scatter(
                    x= filtered_dff.index,
                    y= filtered_dff.values,
                    legendgroup= chosen_figure,
                    legendgrouptitle_text= chosen_figure,
                    name= method,                   
                    mode= 'lines',
                    connectgaps= True,
                    fill= ('tonexty' if accum == [1] else None),
                    stackgroup= (method if accum == [1] else None),
                ),
                # row= 1,
                # col= r,
            )
            # fig.update_annotations(
                # x= .1 + (r-1)* .265, 
                # y=  -0.15,#(0.7295 - 0.38 * (r - 1) if len(init_columns) == 3 else 0.81 - 0.28 * (r - 1)),
                # xanchor= 'center',
                # yanchor= 'bottom',
                # selector={'text': '<b>' + item + '<b>'},
                # font= {
                    # 'size': 18,
                # },
            # )
        fig.update_layout(
            showlegend= True,
            height= 500,#(1600 if len(init_columns) == 3 else 2200),
            # width= (4800 if len(init_columns) == 4 else 3570),
            paper_bgcolor='rgba(0,0,0,0)',
            # plot_bgcolor='rgba(0,0,0,0)',
            legend= {
                'groupclick': 'toggleitem',
                # 'orientation': 'h',
                # 'borderwidth': 1,
            },
            modebar= {
                'bgcolor': 'rgba(0,0,0, 0.1)',
                'activecolor':'gray',
            },
            legend_tracegroupgap= 0.2,#(490 if len(init_columns) == 3 else 510),
            margin= {'t': 30},

        )
        return fig
    return layout


# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    app.layout= graph()
    app.run_server(debug=True)
