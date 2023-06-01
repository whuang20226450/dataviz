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
activity2color = {
    "rest": color_map[0],
    "social": color_map[1],
    "entertainment": color_map[2],
    "other": color_map[3],
    "exercise": color_map[4],
    "work": color_map[6],
}

# todo
# 2. make datepicker more noticeble
# 3. make select-user-dropdown more good-looking
# 6. color pattern ???
# 7. hover template


layout = dbc.Container([
        html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody("App Detail", style={'font-weight': 'bold'}),
                                dcc.Graph(id='fig1'),
                                html.P(id='err1', className='m-3 text-danger'),
                            ],
                            className="mb-3",
                        ),

                        width=6
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody("Activity Analysis", style={'font-weight': 'bold'}),
                                dcc.Graph(id='fig2'),
                                html.P(id='err2', className='m-3 text-danger'),
                            ],
                            className="mb-3",
                        ),
                        width=6,
                        
                    ),
                ],
                justify="center",
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(id='routine'),
                            html.P(id='routine_err', className='m-3 text-danger'),
                        ],
                    ),
                    width=12,
                ),
            ),
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
            dbc.Row(html.Div(html.Br())),  # empty row for spacing
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody("Attention v.s. Stress", style={'font-weight': 'bold'}),
                            dcc.Graph(id='atten'),
                            html.P(id='atten_err', className='m-3 text-danger'),
                        ],
                        className="mb-3",
                    ),
                    width=12,
                ),
            ),

        ]
    ) 
])

@callback(
    Output("atten", "figure"),
    Output('atten', 'style'),
    Output('atten_err', 'children'),
    Input("picked-date", "date"), 
    Input("user-dropdown", "value"),
)
def updateAtten(picked_date, value):

    picked_date = date.fromisoformat(picked_date)

    esm_df = pd.read_csv(dir_path + "/esm_data.csv")
    esm_sel = esm_df[esm_df['UID'] == int(value[1:])]
    esm_sel['date'] = pd.to_datetime(esm_sel['responseTime_KDT'])

    # handle if data doesn't exist for user
    data_start_time = esm_sel.iloc[0]['date']
    data_end_time = esm_sel.iloc[-1]['date']
    if picked_date < data_start_time.date() or picked_date > data_end_time.date():
        return dash.no_update, {'display':'none'}, \
            f"Please choose the date within {data_start_time.strftime('%Y-%m-%d')} ~ {data_end_time.strftime('%Y-%m-%d')}"


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

    return fig, {'display':'block'}, f""


