import dash_core_components as dcc
import dash_html_components as html

def _generate_dropdown():

    forex_list = ['GBPUSD','EURGBP','EURUSD','AUDUSD','AUDJPY','USDJPY']

    dropdown_options = [{'label': currency, 'value': currency} for currency in forex_list]

    return html.Div([
        dcc.Dropdown(
            id='currency-dropdown',
            options=dropdown_options,
            value='GBPUSD'
        ),
        dcc.Store(id='current-currency',data='GBPUSD')
        ],
        style={"width": "10%"}
    )

def _generate_candlestick_monthly():

    return html.Div([
        dcc.Graph(
            id="candlestick-30d-fig"
        )
    ])

def generate_layout():

    return html.Div([
        html.H1(children='Hello World'),
        _generate_dropdown(),
        _generate_candlestick_monthly()
    ])