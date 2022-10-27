import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import dash_daq as daq

#data import
weather_data = pd.read_csv('weatherHistory.csv')

#data Formatting
weather_data['Formatted Date'] = pd.to_datetime(weather_data['Formatted Date'].str[:-10])
weather_data = weather_data.sort_values(by='Formatted Date', ascending=False)
weather_data = weather_data.set_index('Formatted Date')

#Data summeries
hourly_summary = weather_data.resample('H').mean()
daily_summary = weather_data.resample('D').mean()
weekly_summary = weather_data.resample('W').mean()


#Update layout params
date_buttons = [
    {'count': 1, 'step': 'day', 'stepmode': 'backward', 'label': '1D'},
    {'count': 7, 'step': 'day', 'stepmode': 'backward', 'label': '1W'},
    {'count': 1, 'step': 'month', 'stepmode': 'backward', 'label': '1M'},
    {'count': 1, 'step': 'year', 'stepmode': 'backward', 'label': '1Y'},
    {'step': 'all', 'label': 'All'}
]

# #Graphs (Line)
# line_temp_fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
# line_temp_fig.append_trace(go.Scatter(x=weather_data['Formatted Date'], y=weather_data['Temperature (C)'], mode='lines', name='Air Temp'), row=1, col=1)
# line_temp_fig.append_trace(go.Scatter(x=weather_data['Formatted Date'], y=weather_data['Apparent Temperature (C)'], mode='lines', name='Apparent Air Temp'), row=1, col=1)
# line_temp_fig.append_trace(go.Scatter(x=weather_data['Formatted Date'], y=weather_data['Humidity'], mode='lines', name='Humidity'), row=2, col=1)
# line_temp_fig.update_xaxes(title_text='Date')
# line_temp_fig.update_layout(
#     {'xaxis':
#         {'rangeselector':
#             {'buttons': date_buttons}}}
# )

line_temp_fig_2 = go.Figure()
# line_temp_fig_2.add_trace(go.Scatter(x=weather_data.index, y=weather_data['Temperature (C)'], mode='lines'))
# line_temp_fig_2.update_xaxes(title_text='Date')
# line_temp_fig_2.update_yaxes(title_text='Temperature (C)')
# line_temp_fig_2.update_layout(
#     {'xaxis':
#         {'rangeselector':
#             {'buttons': date_buttons,
#             'bgcolor': 'black'}
#         }
#     },
#     margin={'l': 20, 'r': 20, 't': 20, 'b': 20},
#     paper_bgcolor= '#1f2c56',
#     font_color= 'white',
#     title={
#         'text': "Temperature history over time",
#         'y':0.9,
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top',
#     },
#     updatemenus=[
#         dict(
#             type="buttons",
#             direction="down",
#             x=1.1,
#             y=0.8,
#             showactive=True,
#             font={'color': '#192444'},
#             bgcolor='#BBB',
#             buttons=list(
#                 [
#                     dict(
#                         label="H",
#                         method="update",
#                         args=[{
#                             "x": [hourly_summary.index],
#                             "y": [hourly_summary['Temperature (C)']]
#                         }],
#                     ),
#                     dict(
#                         label="D",
#                         method="update",
#                         args=[{
#                             "x": [daily_summary.index],
#                             "y": [daily_summary['Temperature (C)']]
#                         }],
#                     ),
#                     dict(
#                         label="W",
#                         method="update",
#                         args=[{
#                             "x": [weekly_summary.index],
#                             "y": [weekly_summary['Temperature (C)']]
#                         }],
#                     ),
#                 ]
#             ),
#         )
#     ]
# )


#Graphs (Indicator)
indicator_fig_1 = go.Figure()
indicator_fig_1.add_trace(go.Indicator(
    mode = "gauge+number+delta",
    # value = weather_data['Wind Speed (km/h)'][0],
    value = 88,
    number = {'suffix': ' km/h', 'font':{'size': 20}},
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Speed of wind", 'font':{'size': 18}},
    delta = {'reference': 50, 'font': {'size': 16}},
    gauge = {
        'axis': {'range': [0, 99], 'tickwidth': 2, 'tickcolor': '#192444'},
        'bar': {'color': '#192444'},
        'borderwidth': 0,
        'bordercolor': '#192444',
        'steps': [
            {'range': [0, 50], 'color': '#636efa'},
            {'range': [50, 80], 'color': 'orange'},
            {'range': [80, 100], 'color': 'red'},

        ],
    }
))
indicator_fig_1.update_layout(
    paper_bgcolor= '#1f2c56',
    font_color= 'white',
    margin={'l': 20, 'r': 20, 't': 50, 'b': 20},
)

indicator_fig_2 = daq.Gauge(
    color={
        'default': 'white',
        'gradient':False,
        'ranges': {"#636efa":[0,50],"orange":[50,80],"red":[80,100]},
    },
    size=180,
    showCurrentValue=True,
    value=88,
    scale={'start': 0, 'interval': 10, 'labelInterval': 2},
    label={'label': 'Wind Speed (km/h)', 'style': {'font-size': '20px'}},
    min=0,
    max=100,
)

