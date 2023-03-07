import i18n
from dash import Dash
import dash_bootstrap_components as dbc
import os, sys
# from .src.data.source import DataSource
from .src.app import sidebar

LOCALE= 'nl'

# py -m  Amort.multipages.main
def main() -> None:
    # default file format: {namespace}.{locale}.{format}
    # locale: 語言環境
    # 設定語言環境
    i18n.set("locale", LOCALE)
    # 設定載入路徑
    # i18n.load_path.append('locale')
    i18n.load_path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale'))

    app = Dash(__name__, use_pages= True,external_stylesheets= [dbc.BOOTSTRAP], suppress_callback_exceptions=True)
    app.title= i18n.t("general.app_title")
    app.layout= sidebar(app)
    app.run()

# py -m Amort.dashboard.main
if __name__ == "__main__":
    main()