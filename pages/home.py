from dash import dcc, html


layout = html.Div(children=[
    html.H3("click here to go to the farm dashboard"),
    dcc.Link(html.Button("Farm"), href="/farm", refresh=True),
    dcc.Link(html.Button("Energy"), href="/energy", refresh=True),
    dcc.Link(html.Button("security"), href="/security", refresh=True),
])