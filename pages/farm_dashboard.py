import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html, Dash, callback
from dash.dependencies import Input, Output
import dash_daq as daq

#data import
weather_data = pd.read_csv('weatherHistory.csv')
weather_data = weather_data[['Formatted Date', 'Temperature (C)', 'Apparent Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 'Wind Bearing (degrees)', 'Visibility (km)', 'Loud Cover', 'Pressure (millibars)']]
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

line_temp_fig = go.Figure()

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


# NAV TEST
layout = html.Div(id='farm_major_container', children=[
    html.Div(id='farm_live_data_container', children=[
        html.Div(className='farm_live_data', children=[
            html.H4("Air Temp"),
            html.Div(children=[
                html.Span(round(weather_data['Temperature (C)'][0], 2)),
                html.Span(' C')
            ])
        ]),
        html.Div(className='farm_live_data', children=[
            html.H4("GreenHouse Temp"),
            html.Div(children=[
                html.Span(round(weather_data['Apparent Temperature (C)'][0], 2)),
                html.Span(' C')
            ])
        ]),
        html.Div(className='farm_live_data', children=[
            html.H4("Humidity"),
            html.Span(round(weather_data['Humidity'][0], 2))
        ]),
        html.Div(className='farm_live_data', children=[
            html.H4("Wind Speed"),
            html.Div(children=[
                html.Span(round(weather_data['Wind Speed (km/h)'][0], 2)),
                html.Span(' km/h')
            ])
        ]),
        html.Div(className='farm_live_data', children=[
            html.H4("Wind Direction"),
            html.Span(round(weather_data['Wind Bearing (degrees)'][0], 2))
        ]),
    ]),

    html.Div(id='farm_camera_indicator', children=[
        html.Div(id='farm_camera_container', children=[
            dcc.Dropdown(id='farm_camera_dropdown',
                options=[
                    {'label': 'Camera 1', 'value': 'assets/img1.jpg'},
                    {'label': 'Camera 2', 'value': 'assets/img2.jpg'}
                ],
                value = 'assets/img1.jpg',
                clearable = False
            ),
            html.Img(id='farm_image', src='assets\img1.jpg')
        ]),
        html.Div(id='farm_indicator_container', children=[
            dcc.Graph(className='farm_indicator', figure=indicator_fig_1),
            daq.Gauge(
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
            ),
        ]),
    ]),
    

    html.Div(id='farm_history', children=[
        html.Div(className='farm_graph_container', children=[
            dcc.Dropdown(id='farm_line_plot_dropdown',
                options=[
                    {'label': 'Temperature', 'value': 'Temperature (C)'},
                    {'label': 'Apparnet Temp', 'value': 'Apparent Temperature (C)'},
                    {'label': 'Humidity', 'value': 'Humidity'}
                ],
                value = 'Temperature (C)',
                clearable = False
            ),
            dcc.Graph(
                id='farm_line_plot',
                figure=line_temp_fig,
                config={
                    'displayModeBar': False
                }
            )
        ])
    ])
])


# Camera Callback
@callback(
    Output(component_id='farm_image', component_property='src'),
    Input(component_id='farm_camera_dropdown', component_property='value')
)
def update_image(option):
    src='assets/img1.jpg'
    if option:
        src=option
    return src

# Plot Callback
@callback(
    Output(component_id='farm_line_plot', component_property='figure'),
    Input(component_id='farm_line_plot_dropdown', component_property='value')
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
