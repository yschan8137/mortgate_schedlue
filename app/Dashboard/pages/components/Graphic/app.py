import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input, State, MATCH, ALL, callback_context, no_update, Patch
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from itertools import accumulate



from app.Dashboard.assets.ids import GRAPH, LOAN
from app.Dashboard.pages.components.toolkit import suffix_for_type
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
            dmc.Group(
                [
                    dmc.Menu(
                        [
                            dmc.MenuTarget(
                                dmc.Button(
                                    id= 'menu-target',
                                    children= df_schema.level_2.PAYMENT,
                                    variant="gradient",
                                    gradient={"from": "indigo", "to": "cyan"},
                                    style= {
                                        'width': '110px',
                                    },
                                    loading= {'loading_type': 'overlay'},
                                    loaderPosition= 'center',
                                    loaderProps= {"variant": "dots", "color": "white", "size": "sm"},
                                ),
                            ),
                            dmc.MenuDropdown(
                                [],
                                id= 'menu-dropdown',
                            ),
                        ],
                        id= GRAPH.DROPDOWN.MENU,  
                    ),
                    dmc.SegmentedControl(
                        id=GRAPH.ACCUMULATION,
                        value="regular",
                        data=[
                            {"value": "regular", "label": "Regular"},
                            {"value": "cumulative", "label": "Cumulative"},
                        ],
                        size= 'sm',
                        style= {
                            'background-color': "rgba(0, 62, 143, 0.29)",
                            'box-shadow': '0 0 5px #ccc',
                            'border': '1px solid #ccc',
                            'border-radius': '5px',
                        },
                    ),
                ],
                spacing= 10,
                position= 'left',
                style= {
                }
            ),
            dbc.Col(
                dcc.Graph(
                    figure= go.Figure(
                        layout= dict(
                            modebar= {
                                'bgcolor': 'rgba(255, 255, 255, 0.3)',
                                'activecolor':'gray',
                                'orientation': 'v',
                            },
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(255,255,255, 0.3)',
                            legend= {
                                'groupclick': 'toggleitem',
                            },
                            margin= {'t': 30},
                        )
                    ),
                    id= GRAPH.LINE,
                ),
            ),
        ],
        fluid=True,
        style= {
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
        data= data['data']
        level_0 = {c[0] for c in data['columns']}
        if df_schema.level_0.TOTAL in level_0:
            return [], {'display': 'none'}
        else:
            columns_for_original_mortgate= [
                df_schema.level_2.PAYMENT, 
                df_schema.level_2.PRINCIPAL, 
                df_schema.level_2.INTEREST, 
                df_schema.level_2.RESIDUAL,
            ]
            if accum and accum == 'cumulative':
                columns_for_original_mortgate= [v for v in columns_for_original_mortgate if v != df_schema.level_2.RESIDUAL]
            dropdown= [
                    dmc.MenuItem(
                        column, 
                        id= {
                            'index': column, 
                            'type': GRAPH.DROPDOWN.ITEM
                        },
                    ) for column in columns_for_original_mortgate if column != label
                ] # avoid duplicate label
            return dropdown, {'display': 'block'}           

# update the results
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
    def _graph(
        accum, 
        data,
        _,
        label,
        ):
        ctx= callback_context
        data= data['data']
        patched_figure= Patch()
        if isinstance(ctx.triggered_id, dict):
            chosen_figure= ctx.triggered_id['index']
        else:
            if df_schema.level_0.TOTAL not in [col[0] for col in data['columns']]: #type: ignore
                if accum == 'cumulative':
                    if label== df_schema.level_2.RESIDUAL:
                        chosen_figure= df_schema.level_2.PAYMENT
                    else:
                        chosen_figure= label
                else:
                    chosen_figure= (label if label != df_schema.level_0.TOTAL else df_schema.level_2.PAYMENT)
            else:
                chosen_figure = df_schema.level_0.TOTAL
        
        ns, cols = zip(*[(n, col) for n, col in enumerate(data['columns']) if chosen_figure in col])
        res= []
        for n, col in zip(ns, cols):
            dff= [data[n] for data in data['data'][1:-1]]
            method= (" + ".join([co for co in col if co != chosen_figure]) if len(col) > 2 else col[0])
            
            if accum == 'cumulative':
                dff= [*accumulate(dff)] 
            dff= [*map(lambda x: f"{round(x):,}", dff)]
            x_axis_value= data['index']
            
            res.append(go.Scatter(
                    x= x_axis_value,
                    y= dff,
                    legendgroup= chosen_figure,
                    legendgrouptitle_text= chosen_figure,
                    name= method,                   
                    mode= 'lines',
                    connectgaps= True,
                    stackgroup= (col[0] if accum == 'cumulative' else None),
                    text= [method]* len(x_axis_value),
                    hovertemplate =
                        "<br><b>%{text}</b>" +
                        "<br><b>Time</b>: %{x}" + 
                        "<br><b>Amount</b>: %{y:,}" +
                        "<extra></extra>",
                ),
            )
        # patched_figure['data'].name
        patched_figure['data']= res

        patched_figure['layout']['xaxis']= dict(
            title= 'Time',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
        )
        patched_figure['layout']['yaxis']= dict(
            title= 'Amount',
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            type= 'log',
            tickformat= ',.0f',
            rangemode= 'tozero',
        )
        patched_figure['layout']['autosize']= False
        patched_figure['layout']['width']= 1050
        patched_figure['layout']['height']= 600
        patched_figure['layout']['showlegend']= False
        patched_figure['layout']['hovermode']= 'x'        
        return patched_figure, chosen_figure, (DashIconify(icon="raphael:arrowdown") if chosen_figure != df_schema.level_0.TOTAL else None), False, ({"from": "teal", "to": "blue", "deg": 60} if chosen_figure == df_schema.level_0.TOTAL else {"from": "indigo", "to": "cyan"})
    return layout


# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    app.layout= graph()
    app.run_server(debug=True)