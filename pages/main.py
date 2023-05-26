import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os
import plotly.figure_factory as ff
import plotly.graph_objects as go
from dash import callback
import numpy as np

from datetime import date, timedelta

dir_path = os.path.dirname(os.path.realpath(__file__))
color_map = ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]

# todo
# 1. allow range slider to adjust atten as well
# 2. make datepicker more noticeble
# 3. make select-user-dropdown more good-looking
# 4. make popup if user chooses date that doesn't have data
# 5. change how the slider work for the bug 


layout = dbc.Container([
        html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    id='picked-date',
                                    min_date_allowed=date(2010, 1, 5),
                                    max_date_allowed=date(2023, 9, 19),
                                    initial_visible_month=date(2019, 5, 8),
                                    date=date(2019, 5, 8),
                                ),
                            ],
                            # style={"background-color": "red", "width": "fit-content", "margin-right": 0}
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.RangeSlider(0, 24, 1, value=[0, 24], id='range-slider'),
                        width=8,
                    ),
                ],
                # justify="center",
                # style={"background-color": "black"}
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                            dcc.Graph(id='atten'),
                    ),
                    width=12,
                ),
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                            dcc.Graph(id='routine'),
                    ),
                    width=12,
                ),
            ),
            dbc.Row(html.Div(html.Br())),  # empty row for spacing
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody("App Detail"),
                                dcc.Graph(id='fig1'),
                            ],
                            className="mb-3",
                        ),

                        width=6
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody("Activity Analysis"),
                                dcc.Graph(id='fig2'),
                            ],
                            className="mb-3",
                        ),
                        width=6,
                        
                    ),
                ],
                justify="center",
            ),
        ]
    ) 
])

@callback(Output("atten", "figure"), [Input("picked-date", "date"), Input("user-dropdown", "value")])
def updateGraph(picked_date, value):

    picked_date = date.fromisoformat(picked_date)

    esm_df = pd.read_csv(dir_path + "/esm_data.csv")
    esm_sel = esm_df[esm_df['UID'] == int(value[1:])]
    esm_sel['date'] = pd.to_datetime(esm_sel['responseTime_KDT'])
    esm_sel['month'] = esm_sel['date'].dt.month
    esm_sel['day'] = esm_sel['date'].dt.day
    esm_sel = esm_sel[(esm_sel["month"] == picked_date.month) & (esm_sel["day"] == picked_date.day)]

    fig = go.Figure()
    fig.add_traces(go.Scatter(
        x = esm_sel['date'],
        y = esm_sel["Attention"],
        name='Attention'
        ))
    fig.add_traces(go.Scatter(
        x = esm_sel['date'],
        y = esm_sel["Stress"],
        name='Stress'
        ))

    fig.update_layout(
        showlegend=True, plot_bgcolor = "white", height = 350,
        hovermode="x",
        yaxis_range=[-3.1,3.1],     # if set -3~3, the line will get cropped if val is 3 to 3
        yaxis = dict(
            tickmode = 'linear',
            tick0 = -3,
            dtick = 1
        ),
    )
    # fig.update_yaxes(
    #     ticks='outside',
    #     showline=True,
    #     linecolor='black',
    #     linewidth=1,
    # )

    return fig

@callback(Output("routine", "figure"),[Input("picked-date", "date"), Input('range-slider', 'value'), Input("user-dropdown", "value")])
def updateRoutine(picked_date=29, picked_hours=[0,24], uid='P0705'):

    start_hour, end_hour = picked_hours
    picked_hours = [start_hour + delta for delta in range(end_hour - start_hour)]

    df = pd.read_csv(dir_path + '/data/' + 'processed_data_v2.csv')
    data_start_time = df[df.user_id == uid].iloc[0]['start_time'][:10]
    data_end_time = df[df.user_id == uid].iloc[-1]['end_time'][:10]
    if date.fromisoformat(picked_date) < date.fromisoformat(data_start_time) or date.fromisoformat(picked_date) > date.fromisoformat(data_end_time):
        picked_date = data_start_time

    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    df["date"] = df["start_time"].dt.date
    df["start_hour"] = df["start_time"].dt.hour
    df["end_hour"] = df["end_time"].dt.hour

    df_sel = df[df.user_id == uid]
    df_sel = df_sel[df_sel["date"] == date.fromisoformat(picked_date)]
    df_sel = df_sel[df_sel["start_hour"].isin(picked_hours)]
    df_sel = df_sel[df_sel["end_hour"].isin(picked_hours)]

    fig = px.timeline(
        df_sel, 
        x_start="start_time", 
        x_end="end_time", 
        y = [1]*len(df_sel), 
        color="activity_type",
        color_discrete_map={
            "rest": color_map[0],
            "social": color_map[1],
            "entertainment": color_map[2],
            "other": color_map[3],
            "exercise": color_map[4],
            "work": color_map[6],
        },
        hover_name = "name",
        hover_data = {
            'start_time': True,
            'end_time': True,
            'activity_type': True,
            'name': True,
        },)

    fig.update_yaxes(visible=False)
    fig.update_layout(
        plot_bgcolor = "white",
        showlegend=True,
        height=200,
        legend=dict(
            orientation="h",
            # entrywidth=70,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title='Activity type',
            font=dict(
                family="Arial",
                size=12,
                color="black"
            ),
        )
    )

    return fig


