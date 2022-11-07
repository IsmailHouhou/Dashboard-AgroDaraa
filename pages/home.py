from dash import dcc, html


layout = html.Div(id='home_div', children=[
    dcc.Link("Farm", href="/farm", refresh=True, className='home_button'),
    dcc.Link("Energy", href="/energy", refresh=True, className='home_button'),
    dcc.Link("security", href="/security", refresh=True, className='home_button'),
])