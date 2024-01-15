"""Build a graph for the loan"""
from itertools import accumulate
from dash import Dash, dcc, callback, Output, Input, State, ALL, callback_context, html
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import plotly.express as px
import dash_mantine_components as dmc
from plotly.subplots import make_subplots

import sys
sys.path.append('./')

from app.Dashboard.assets.ids import GRAPH, LOAN
from app.Loan import df_schema, merge_sublist


def graph():
    """Build the graph"""
    layout = html.Div(
        [
            html.Div(
                id= 'information-dashboard',
                children= [
                    # dmc.Stack(
                    #     id= 'information-dashboard',
                    #     spacing= 20,
                    #     children= [
                    #         dmc.Skeleton(
                    #             height= 100,
                    #             circle= True,
                    #             children= [],
                    #         ),
                    #         dmc.Skeleton(height= 15, width="90%"),
                    #         dmc.Skeleton(height= 15, width="90%"),
                    #         dmc.Skeleton(height= 15, width="70%"),
                    #     ],
                    # )
                ],
                style= {
                    # 'display': 'flex',
                    'height': '40%',
                    'background-color': 'white',
                    'box-shadow': '0 0 5px #ccc',
                    'border-radius': '5px',
                    'border': '1px solid #ccc',
                    'shadow': '0 0 5px #ccc',
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

    @callback(
        Output('information-dashboard', 'children'),
        # Input(GRAPH.LINE, 'hoverData'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        # State('menu-target', 'children')
    )
    def update_info(
        memory, 
        ):
        if memory:
            memory = memory['data']
            demostrated_items= [df_schema.level_2.PAYMENT, df_schema.level_2.PRINCIPAL, df_schema.level_2.INTEREST]
            pie_data = {
                df_schema.level_1.EPP: {
                    'labels': [],
                    'values': []
                },
                df_schema.level_1.ETP: {
                    'labels': [],
                    'values': []
                },
                df_schema.level_2.PAYMENT: {
                    df_schema.level_1.EPP: [],
                    df_schema.level_1.ETP: []
                },
            }

            for key, value in {k: round(v) for k, v in zip(map(lambda x: tuple(x), memory['columns']), memory['data'][-1]) if k[-1] in demostrated_items}.items():
                if key[-1] != df_schema.level_2.PAYMENT:
                    if len(key) > 2:
                        if 'names' not in pie_data[key[-2]]: # avoid errors raised by the restriction regarding the same length of arrays in composing the pie chart.
                            pie_data[key[-2]].update({'names': [key[0]]})
                        else:
                            pie_data[key[-2]]['names'].append(key[0])
                    pie_data[key[-2]]['labels'].append(key[-1])
                    pie_data[key[-2]]['values'].append(value)
                elif key[-1] == df_schema.level_2.PAYMENT:
                    pie_data[key[-1]][key[-2]].append(value)
                    summary = sum(pie_data[key[-1]][key[-2]])
                    pie_data[key[-1]][key[-2]] = [summary]

            fig = make_subplots(rows=1, cols=len({k for k in pie_data.keys() if k != df_schema.level_2.PAYMENT}), specs=[[{'type':'domain'}, {'type':'domain'}]])

            for col, name in enumerate({k for k in pie_data.keys() if k != df_schema.level_2.PAYMENT}):
                for label in pie_data[name]['labels']:
                    fig.add_trace(
                        px.pie(
                            pie_data[name], 
                            values='values', 
                            names='labels', 
                            title=name, 
                            opacity= .8,
                            color= 'labels',
                            color_discrete_sequence= px.colors.qualitative.D3,
                            ).data[0], 
                            1, 
                            col + 1,
                    )
            fig.update_traces(
                hole= .7,
                hoverinfo="label+percent+name"
            )
            fig.update_layout(
                title_text="<b>Total Payment</b>", 
                template= 'seaborn',
                annotations=[
                    dict(
                        text= f"""
                                <b>{round(pie_data[df_schema.level_2.PAYMENT][name][0] // len(memory['data'])): ,}</b>
                                 <br><b>{name}</b><br>
                        """,
                        align='center', 
                        x= 0.08 + 0.84 * n,
                        y=0.4, 
                        xref='paper', # [paper, x, x2, x3]
                        font_size=20, 
                        showarrow=False,
                        ax=0,
                        ay=0
                        ) 
                        for n, name in enumerate([k for k in pie_data.keys() if k != df_schema.level_2.PAYMENT])
                ] + [dict(
                        text= """<b>平均償還金額:</b><br>""",
                        x= 0.195 + 0.615 * n,
                        y=0.58,
                        font_size=13,
                        showarrow=False,
                        ax=0,
                        ay=0,
                        font_color= px.colors.qualitative.D3[9],
                    ) for n in range(len([k for k in pie_data.keys() if k != df_schema.level_2.PAYMENT]))],
                # showlegend=False
            )
            # fig= px.pie(
            #     pie_data,
            #     values='value',
            #     names='items',
            #     hole= 0.8,
            #     opacity= 0.8,
            #     color_discrete_sequence= px.colors.sequential.RdBu,
            #     template='seaborn',
            #     facet_col= 'repay_method',
            # )
            # fig.update_layout(
            #     showlegend= True,
            #     legend= dict(
            #         orientation= 'v',
            #         yanchor= 'bottom',
            #         y= 1.02,
            #         xanchor= 'right',
            #         x= 1,
            #     ),
            #     margin= dict(l=20, r=10, t=35, b=40),
            #     paper_bgcolor= 'rgba(0, 0, 0, 0)',
            #     plot_bgcolor= 'rgba(0, 0, 0, 0)',
            # )
            # fig.update_traces(
            #     texttemplate='%{percent:.2%}',
            #     textposition='inside',
            #     textinfo='percent+label',
            #     hovertemplate= '%{label}: %{value:,}',
            # )
            # fig= px.bar(
            #     pie_data,
            #     x= 'method',
            #     y= 'value',
            #     text= 'items',
            #     text_auto= True,
            #     color= 'items',
            #     orientation= 'v',
            #     opacity= 0.8,
            #     color_discrete_map= {
            #         'principal': 'gold',
            #         'interest': 'royalblue',
            #         'residual': 'mediumturquoise',
            #     },
            #     template= 'seaborn',
            # )
            # fig.update_layout(
            #     showlegend= True,
            #     margin= dict(l=10, r=10, t=10, b=10),
            #     paper_bgcolor= 'rgba(0, 0, 0, 0)',
            #     plot_bgcolor= 'rgba(0, 0, 0, 0)',
            # )
            # fig.update_xaxes(
            #     visible= True,
            #     showticklabels= True,
            #     title= None,
            # )
            # fig.update_yaxes(
            #     range= [0, sum(pie_data['value']) * 1.1 / 2],
            #     visible= False,
            #     showticklabels= False,
            # )
            # fig.update_traces(
            #     texttemplate= '%{value:,}',
            #     width= 0.4,
            #     textangle= 0,
            # )
            return dcc.Graph(
                figure= fig,
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
            ),
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
