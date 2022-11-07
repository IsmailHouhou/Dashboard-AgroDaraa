import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages import farm_dashboard, energy_dashboard, security_dashboard, home

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

sidebar = html.Div(id="navbar", children=
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Farm", href="/farm", active="exact"),
                dbc.NavLink("Energy", href="/energy", active="exact"),
                dbc.NavLink("Security", href="/security", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
)

content = html.Div(id="page_content")

def serve_layout():
    return html.Div([dcc.Location(id="url"), sidebar, content])

app.layout = serve_layout


# Hide sidebar when at Home
@app.callback(
    Output("page_content", "id"),
    Output("navbar", "id"),
    Input("url", "pathname")
)
def page_content_extention(pathname):
    if pathname== '/':
        return 'home_page_content', 'home_navbar_display'
    else:
        return 'page_content', 'navbar'


# Navigation Sidebar
@app.callback(Output("page_content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/farm":
        return farm_dashboard.layout
    elif pathname == "/energy":
        return energy_dashboard.layout
    elif pathname == "/security":
        return security_dashboard.layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)