from dash import Dash, html
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


app.layout = html.Div(
                 [
                     dbc.Button(className="bi bi-plus-lg rounded-circle", outline= True, color="primary"),
                     dbc.Button(className="bi bi-trash  rounded-circle m-4", outline= True, color="primary"),
                 ],
             )

#py -m Amort.test.AddandDeleteButton
if __name__ == "__main__":
    app.run_server(debug=True)
