import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input, State, MATCH, ALL, callback_context, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

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
        resource_data,
        ):
        level_0 = {c[0] for c in resource_data['columns']}
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

# update label of the dropdown menu
    # @callback(
    #     Output('menu-target', 'children'),
    #     Output('menu-target', 'rightIcon'),
    #     Output('menu-target', 'loading'),
    #     Input(GRAPH.LINE, 'figure'),
    # )
    # def update_label_for_dropdownmune(fig):
    #     if fig['data']:
    #         text = [*{data['legendgroup'] for data in fig['data']}][-1]
    #         if text == df_schema.level_0.TOTAL:
    #             return text, [], False
    #         else:
    #             return text, DashIconify(icon="raphael:arrowdown"), False
    #     else:
    #         raise PreventUpdate

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
        resource_data,
        _,
        label,
        ):
        ctx= callback_context
        fig= go.Figure(
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
        )
        df = pd.DataFrame.from_dict(resource_data, 'tight')[1:-1]
        if isinstance(ctx.triggered_id, dict):
            chosen_figure= ctx.triggered_id['index']
        else:
            #if df_schema.level_0.TOTAL in [*df.columns.levels[0]]: # type: ignore
             #   chosen_figure = df_schema.level_0.TOTAL
            #else:
            #    if accum == 'cumulative':
            #        if label== df_schema.level_2.RESIDUAL:
            #            chosen_figure= df_schema.level_2.PAYMENT
            #        else:
            #            chosen_figure= label
            #    else:
            #        chosen_figure= (label if label != df_schema.level_0.TOTAL else df_schema.level_2.PAYMENT)
            if df_schema.level_0.TOTAL not in [*df.columns.levels[0]]: #type: ignore
                if accum == 'cumulative':
                    if label== df_schema.level_2.RESIDUAL:
                        chosen_figure= df_schema.level_2.PAYMENT
                    else:
                        chosen_figure= label
                else:
                    chosen_figure= (label if label != df_schema.level_0.TOTAL else df_schema.level_2.PAYMENT)
            else:
                chosen_figure = df_schema.level_0.TOTAL
        for col in df.columns:
            if chosen_figure in col:
                dff= df[col].apply(lambda x: round(x, 0))
                method= (" + ".join([co for co in col if co != chosen_figure]) if len(col) > 2 else col[0])
                if accum == 'cumulative':
                    dff = dff.cumsum().apply(lambda x: round(x))
                x_axis_value= dff.index
                fig.add_trace(
                    go.Scatter(
                        x= x_axis_value,
                        y= dff.values,
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
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', type= 'log', tickformat= ',.0f', rangemode= 'tozero')
        fig.update_layout(
            autosize= False,
            width= 1050,
            height= 600,
            showlegend= False,
            hovermode= 'x',
        )
        return fig, chosen_figure, (DashIconify(icon="raphael:arrowdown") if chosen_figure != df_schema.level_0.TOTAL else None), False, ({"from": "teal", "to": "blue", "deg": 60} if chosen_figure == df_schema.level_0.TOTAL else {"from": "indigo", "to": "cyan"})
    return layout


# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    app.layout= graph()
    app.run_server(debug=True)