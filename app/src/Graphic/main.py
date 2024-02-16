"""Build a graph for the loan"""
from itertools import accumulate
from dash import Dash, html, dcc, callback, Output, Input, State, ALL, callback_context, Patch, no_update
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
import dash_mantine_components as dmc
from plotly.subplots import make_subplots

import sys
sys.path.append('./')

from app.assets.ids import GRAPH, LOAN
from app import df_schema


def graph():
    """
    Build the graph
    Args:
        locale (str): The language of the graph. 
        Available options are ['en', 'zh_TW'], which represents English and Tranditional Chinese respectively.
    """

    layout = html.Div(
        [
            dmc.LoadingOverlay(    
                html.Div(
                    id= 'information-dashboard',
                    children= [],
                    style= {
                        'display': 'flex',
                        'flex-direction': 'row',
                        'width': '100%',
                        'height': '100%',
                        'background-color': 'white',
                        'border-radius': '5px',
                        'border': '1px solid #ccc',
                        'box-shadow': '0 0 5px #ccc',
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                        'justify-content': 'center',
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
                                            children= df_schema.level_2.PAYMENT['en'],
                                            rightIcon= DashIconify(icon="raphael:arrowdown"),
                                            variant="gradient",
                                            gradient={"from": "indigo", "to": "cyan"},
                                            loading={'loading_type': 'overlay'},
                                            loaderPosition='center',
                                            loaderProps={"variant": "dots",
                                                         "color": "white", "size": "sm"},
                                            n_clicks= 0,
                                        ),
                                    ),
                                    dmc.MenuDropdown(
                                        [],
                                        id='menu-dropdown',
                                    ),
                                ],
                                id=GRAPH.DROPDOWN.MENU,
                            ),
                            dcc.Store(id='menu-locale', data={}),
                            dmc.SegmentedControl(
                                id=GRAPH.ACCUMULATION,
                                value="regular",
                                data=[
                                    {"value": "regular", "label": {'en': "Regular", 'zh_TW': '一般'}['en']},
                                    {"value": "cumulative", "label": {'en': 'Cumulative', 'zh_TW': '累計'}['en']},
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
                        {'en': 'spreadsheet', 'zh_TW': '試算表'}['en'], 
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
                    style={
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
                style={
                    'display': 'flex',
                    'flex-direction': 'row',
                    'width': '100%',
                    'height': '55%',
                    'background-color': 'white',
                    'border-radius': '5px',
                    'border': '1px solid #ccc',
                    'box-shadow': '0 0 5px #ccc',
                    'margin-left': 'auto',
                    'margin-right': 'auto',
                    'justify-content': 'center',
                },
            ),
        ],
        style={
            'width': '100%',
            'height': '90dvh',
        },
        className= 'custom-scrollbar',
    )

#1 options for dropdown menu of the main graph
    @callback(
            Output('menu-target', 'children'),
            Output('menu-locale', 'data'),
            Output('menu-target', 'rightIcon'),
            Output('menu-target', 'loading'),
            Output('menu-target', 'gradient'),
            Output('menu-dropdown', 'children'),
            Output('menu-dropdown', 'style'),
            Input({'index': ALL, 'type': GRAPH.DROPDOWN.ITEM}, 'n_clicks'),
            Input(GRAPH.ACCUMULATION, 'value'),
            Input(LOAN.RESULT.DATAFRAME, 'data'),
            State('menu-locale', 'data'),
            State({'index': ALL, 'type': 'locale-config'}, 'data'),
    )
    def update_dropdown_items(
        _,
        accum,
        memory,
        menu_locale,
        locale,
    ):
        memory = memory['data']
        locale= locale[-1]
        label_for_dropdown = Patch()
        level_0 = {c[0] for c in memory['columns'] if c[0] != ''} # level_0: the first level of the column
        if not menu_locale:
            menu_locale = df_schema.level_2.PAYMENT
        if df_schema.level_0.TOTAL[locale] in level_0 or not level_0:
            return label_for_dropdown, no_update, no_update, False, no_update, [], {'display': 'none'}
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
            
            dropdown_elements = [column for column in method_for_original_mortgate if column[locale] != menu_locale[locale]]
            
            dropdown = [
                dmc.MenuItem(
                    element[locale],
                    id={
                        'index': element[locale],
                        'type': GRAPH.DROPDOWN.ITEM
                    },
                ) for element in dropdown_elements
            ]  # avoid duplicate label
            label_for_dropdown = [label for label, filter in zip(dropdown_elements, _) if filter]
            
            if len(label_for_dropdown) == 0:
                label_for_dropdown = menu_locale
            else:
                label_for_dropdown = label_for_dropdown[0]
            return [
                label_for_dropdown[locale], 
                label_for_dropdown,
                (DashIconify(icon="raphael:arrowdown") if label_for_dropdown != df_schema.level_0.TOTAL else None),
                False, 
                ({"from": "teal", "to": "blue", "deg": 60} if label_for_dropdown == df_schema.level_0.TOTAL else {"from": "indigo", "to": "cyan"}),
                dropdown, 
                {'display': 'block'},
            ]

#2 update the main graph
    @callback(
        Output(GRAPH.LINE, 'children'),
        # Output('menu-locale', 'data'),
        # Output('menu-target', 'children'),
        # Output('menu-target', 'loading'),
        # Output('menu-target', 'gradient'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        Input({'index': ALL, 'type': GRAPH.DROPDOWN.ITEM}, 'n_clicks'),
        State('menu-locale', 'data'),
        State({'index': ALL, 'type': 'locale-config'}, 'data'),
        prevent_initial_call=True,
    )
    def update_graph(
        accum,
        memory,
        _,
        menu_locale,
        locale,
    ):
        ctx = callback_context
        memory = memory['data']
        locale= locale[-1]
        
        # if isinstance(ctx.triggered_id, dict) :
        #     chosen_figure = ctx.triggered_id['index']
        #     ns, cols = zip(*[(n, col) for n, col in enumerate(memory['columns']) if chosen_figure in col])
        # else:
        #     if df_schema.level_0.TOTAL[locale] not in [col[0] for col in memory['columns']]:
        #         if accum == 'cumulative':
        #             if menu_locale == df_schema.level_2.RESIDUAL:
        #                 chosen_figure = df_schema.level_2.PAYMENT
        #             else:
        #                 chosen_figure = (menu_locale if menu_locale else df_schema.level_2.PAYMENT)
        #                 # chosen_figure= label
        #         else:
        #             chosen_figure = (menu_locale if menu_locale and menu_locale != df_schema.level_0.TOTAL else df_schema.level_2.PAYMENT)
        #             # chosen_figure = (label if label != df_schema.level_0.TOTAL[locale] else df_schema.level_2.PAYMENT[locale])
        #     else:
        #         chosen_figure = df_schema.level_0.TOTAL # 總計
        if not menu_locale:
            menu_locale = df_schema.level_2.PAYMENT
        ns, cols = zip(*[(n, col) for n, col in enumerate(memory['columns']) if menu_locale[locale] in col])
        # """
        # 重新設計dropdown menu的chidren

        # """
        
        x_axis_value = memory['index'][1:-1]
        # construct the data frame for the graph
        data_frame_for_loan_timeSeries= {
            {'en': 'Time', 'zh_TW': '時間'}[locale]: [],
            {'en': 'Amount', 'zh_TW': '金額'}[locale]: [],
            {'en': 'methods', 'zh_TW': '方式'}[locale]: [],
        }
        for n, col in zip(ns, cols): # n: index of the column; col: column name
            dff = [data[n] for data in memory['data'][1:-1]]
            method = (" + ".join(
                [
                    co for co in col 
                    if co != (
                        menu_locale[locale] 
                        if isinstance(menu_locale, dict) 
                        else menu_locale
                    )
                ]
            ) if len(col) > 2 else col[0])

            if accum == 'cumulative':
                dff = [*accumulate(dff)]
            dff = [*map(lambda x: f"{round(x):,}", dff)]

            data_frame_for_loan_timeSeries[{'en': 'Time', 'zh_TW': '時間'}[locale]].extend(x_axis_value)
            data_frame_for_loan_timeSeries[{'en': 'Amount', 'zh_TW': '金額'}[locale]].extend(dff)
            data_frame_for_loan_timeSeries[{'en': 'methods', 'zh_TW': '方式'}[locale]].extend([method] * len(x_axis_value))

        fig = px.line(
            data_frame_for_loan_timeSeries,
            x= {"en": "Time", "zh_TW": "時間"}[locale], 
            y= {"en": "Amount", "zh_TW": "金額"}[locale],
            color={'en': 'methods', 'zh_TW': '方式'}[locale], 
            title='<b>{}</b>'.format({'en': 'Life of Loan', 'zh_TW': '時序圖'}[locale]), 
            log_y= True,
            line_shape="spline",
            render_mode="svg",
            hover_name= {'en': 'methods', 'zh_TW': '方式'}[locale],
            template="plotly_white",
            color_discrete_map= {
                    df_schema.level_1.ETP[locale]: '#0C82DF',
                    df_schema.level_1.EPP[locale]: '#F7DC6F',
            },
        )
        fig.update_layout(showlegend= False)

        return dcc.Graph(
            figure= fig,
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
            # chosen_figure, 
            # (chosen_figure[locale] if isinstance(chosen_figure, dict) else chosen_figure), 
            # (DashIconify(icon="raphael:arrowdown") if chosen_figure != df_schema.level_0.TOTAL[locale] else None), 
            # False, 
            # ({"from": "teal", "to": "blue", "deg": 60} if chosen_figure == df_schema.level_0.TOTAL[locale] else {"from": "indigo", "to": "cyan"})
    
# Information for avg payment.
    @callback(
        Output('information-dashboard', 'children'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        State({'index': ALL, 'type': 'locale-config'}, 'data'),
    )
    def update_info(
        memory, 
        locale,
        ):
        memory = memory['data']
        locale= locale[-1]
        if [c for c in memory['columns'] if c[0] != '']:
            # Group the data by the method of repayment which includes [Equal total payment, Equal principal payment]. 
            pie_data = {}
            payment= {}
            target= [df_schema.level_2.PAYMENT[locale], df_schema.level_2.PRINCIPAL[locale], df_schema.level_2.INTEREST[locale]]
            for n, col in enumerate(memory['columns']):
                if col[-1] in target:
                    if col[-1] != df_schema.level_2.PAYMENT[locale]:
                        if col[-2] not in pie_data.keys():
                            pie_data.update({col[-2]: {'labels': [], 'values': {}, 'names': []}}) # initialize the dictionary
                        if (col[0] if col[0] != col[-2] else None) not in pie_data[col[-2]]['names']:
                            pie_data[col[-2]]['names'].append((col[0] if col[0] != col[-2] else None))
                        if len(col) > 2:
                            if col[-3] not in pie_data[col[-2]]['values'].keys():
                                pie_data[col[-2]]['values'].update({col[-3]: []}) 
                            if col[-3]== df_schema.level_0.ORIGINAL[locale]:
                                if col[-1]== df_schema.level_2.PRINCIPAL[locale]:
                                    pie_data[col[-2]]['values'][col[0]].append(
                                        round(
                                            sum(
                                                [*map(lambda x, y: (x-y if x-y > 0 else 0), 
                                                      [
                                                          *map(lambda x: [x[n] for n, c in enumerate(memory['columns']) 
                                                                          if c[-3] == df_schema.level_0.ORIGINAL[locale] and 
                                                                            c[-2] == col[-2] and #type: ignore
                                                                            c[-1] == df_schema.level_2.PRINCIPAL[locale]][0], memory['data'][1:-1])
                                                      ], 
                                                      [
                                                          *map(lambda x: [(x[n] if x[n-1] == 0 else 0) for n, c in enumerate(memory['columns']) 
                                                                          if c[-3] == df_schema.level_0.SUBSIDY[locale] and 
                                                                            c[-2] == col[-2] and #type: ignore
                                                                            c[-1] == df_schema.level_2.RESIDUAL[locale]][0], memory['data'][1:-1])
                                                      ],
                                                    )
                                                ]
                                            )
                                        )
                                    )
                                else:
                                    pie_data[col[-2]]['values'][col[0]].append(round(memory['data'][-1][n]))
                            else:
                               pie_data[col[-2]]['values'][col[0]].append(round(memory['data'][-1][n])) 
                        else:
                            if 0 not in pie_data[col[-2]]['values'].keys():
                                pie_data[col[-2]]['values'].update({0: []})
                            pie_data[col[-2]]['values'][0].append(round(memory['data'][-1][n]))
                        pie_data[col[-2]]['labels'].append(col[-1])
                    else:
                        if col[-2] not in payment.keys():
                            payment.update({col[-2]: {'labels': [], 'values': {}, 'names': []}})
                        if (col[0] if col[0] != col[-2] else None) not in payment[col[-2]]['names']:
                            payment[col[-2]]['names'].append((col[0] if col[0] != col[-2] else None))
                        else:
                            payment[col[-2]]['values'].append(round(memory['data'][-1][n]))
                        if len(col) > 2:
                            if col[-3] not in payment[col[-2]]['values'].keys():
                                payment[col[-2]]['values'].update({col[-3]: []})
                            payment[col[-2]]['values'][col[-3]].append(sum(pie_data[col[-2]]['values'][col[-3]]))
                        else:
                            if 0 not in payment[col[-2]]['values'].keys():
                                payment[col[-2]]['values'].update({0: []})
                            payment[col[-2]]['values'][0].append(round(memory['data'][-1][n]))
                        payment[col[-2]]['labels'].append(col[-1])
            # generate the pie charts by the method of repayment
            fig = None
            fig_main= None
            fig_sub= None
            for col, method in enumerate(pie_data.keys()):
                for name in pie_data[method]['names']:
                    # without the subsidy loan
                    if name == None:
                        if not fig:
                            fig = make_subplots(rows=1, cols=len(pie_data.keys()), specs=[[{'type':'domain'}]* len(pie_data.keys())])
                        fig.add_trace(
                            go.Pie(
                                labels= pie_data[method]['labels'],
                                values= pie_data[method]['values'][0], #note 0 is a key for the dictionary.
                                title= f"""<b>{method}</b><br>{round(payment[method]['values'][0][0] // len(memory['data'][1:-1])): ,}/""" + {'en': 'Month', 'zh_TW': '月'}[locale] ,
                                name= "",
                                titlefont= dict(size= 20, color= 'dark grey'),
                                marker= dict(colors= px.colors.qualitative.Pastel1),
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
                            title_text="<b>{}</b>".format({'en': 'Avg. Payment', 'zh_TW': '平均還款'}[locale]), 
                            title_font_size= 20,
                            title_x= 0.5,
                            margin=dict(l=20, r=20, t=60, b=30),
                        )
                    # with the subsidy loan
                    else:
                        if name == df_schema.level_0.ORIGINAL[locale]:
                            if not fig_main:
                                fig_main = make_subplots(rows=1, cols=len(pie_data.keys()), specs=[[{'type':'domain'}, {'type':'domain'}]])
                            fig_main.add_trace(
                                go.Pie(
                                    labels= pie_data[method]['labels'],
                                    values= pie_data[method]['values'][name],
                                    title= f"""<b>{method}</b><br>{round(payment[method]['values'][name][0] // len(memory['data'])): ,}/""" + {'en': 'Month', 'zh_TW': '月'}[locale] ,
                                    name= "",   
                                    titlefont= dict(size= 20, color= 'dark grey'),
                                    marker= dict(colors= px.colors.qualitative.Pastel1),
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
                        elif name == df_schema.level_0.SUBSIDY[locale]:
                            if not fig_sub:
                                fig_sub = make_subplots(rows=1, cols=len(pie_data.keys()), specs=[[{'type':'domain'}]* len(pie_data.keys())])
                            fig_sub.add_trace(
                                go.Pie(
                                    labels= pie_data[method]['labels'],
                                    values= pie_data[method]['values'][name],
                                    title= f"""<b>{method}</b><br>{round(payment[method]['values'][name][0] // len(
                                        [v for v in map(lambda x: [
                                            x[n] > 0 for n, c in enumerate(memory['columns']) 
                                            if c[-3] == name and 
                                            c[-2] == method and 
                                            c[-1] == df_schema.level_2.PAYMENT[locale]][0], 
                                            memory['data'][1:-1]) if v])): ,}/月""",
                                    name= "",
                                    titlefont= dict(size= 20, color= 'dark grey'),
                                    marker= dict(colors= px.colors.qualitative.Pastel1[-2:-1]),
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
                        'border-radius': '5px',
                        'border': '1px solid #ccc',
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
            return dmc.Center(
                      children=[
                          dmc.Text(
                              "No Data Available.",
                              variant="gradient",
                              gradient={"from": "red", "to": "yellow", "deg": 45},
                              style={
                                  "fontSize": 40,
                                  },
                          )
                      ]
                  )
    return layout

# python app/Dashboard/pages/components/Graphic/main.py
# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    import dash_bootstrap_components as dbc
    from app.src.Controls.panels import panel
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