# indicator_fig_3 = go.Figure()
# indicator_fig_3.add_trace(go.Indicator(
#     mode = "gauge+number",
#     value = 60,
#     number = {'suffix': ' km/h'},
#     domain = {'x': [0, 1], 'y': [0, 1]},
#     title = {'text': "Speed of wind (km/h)"}
# ))
# indicator_fig_3.update_layout(
#     paper_bgcolor= '#1f2c56',
#     font_color= 'white',
# )


# Dashboard web app
app = Dash(__name__)

#App Layout
app.layout = html.Div(id='major_container', children=[
    html.Div(id='live_data_container', children=[
        html.Div(className='live_data', children=[
            html.H3("Air Temp"),
            html.Span(round(weather_data['Temperature (C)'][0], 2)),
            html.Span(' C')
        ]),
        html.Div(className='live_data', children=[
            html.H3("GreenHouse Temp"),
            html.Span(round(weather_data['Apparent Temperature (C)'][0], 2)),
            html.Span(' C')
        ]),
        html.Div(className='live_data', children=[
            html.H3("Humidity"),
            html.Span(round(weather_data['Humidity'][0], 2))
        ]),
        html.Div(className='live_data', children=[
            html.H3("Wind Speed"),
            html.Span(round(weather_data['Wind Speed (km/h)'][0], 2)),
            html.Span(' km/h')
        ]),
        html.Div(className='live_data', children=[
            html.H3("Wind Direction"),
            html.Span(round(weather_data['Wind Bearing (degrees)'][0], 2))
        ]),
    ]),

    html.Div(id='camera_indicator', children=[
        html.Div(id='camera_container', children=[
            dcc.Dropdown(id='camera_dropdown',
                options=[
                    {'label': 'Camera 1', 'value': 'assets/img1.jpg'},
                    {'label': 'Camera 2', 'value': 'assets/img2.jpg'}
                ],
                value = 'assets/img1.jpg',
                clearable = False
            ),
            # html.H2(className='container_title', children=['Farm Cameras']),
                # html.H2('Camera 1'),
                html.Img(id='farm_image', src=app.get_asset_url('img1.jpg'))
        ]),
        html.Div(id='indicator_container', children=[
            dcc.Graph(className='indicator', figure=indicator_fig_1),
            indicator_fig_2,
            # dcc.Graph(className='indicator', figure=indicator_fig_3),
        ]),
    ]),
    

    html.Div(id='history', children=[
        # html.Div(
        #     dcc.Graph(className='line_graph', figure=line_temp_fig)
        # ),
        html.Div(className='graph_container', children=[
            dcc.Dropdown(id='line_plot_dropdown',
                options=[
                    {'label': 'Temperature', 'value': 'Temperature (C)'},
                    {'label': 'Apparnet Temp', 'value': 'Apparent Temperature (C)'},
                    {'label': 'Humidity', 'value': 'Humidity'}
                ],
                value = 'Temperature (C)',
                clearable = False
            ),
            dcc.Graph(
                id='dynamic_plot',
                figure=line_temp_fig_2,
                config={
                    'displayModeBar': False
                }
            )
        ])
    ])
])

# Camera Callback
@app.callback(
    Output(component_id='farm_image', component_property='src'),
    Input(component_id='camera_dropdown', component_property='value')
)
def update_image(option):
    src='assets/img1.jpg'
    if option:
        src=option
    return src

# Plot Callback
@app.callback(
    Output(component_id='dynamic_plot', component_property='figure'),
    Input(component_id='line_plot_dropdown', component_property='value')
)
def update_plot(option):
    title='Temperature (C)'
    if option:
        title = option
    line_plot = go.Figure(go.Scatter(x=weather_data.index, y=weather_data[title], mode='lines'))
    line_plot.update_xaxes(title_text='Date')
    # line_plot.update_yaxes(title_text=f'{title}')
    line_plot.update_layout(
        {'xaxis':
            {'rangeselector':
                {'buttons': date_buttons,
                'bgcolor': '#141d36'}
            }
        },
        margin={'l': 20, 'r': 20, 't': 50, 'b': 20},
        paper_bgcolor= '#1f2c56',
        font_color= 'white',
        title={
        'text': f"{option} history over time",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                x=1.1,
                y=1,
                showactive=True,
                font={'color': '#192444'},
                bgcolor='#BBB',
                # pad={'l': 5, 'r': 5, 't': 5, 'b': 5},
                buttons=list(
                    [
                        dict(
                            label="H",
                            method="update",
                            args=[{
                                "x": [hourly_summary.index],
                                "y": [hourly_summary[title]]
                            }],
                        ),
                        dict(
                            label="D",
                            method="update",
                            args=[{
                                "x": [daily_summary.index],
                                "y": [daily_summary[title]]
                            }],
                        ),
                        dict(
                            label="W",
                            method="update",
                            args=[{
                                "x": [weekly_summary.index],
                                "y": [weekly_summary[title]]
                            }],
                        ),
                    ]
                ),
            )
        ]
    )
    return line_plot


if __name__ == '__main__':
    app.run_server(debug=True)
