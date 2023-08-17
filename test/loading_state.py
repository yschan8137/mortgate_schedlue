import dash
from dash import dash_table, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

# Initialize the app
app = dash.Dash(__name__)

# Assume we have a DataFrame 'df'
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

app.layout = html.Div([
    dcc.Input(id='input', min= 1, value='1', type='number'),
    html.Div(
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        ),
        id='table-container',
        className='fade'
    )
])

# Callback to hide DataTable
@app.callback(Output('table', 'style_data'),
              Input('input', 'value'),
              prevent_initial_call=True
              )

def hide_table(data):
    return {
            'opacity': 0, 
            'backgroundColor': 'rgb(30, 30, 30)'
            }


# Callback to update DataTable
@app.callback(Output('table', 'data'),
              Output('table', 'style_data', allow_duplicate=True),
              Input('input', 'value'),
              delay= 500,
              prevent_initial_call=True
)
def update_table(value):
    dff= pd.DataFrame(columns= ['A', 'B'])
    if value:
      dff['A'] = df['A'].apply(lambda x: x* int(value))
      dff['B'] = df['B'].apply(lambda x: x* int(value))
    else:
      dff= df
    return dff.to_dict('records'), {'opacity': 1, 'backgroundColor': 'rgb(100, 100, 100)'}

if __name__ == '__main__':
    app.run_server(debug=True)
