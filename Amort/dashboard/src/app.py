from dash import Dash, dcc, html, register_page
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from .design import homepage
from .design.components import styles, ids, className
from .data.source import DataSource


# 2022/11/6 
# test: py -m Amort.tests.dashboard.layout
external_stylesheets = ['./assets/style.css']
    # [
    # Dash CSS
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    # 'https://codepen.io/chriddyp/pen/brPBPO.css']


def sidebar(
    app: Dash,
    source= DataSource, 
    style: dict= {
        'content': styles.CONTENT_STYLE,
        'sidebar': styles.SIDEBAR_STYLE,
    },
    ) -> None:
    app.layout= html.Div([
        dcc.Location('url'),
        html.Div([
            html.H2('【測試】側邊欄', className= className.SIDE_BAR), 
            html.Hr(),
            html.P(
                '【測試】側邊欄選項', className= className.LEAD,
                ),
                dbc.Nav(
                    [
                        dbc.NavLink('Home', href= "/home", active= "exact", external_link=True),
                        dbc.NavLink('Page 1', href= "/page-1", active= "exact"),
                        dbc.NavLink('Page 2', href= "/page-2", active= "exact"),
                    ],
                    vertical= True,
                    pills= True,
                ),
                ],
                style= styles.SIDEBAR_STYLE, 
        ),
        content := html.Div(
            id= ids.PAGE_CONTNET, 
            style= styles.CONTENT_STYLE
            ),
        ]
    )

    @app.callback(
        Output(ids.PAGE_CONTNET, 'children'),
        Input('url', 'pathname'), 
        )
    def render_page_content(pathname):
        if pathname == '/home':
            return homepage.render(app, source)
        elif pathname == '/page-1':
            return html.P('This is the page of the page 1. Ya!!')
        elif pathname == '/page-2':
            return html.P('This is the page of the page 2!')
        return html.Div([
            html.H1('404: Not Found', className= className.TEXT_DANGER),
            html.Hr(),
            html.P(f'The pathname {pathname} was not recognized.')
        ],
        className= className.P3)
    return app.run(debug= True)

# py -m Amort.dashboard.src.layout
if __name__ == "__main__":
    app = Dash(
        __name__, 
        # use_pages= True, 
        external_stylesheets= external_stylesheets, 
        suppress_callback_exceptions=True
        )
    app.layout = sidebar(app)
    app.run_server(debug= True)