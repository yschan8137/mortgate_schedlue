from Amort.loan import calculator

from dash import Dash, dcc, html, page_registry, page_container
import dash_bootstrap_components as dbc
from Amort.multipages import amortization

app= Dash(
    __name__, 
    use_pages= True, 
    external_stylesheets= [dbc.themes.SPACELAB])

server= app.server

# sidebar= dbc.Nav(
#     [
#         dbc.NavLink(
#             [
#                 html.Div(page['name'], className= 'ms-2'),
#             ],
#             href= page['path'],
#             active= 'exact',
#         ) for page in page_registry.values()
#     ],
#     vertical= True,
#     pills= True,
#     className= 'bg-light',
# )

# app.layout= dbc.Container(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(html.Div('dash多頁面測試', style= {'fontSize': 50, 'textAlign': 'center'}))
#             ]
#         ),

#         html.Hr(),

#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         sidebar
#                     ], xs= 4, sm= 4, md= 2, lg= 2, xl= 2, xxl= 2
#                 ),
#                 dbc.Col(
#                     [
#                         page_container
#                     ], xs= 8, sm= 8, md= 10, lg= 10, xl= 10, xxl= 10
#                 )
#             ]
#         )

#     ], fluid= True
# )

# py -m Amort.multipages.app
if __name__ == '__main__':
    app.run(debug= True)