@callback(
    Output("routine", "figure"),
    Output('routine', 'style'),
    Output('routine_err', 'children'),
    Input("picked-date", "date"), 
    Input('range-slider', 'value'), 
    Input("user-dropdown", "value")
)
def updateRoutine(picked_date, picked_hours=[0,24], uid='P0705'):

    picked_date = date.fromisoformat(picked_date)
    start_hour, end_hour = picked_hours
    picked_hours = [start_hour + delta for delta in range(end_hour - start_hour)]

    df = pd.read_csv(dir_path + '/data/' + 'processed_data_v3.csv')

    # handle if data doesn't exist for user
    data_start_time = df[df.user_id == uid].iloc[0]['start_time'][:10]  # [:10] is to extract the 10 chars '2019-05-10'
    data_end_time = df[df.user_id == uid].iloc[-1]['end_time'][:10]
    if picked_date < date.fromisoformat(data_start_time) or picked_date > date.fromisoformat(data_end_time):
        return dash.no_update, {'display':'none'}, f"Please choose the date within {data_start_time} ~ {data_end_time}"


    df_sel = df[df.user_id == uid]
    df_sel["start_time"] = pd.to_datetime(df_sel["start_time"])
    df_sel["end_time"] = pd.to_datetime(df_sel["end_time"])
    df_sel["date"] = df_sel["start_time"].dt.date
    df_sel = df_sel[df_sel["date"] == picked_date]

    df_sel["start_hour"] = df_sel["start_time"].dt.hour
    df_sel["end_hour"] = df_sel["end_time"].dt.hour

    df_sel = df_sel[df_sel["start_hour"].isin(picked_hours)]

    fig = px.timeline(
        df_sel, 
        x_start="start_time", 
        x_end="end_time", 
        y = [1]*len(df_sel), 
        color="activity_type",
        color_discrete_map=activity2color,
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

    return fig, {'display':'block'}, f""


def compute_total_time(times):
    total_time = timedelta(0)
    for time in times:
        total_time += time
    return total_time

# for plots
@callback(
    Output("fig1", "figure"),
    Output('fig1', 'style'),
    Output('err1', 'children'),
    Input("picked-date", "date"),
    Input('routine', 'clickData'),
    Input("user-dropdown", "value")
)
def fig1_callback(picked_date, click_data=None, uid='P0705'):

    # handle if no click data
    if click_data is None:
        return dash.no_update, {'display':'none'}, 'No activity is choosen now. Please choose one by clicking the activity in the routine plot!'

    picked_date = date.fromisoformat(picked_date)
    picked_dates = [picked_date + timedelta(days=i) for i in range(7)]
    activity = click_data['points'][0]['customdata'][0] if click_data is not None else None
    picked_name = click_data['points'][0]['customdata'][1] if click_data is not None else None

    df = pd.read_csv(dir_path + '/data/' + 'processed_data_v2.csv')

    # handle if data doesn't exist for user
    data_start_time = df[df.user_id == uid].iloc[0]['start_time'][:10]
    data_end_time = df[df.user_id == uid].iloc[-1]['end_time'][:10]
    if picked_date < date.fromisoformat(data_start_time) or picked_date > date.fromisoformat(data_end_time):
        return dash.no_update, {'display':'none'}, f"Please choose the date within {data_start_time} ~ {data_end_time}"

    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    df["date"] = df["start_time"].dt.date
    
    df = df[(df['user_id'] == uid) & 
            (df["date"].isin(picked_dates)) & 
            (df['name'] == picked_name)]

    df['time'] = df['end_time'] - df['start_time']
    df = df[['date', 'time']]     # only keep this two cols
    df = df.groupby(['date'], group_keys=False).time.apply(compute_total_time).reset_index(name='time')

    df['hours'] = df.time.apply(lambda x: float(x.seconds)/3600)

    fig=go.Figure()
    fig.add_traces(go.Bar(x=[date.strftime('%Y %m/%d') for date in df["date"].values.tolist()], y=df["hours"], marker_color='#66C5CC'))

    fig.update_layout(
        title=f'<B>{picked_name.capitalize()}</B> time over a week',
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

    return fig, {'display':'block'}, ""


@callback(
    Output("fig2", "figure"),
    Output('fig2', 'style'),
    Output('err2', 'children'),
    Input("picked-date", "date"),
    Input('routine', 'clickData'),
    Input("user-dropdown", "value")
)
def fig2_callback(picked_date, click_data=None, uid='P0705', activity='other'):

    if click_data is None:
        return dash.no_update, {'display':'none'}, 'No activity is choosen now. Please choose one by clicking the activity in the routine plot!'
    
    
    activity = click_data['points'][0]['customdata'][0] if click_data is not None else None
    picked_name = click_data['points'][0]['customdata'][1] if click_data is not None else None
    df = pd.read_csv(dir_path + '/data/' + 'processed_data_v2.csv')

    
    # handle if data doesn't exist for user
    data_start_time = df[df.user_id == uid].iloc[0]['start_time'][:10]
    data_end_time = df[df.user_id == uid].iloc[-1]['end_time'][:10]
    picked_date = date.fromisoformat(picked_date)
    if picked_date < date.fromisoformat(data_start_time) or picked_date > date.fromisoformat(data_end_time):
        return dash.no_update, {'display':'none'}, f"Please choose the date within {data_start_time} ~ {data_end_time}"

    
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    df["date"] = df["start_time"].dt.date
    
    df = df[(df['user_id'] == uid) & 
            (df["date"] == picked_date) & 
            (df['activity_type'] == activity)]

    df['time'] = df['end_time'] - df['start_time']
    df = df[['name', 'time']]     # only keep this two cols
    df = df.groupby(['name'], group_keys=False).time.apply(compute_total_time).reset_index(name='time')

    total_time = df.time.values.tolist()
    total_time_sum = np.array(total_time).sum()
    total_time_percentage = total_time / total_time_sum

    df = pd.DataFrame({'name': df.name, 
                       'total_time_percentage': total_time_percentage})
    

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=df["name"], 
            values=df["total_time_percentage"],
            textposition='inside',
            pull=[0.2 if n == picked_name else 0. for n in df['name'].values.tolist()]
        )
    )

    m1 = 50
    fig.update_layout(
        margin=dict(t=m1, b=m1, l=m1, r=m1),
        title=f'<B>{picked_name.capitalize()}</B> highlighted in <B>{activity.capitalize()}</B>',
        template='seaborn',
    )

    return fig, {'display':'block'}, ""