def compute_total_time(times):
    total_time = timedelta(0)
    for time in times:
        total_time += time
    return total_time

# for plots
@callback(
    Output("fig1", "figure"),
    Input("picked-date", "date"),
    Input('routine', 'clickData'),
    Input("user-dropdown", "value")
)
def fig1_callback(picked_date, click_data=None, value='P0705', activity='other'):
    
    picked_date = date.fromisoformat(picked_date)
    picked_dates = [picked_date + timedelta(days=i) for i in range(7)]
    activity = click_data['points'][0]['customdata'][0] if click_data is not None else None
    picked_name = click_data['points'][0]['customdata'][1] if click_data is not None else None

    activity_df = pd.read_csv(dir_path + '/data/' + 'processed_data_v2.csv')
    activity_df["start_time"] = pd.to_datetime(activity_df["start_time"])
    activity_df["end_time"] = pd.to_datetime(activity_df["end_time"])
    activity_df["date"] = activity_df["start_time"].dt.date
    
    activity_df = activity_df[(activity_df['user_id'] == value) & 
                                (activity_df["date"].isin(picked_dates)) & 
                                (activity_df['name'] == picked_name)]

    activity_df['time'] = activity_df['end_time'] - activity_df['start_time']
    activity_df = activity_df[['date', 'time']]     # only keep this two cols
    activity_df = activity_df.groupby(['date'], group_keys=False).time.apply(compute_total_time).reset_index(name='time')

    activity_df['hours'] = activity_df.time.apply(lambda x: float(x.seconds)/3600)

    fig=go.Figure()
    fig.add_traces(go.Bar(x=activity_df["date"], y=activity_df["hours"], marker_color='#66C5CC'))

    fig.update_layout(
        title=f'<B>{picked_name}</B> use time over a week',
        plot_bgcolor='white',
    )
    fig.update_xaxes(
        ticks='outside',
        showline=True,      # axis show or not
        linecolor='black',  # axis line color
        linewidth=1,        # axis thickness
    )
    fig.update_yaxes(
        title_text="Hours",
        ticks='outside',
        showline=True,
        linecolor='black',
        linewidth=1,
    )

    return fig


@callback(
    Output("fig2", "figure"),
    Input("picked-date", "date"),
    Input('routine', 'clickData'),
    Input("user-dropdown", "value")
)
def fig2_callback(picked_date, click_data=None, value='P0705', activity='other'):
    
    activity = click_data['points'][0]['customdata'][0] if click_data is not None else None
    picked_name = click_data['points'][0]['customdata'][1] if click_data is not None else None
    activity_df = pd.read_csv(dir_path + '/data/' + 'processed_data_v2.csv')

    activity_df["start_time"] = pd.to_datetime(activity_df["start_time"])
    activity_df["end_time"] = pd.to_datetime(activity_df["end_time"])
    activity_df["date"] = activity_df["start_time"].dt.date
    
    activity_df = activity_df[(activity_df['user_id'] == value) & 
                                (activity_df["date"] == date.fromisoformat(picked_date)) & 
                                (activity_df['activity_type'] == activity)]

    activity_df['time'] = activity_df['end_time'] - activity_df['start_time']
    activity_df = activity_df[['name', 'time']]     # only keep this two cols
    activity_df = activity_df.groupby(['name'], group_keys=False).time.apply(compute_total_time).reset_index(name='time')

    total_time = activity_df.time.values.tolist()
    total_time_sum = np.array(total_time).sum()
    total_time_percentage = total_time / total_time_sum

    activity_df = pd.DataFrame({'name': activity_df.name, 
                                'total_time_percentage': total_time_percentage})
    

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=activity_df["name"], 
            values=activity_df["total_time_percentage"],
            textposition='inside', 
        )
    )

    m1 = 50
    fig.update_layout(
        margin=dict(t=m1, b=m1, l=m1, r=m1),
        title=f'<B>{activity}</B> with activity <B>{picked_name}</B> highlighted'
    )

    return fig


