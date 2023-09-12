import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input, State, MATCH, ALL, no_update
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

# groping

def graph():
    layout= dbc.Container(
        [
            dbc.Checklist(
                id= GRAPH.ACCUMULATION,
                options= [{'label': GRAPH.ACCUMULATION, 'value': 1}],
            value= [1],
            switch= True,
            ),
            dbc.Col(
                dcc.Graph(
                    id= GRAPH.LINE,
                ),
            ),
        ],
        fluid=True,
        className= 'bm-2',
        style= {
        }
    )

    @callback(
        Output(GRAPH.LINE, 'figure'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        State(GRAPH.LINE, 'figure'),
    )
    def _graph(
        accum, 
        resource_data,
        fig
        ):
        df = pd.DataFrame.from_dict(resource_data, 'tight')[1:-1]
        init_columns= [
            df_schema.level_2.PRINCIPAL, 
            df_schema.level_2.INTEREST, 
            df_schema.level_2.PAYMENT, 
            df_schema.level_2.RESIDUAL,
        ]
        if accum and accum == [1]:
            init_columns= [v for v in init_columns if v != df_schema.level_2.RESIDUAL]
        fig= make_subplots(
            rows= len(init_columns), 
            cols= 1, 
            start_cell="top-left", 
            subplot_titles= ['<b>' + title + '<b>' for title in init_columns],
            
        )
        for method in [df_schema.level_1.ETP, df_schema.level_1.EPP]:
            dff = df[method]
            if accum and accum == [1]:
                dff = dff.cumsum().apply(lambda x: round(x))
            for r, item in zip(range(1, len(init_columns) + 1), dff.columns):
                filtered_dff= dff[item].apply(lambda x: round(x, 0))
                fig.add_trace(
                    go.Scatter(
                        x= filtered_dff.index,
                        y= filtered_dff.values,
                        legendgroup= item,
                        legendgrouptitle_text= item,
                        name= method,                        
                        mode= 'lines',
                        connectgaps= True,
                        fill= ('tozeroy' if accum and accum == [1] else None),
                        stackgroup= (method if accum and accum == [1] else None),
                    ),
                    row= r,
                    col= 1,
                )
                fig.update_annotations(
                    x=0.5, 
                    y=  (0.7295 - 0.38 * (r - 1) if len(init_columns) == 3 else 0.81 - 0.28 * (r - 1)),
                    xanchor= 'center',
                    yanchor= 'bottom',
                    selector={'text': '<b>' + item + '<b>'},
                    )                                
        fig.update_layout(
            showlegend= True,
            height= (1600 if len(init_columns) == 3 else 2200),
            legend= {
                'groupclick': 'toggleitem',
            },
            legend_tracegroupgap= (490 if len(init_columns) == 3 else 510)
        )
        return fig
    return layout

# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    app.layout= graph()
    app.run_server(debug=True)
