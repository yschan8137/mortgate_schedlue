import dash
import dash_bootstrap_components as dbc

app = dash.Dash()

app.layout = dbc.Container([
    dbc.InputGroup(
        dbc.Input(id='my-input', placeholder='Enter a value'),
        loading_state={
            'is_loading': False,
            'message': 'No data to load',
            'color': 'secondary',
        },
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)