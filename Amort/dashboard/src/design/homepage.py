from dash import Dash, dcc, html
import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from .components import ids, className
from ....dashboard import amortization_types

# 整合所有資料來源至data.source
def to_dropdown_options(values: list[str]) -> list[dict[str, str]]:
    return [{"label": value, "value": value} for value in values]
    

def render(app: Dash, source: DataSource= DataSource) -> html.Div:
    @app.callback(
            Output(ids.DROPDOWN_METHODS, "value"),
            Input(ids.REFRESH_ALL_METHODS, "n_clicks"),
            )
    def refresh_all_methods(_: int) -> list[str]:
        return [*amortization_types]

    return html.Div(
        children= [
            html.H6(i18n.t("generel.methods")),
            dcc.Dropdown(
                id= ids.DROPDOWN_METHODS,
                options= to_dropdown_options([*amortization_types]),
                value= [*amortization_types],
                multi= True,
            ),
            html.Button(
                className= className.DROPDOWN_BUTTON,
                children= [i18n.t("refresh.select_all")],
                id= ids.REFRESH_ALL_METHODS,
                n_clicks= 0,
            )
        ]
    )

# py -m Amort.dashboard.src.design.homepage
if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = render(app)
    app.run_server(debug= True)