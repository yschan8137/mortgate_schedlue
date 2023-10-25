import pandas as pd
from dash import Dash, dcc, html, callback, Output, Input, State, MATCH, ALL, no_update, callback_context
from dash_iconify import DashIconify
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import datetime
from dateutil.relativedelta import relativedelta

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
                    dbc.DropdownMenu(
                        id= GRAPH.DROPDOWN.MENU,
                        color= '#CECECE', # color of the label background.
                        style={
                            # 'width': '110px',
                            "borderColor": "#ff0000",
                            'margin-left': '6%'
                        },
                        size= 'md',
                        toggle_style={
                            'width': '100px',
                            "color": "#162126", 
                            'font-weight': 'bold',
                            'box-shadow': '0 0 5px #ccc',
                            'border': '1px solid #ccc',
                            'border-radius': '5px',
                        },
                        toggleClassName= "border None text-align justify middle",
                    ),
                    dmc.SegmentedControl(
                        id=GRAPH.ACCUMULATION,
                        value="regular",
                        data=[
                            {"value": "regular", "label": "Regular"},
                            {"value": "cumulative", "label": "Cumulative"},
                        ],
                        # mt=5,
                        size= 'sm',
                        style= {
                            'background-color': "rgba(0, 62, 143, 0.29)",
                            'box-shadow': '0 0 5px #ccc',
                            'border': '1px solid #ccc',
                            'border-radius': '5px',
                        },
                    ),
                ],
                # direction= 'horizontal',
                spacing= 10,
                position= 'left',
                style= {
                }
            ),
            dbc.Col(
                dcc.Graph(id= GRAPH.LINE),
            ),
        ],
        fluid=True,
        style= {
            'margin-top': '5px',
        }
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
        if accum and accum == 'cumulative':
            init_columns= [v for v in init_columns if v != df_schema.level_2.RESIDUAL]
        return [dbc.DropdownMenuItem(children= column, id= {'index': column, 'type': GRAPH.DROPDOWN.ITEM}) for column in init_columns if column != label]

# update label of the dropdown menu
    @callback(
        Output(GRAPH.DROPDOWN.MENU, 'label'),
        Input(GRAPH.LINE, 'figure'),
    )
    def update_label_for_dropdownmune(fig):
        return [*{data['legendgroup'] for data in fig['data']}][-1]


# update the results
    @callback(
        Output(GRAPH.LINE, 'figure'),
        Input(GRAPH.ACCUMULATION, 'value'),
        Input(LOAN.RESULT.DATAFRAME, 'data'),
        Input({'index': ALL, 'type': GRAPH.DROPDOWN.ITEM}, 'n_clicks'),
        Input(LOAN.DATE, 'value'),
        State(GRAPH.DROPDOWN.MENU, 'label'),
        State(GRAPH.LINE, 'figure'),
    )
    def _graph(
        accum, 
        resource_data,
        _,
        date,
        label,
        fig
        ):
        print(f'date on line 133 in Graph.app is {date}')
        try:
            start_date= datetime.datetime.strptime(date, '%Y-%m-%d')
        except:
            start_date = None
        ctx= callback_context
        if isinstance(ctx.triggered_id, dict):
            chosen_figure= ctx.triggered_id['index']
        else:
            if label:
                if accum == 'cumulative':
                    if label== df_schema.level_2.RESIDUAL:
                        chosen_figure= df_schema.level_2.PAYMENT
                    else:
                        chosen_figure= label
                else:
                    chosen_figure= label
            else:
                chosen_figure= df_schema.level_2.PAYMENT
        df = pd.DataFrame.from_dict(resource_data, 'tight')[1:-1]
        fig= go.Figure()

        for method in [*{*df.columns.get_level_values(0)}]:
            dff = df[method]
            if accum == 'cumulative':
                dff = dff.cumsum().apply(lambda x: round(x))
            filtered_dff= dff[chosen_figure].apply(lambda x: round(x, 0))
            if start_date:
                x_axis_value= [start_date + relativedelta(months=n) for n in filtered_dff.index]
            else:
                x_axis_value= filtered_dff.index
            fig.add_trace(
                go.Scatter(
                    x= x_axis_value,
                    y= filtered_dff.values,
                    legendgroup= chosen_figure,
                    legendgrouptitle_text= chosen_figure,
                    name= method,                   
                    mode= 'lines',
                    connectgaps= True,
                    fill= ('tonexty' if accum == 'cumulative' else None),
                    stackgroup= (method if accum == 'cumulative' else None),
                    text= [method]* len(x_axis_value),
                    hovertemplate =
                        "<br><b>%{text}</b>" +
                        ("<br><b>Date</b>: %{x: %d-%M-%Y}" if start_date else "<br><b>Time</b>: %{x}") + 
                        "<br><b>Amount</b>: %{y:,}" +
                        "<extra></extra>",
                ),
            )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_layout(
            showlegend= False,
            height= 500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255, 0.3)',
            legend= {
                'groupclick': 'toggleitem',
            },
            modebar= {
                'bgcolor': 'rgba(255, 255, 255, 0.3)',
                'activecolor':'gray',
            },
            margin= {'t': 30},
            hovermode= 'x',

        )
        return fig
    return layout


# py -m app.Dashboard.pages.components.Graphic.app
if __name__ == '__main__':
    app.layout= graph()
    app.run_server(debug=True)