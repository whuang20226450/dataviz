import pandas as pd
import plotly.express as px
import numpy as np
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
import os
import datetime
from datetime import date
#-------------------------------------------------------------fake data--------------------------------------------------#
#Import data
gapminder_df=pd.read_csv('gapminder_co2.csv')
gapminder_df['co2']=gapminder_df['co2'].astype(float)
gapminder_df['gdp']=gapminder_df['gdp'].astype(float)
gapminder_df['population']=gapminder_df['population'].astype(float)
gapminder_df['life']=gapminder_df['life'].astype(float)

#Draw scatter plot
main_fig=px.scatter(gapminder_df, x='co2', y='gdp')
sub_fig=px.scatter(gapminder_df, x='co2', y='gdp')


# fake data for productivity plot
productivity_fake = np.random.rand(31).tolist()
productivity_diff_fake = np.random.rand(31).tolist()
productivity_other_fake = np.random.rand(31).tolist()
week_day = ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
df_fake = pd.DataFrame(data={'productivity': productivity_fake, 'productivity_diff': productivity_diff_fake, 'productivity_other': productivity_other_fake, 'week_day': (week_day*5)[:31]})

# fake data for activity plot
activity_type = ['Social', 'Entertainment', 'Work', 'Rest', 'Exercise', 'Other']
activity_time = [3,5,2,8,1,5]
activity_time2 = [8,1,5,3,5,2,]
activity_detail_type_fake = ['yt', 'netflix', 'LOL', 'Shopping']
activity_detail_time_fake = ['3','5','2','8']
df_fake3 = pd.DataFrame(data={'activity_type': activity_type, 'activity_time': activity_time, 'activity_time2': activity_time2})
df_fake3_2 = pd.DataFrame(data={'activity_detail_type': activity_detail_type_fake, 'activity_detail_time': activity_detail_time_fake})

# fake data for weekly key metrics (S+A)
stress_fake = [3, 1, 2, 3, 1, -2, -3]
attention_fake = [0, 2, 3, 2, 1, 2, 1]
stress_fake2 = [3, 1, -2, -3, 3, 1, 2]
attention_fake2 = [1, 2, 1, 0, 2, 3, 2, ]
df_fake2 = pd.DataFrame(data={'stress': stress_fake, 'attention': attention_fake, 'stress_other': stress_fake2, 'attention_other': attention_fake2, 'week_day': week_day})
#-------------------------------------------------------------fake data--------------------------------------------------#


def plot_main(graph_type, comparison_type, start_date, user):
    # print(user)
    if graph_type == "Weekly Productivity":
        fig1 = weekly_productivity_plot(comparison_type, start_date, user)
        fig2 = None
    elif graph_type == "Monthly Productivity":
        fig1, fig2 = monthly_productivity_plot(comparison_type, start_date, user)
    elif graph_type == "Activity Analysis":
        fig1, fig2 = activity_analysis_plot(comparison_type, start_date, user)
    elif graph_type == "Weekly Key Metrics (S+A) Levels":
        fig1 = key_metrics_plot(comparison_type, start_date, df_fake2, user)
        fig2 = None
    
    # Fix the glitch of fig1 when switching form no fig2 to fig2 showing
    if (comparison_type == 'Self') or (fig2 is None):
        figs = [dbc.Col( dcc.Graph(figure=fig1), width=8)]
    else:
        figs = [dbc.Col( dcc.Graph(figure=fig1), width=6), dbc.Col(dcc.Graph(figure=fig2),width=6)]

    return figs

def compute_total_time(start_times, end_times):

    # change the str to datetime obj in the Series
    # start_times = start_times.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
    # end_times = end_times.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
    
    diff_time = (end_times - start_times).sum()
    return diff_time

def get_prod(df):
    out = 0 
    product = df[df.activity_type == "work"]
    out = compute_total_time(product["start_time"], product["end_time"])

    # print(out)
    if out == 0:
        return 0 
    else:
        return np.log(1 + (600 / ( 10 + out.total_seconds())))
        # return 1/out.total_seconds()

# Note: somehow the end is included for df.loc[], eg. df.loc[:6] -> row 0~6 are included
def weekly_productivity_plot(comparison_type, start_date, value):
    fig=go.Figure()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data = pd.read_csv(dir_path + '/pages/data/' + 'processed_data_v2.csv')
    df = data.copy()
    df["start_time"] = pd.to_datetime(data["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    df["date"] = df["start_time"].dt.date
    df = df[df.user_id == value]
    df = df[df["date"] >= start_date]
    # df = df[:7]

    productivities = {}
    avg_prod = {}
    # print(sorted(list(set(df.date))))
    users = list(set(data["user_id"]))

    for date in sorted(list(set(df.date))):
        productivities[date] = get_prod(df[df["date"] == date])

        # user_prods = []
        # for user in users:
        #     df = data.copy()
        #     df["start_time"] = pd.to_datetime(data["start_time"])
        #     df["end_time"] = pd.to_datetime(df["end_time"])
        #     df["date"] = df["start_time"].dt.date
        #     df = df[df.user_id == user]
        #     df = df[df["date"] >= date]
        #     if len(df) == 0:
        #         continue
        #     user_prod = get_prod(df[df["date"] == date])
        #     user_prods.append(user_prod)
        # # print(user_prods)
        # avg_prod[date] = np.mean(user_prods)

    # print(productivities)

    #all users
    
    # user_prod = {user: dict() for user in users}
    # for user in users:
    #         df = data.copy()
    #         df["start_time"] = pd.to_datetime(data["start_time"])
    #         df["end_time"] = pd.to_datetime(df["end_time"])
    #         df["date"] = df["start_time"].dt.date
    #         df = df[df.user_id == user]
    #         df = df[df["date"] >= start_date]

    #         product_user = {}
    #         for date in sorted(list(set(df.date))):
    #             product_user[date] = get_prod(df[df["date"] == date])
            
    #         user_prod[user] = product_user


    # print(user_prod)

    others = pd.read_csv(dir_path + '/pages/data/' + 'dataAVG_prod.csv')
    # print(others.head())
    # df["start_time"] = pd.to_datetime(data["start_time"])
    # df["end_time"] = pd.to_datetime(df["end_time"])
    # print(others.columns)
    others["Date"] = pd.to_datetime(others["Date"])
    
    fig.add_traces(go.Bar(name='Self', x=list(productivities.keys()), y=list(productivities.values()), marker_color='#66C5CC'))
    if comparison_type == "All users":
        # fig.add_traces(go.Bar(name=comparison_type, x=df.week_day, y=df.loc[:6].productivity_other, marker_color='#F6CF71'))
        sel = others[others.Date.isin(list(productivities.keys()))]
        # print(sel.head())
        fig.add_traces(go.Bar(name=comparison_type, x=list(sel["Date"]), y=list(sel["avg_prod_all"]), marker_color='#F6CF71'))
    if comparison_type == "Best users":
        # sel = [others[i] if others.Date[i] in productivities.keys()]
        sel = others[others.Date.isin(list(productivities.keys()))]
        fig.add_traces(go.Bar(name=comparison_type, x=list(sel["Date"]), y=list(sel["avg_prod_top"]), marker_color='#F6CF71'))
    if comparison_type == "Worst users":
        sel = others[others.Date.isin(list(productivities.keys()))]
        fig.add_traces(go.Bar(name=comparison_type, x=list(sel["Date"]), y=list(sel["avg_prod_bot"]), marker_color='#F6CF71'))

    fig.update_layout(
        title=f'<B>Weekly Productivity</B> compared with {comparison_type} starting from {start_date}',
        hovermode='x',
        plot_bgcolor='white',
    )
    fig.update_xaxes(
        ticks='outside',
        showline=True,      # axis show or not
        linecolor='black',  # axis line color
        linewidth=1,        # axis thickness
    )
    fig.update_yaxes(
        title_text="Productivity",
        ticks='outside',
        showline=True,
        linecolor='black',
        linewidth=1,
    )

    if comparison_type == 'Self':
        fig.update_layout(
            title=f'<B>Weekly Productivity</B> starting from {min(list(productivities.keys()))}',
        )
    return fig


def monthly_productivity_plot(comparison_type, start_date, value):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(dir_path + '/pages/data/' + 'processed_data_v2.csv')
    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    df["date"] = df["start_time"].dt.date
    df = df[df.user_id == value]
    df = df[df["date"] >= start_date]
    # df = df[:7]

    productivities = {}
    # print(sorted(list(set(df.date))))

    others = pd.read_csv(dir_path + '/pages/data/' + 'dataAVG_prod.csv')
    # print(others.columns)
    others["Date"] = pd.to_datetime(others["Date"])

    for date in sorted(list(set(df.date))):
        productivities[date] = get_prod(df[df["date"] == date])

    fig1 = calendar_heatmap(list(productivities.values()), min(productivities.keys()), 
        f'<B>Monthly Productivity</B> from {str(start_date)}')


    # fig2 = calendar_heatmap(df.productivity_diff.values.tolist(), start_date, 
    #     f'<B>Productivity Difference</B> between user and {comparison_type} <Br>starting from {str(start_date)}')
    if comparison_type == "All users":
        fig2 = calendar_heatmap(list(others.avg_prod_all), min(others.Date), 
        f'<B>Productivity Difference</B> between user and {comparison_type} <Br>starting from {str(start_date)}')
    elif comparison_type == "Best users":
        fig2 = calendar_heatmap(list(others.avg_prod_top), min(others.Date), 
        f'<B>Productivity Difference</B> between user and {comparison_type} <Br>starting from {str(start_date)}')
    elif comparison_type == "Worst users":
        fig2 = calendar_heatmap(list(others.avg_prod_bot), min(others.Date), 
        f'<B>Productivity Difference</B> between user and {comparison_type} <Br>starting from {str(start_date)}')
    else:
        fig2 = None


    

    return fig1, fig2

# this function is slightly modified from the internet, whoever in charge plz modify it and make it diff from the ori version
# see the following link to see comment of the code
# https://community.plotly.com/t/colored-calendar-heatmap-in-dash/10907/7
def calendar_heatmap(data, start_date, title):

    end_date = start_date + datetime.timedelta(30)

    # eg. if start_date is Thr then start_date.weekday() would be 3 since it is 0-based
    # then we need to fill the first missing 3 days in the front of the week. Therefore, missing_front = 3
    missing_front = start_date.weekday()
    missing_back = 6 - end_date.weekday()

    Mon_of_start_date = start_date - datetime.timedelta(missing_front)
    Sun_of_end_date = end_date + datetime.timedelta(missing_back)
    selected_dates_count = (Sun_of_end_date - Mon_of_start_date).days + 1

    # selected_dates: list of datetime.time() obj of selected dates
    # weekdays_of_selected_dates: would be [0, 1, 2 ..., 6] * week_number
    # datetime.time().strftime("%V") get the week number of the date, e. like the 1/2 is 1 since it is 1st week of the year
    selected_dates = [Mon_of_start_date + datetime.timedelta(i) for i in range(selected_dates_count)]
    weekdays_of_selected_dates = [i.weekday() for i in selected_dates]   
    weeknumber_of_selected_dates = [int(i.strftime("%V")) for i in selected_dates]
    productivity_fake = [0]*missing_front + data + [0]*missing_back
    text = [str(i)+"   Productivity: "+str(np.round(j,2)) for i, j in zip(selected_dates, productivity_fake)]

    plot_data = [
        go.Heatmap(
            x = weekdays_of_selected_dates,
            y = weeknumber_of_selected_dates,
            z = productivity_fake,
            text=text,
            hoverinfo="text",
            xgap=3, 
            ygap=3, 
            colorscale='blues',
            colorbar=dict(title='Productivity') ,
        )
    ]
    layout = go.Layout(
        title=title,
        xaxis=dict(
            tickmode="array",
            ticktext=['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun'],
            tickvals=[0,1,2,3,4,5,6],
        ),
        yaxis=dict(
            visible=False,
        ),
        plot_bgcolor=('rgb(255,255,255)') # making grid appear white
    )
    fig = go.Figure(data=plot_data, layout=layout)

    return fig


def details_activity_type(user, day, activity_type, user_df):
  # filtering by user and activity
  user_df.user_id = user_df.user_id.astype(str)
  user_df = user_df[user_df.user_id == user]
  user_activity_df = user_df[user_df['activity_type'] == activity_type]

  # turing timestamps to datetime
  user_activity_df.start_time = pd.to_datetime(user_activity_df.start_time)
  user_activity_df.end_time = pd.to_datetime(user_activity_df.end_time)

  # finding the total duration
  user_activity_df['day'] = user_activity_df['start_time'].dt.day
  user_activity_df['duration'] = user_activity_df.end_time - user_activity_df.start_time

  user_activity_df.drop(['activity_type', 'start_time', 'end_time', 'Unnamed: 0', "user_id"], axis=1, inplace=True)
  user_activity_day_df = user_activity_df[user_activity_df.day == day]

  user_activity_df = user_activity_day_df.groupby('name')['duration'].sum().reset_index()
  total_time = user_activity_df['duration'].sum()
  user_activity_df['duration'] = (user_activity_df['duration']/total_time)*100

  return user_activity_df


def activity_analysis_plot(comparison_type, start_date, value):
    
    # activity_type = df.activity_type
    # activity_time = df.activity_time
    # activity_time2 = df.activity_time2
    # activity_detail_type_fake = df2.activity_detail_type
    # activity_detail_time_fake = df2.activity_detail_time

    dir_path = os.path.dirname(os.path.realpath(__file__))
    user = str(value)
    # print(user)
    activity_df = pd.read_csv(dir_path + r'/pages/data/' + r'activ_data/'+f"{user}.csv")
    df2 = pd.read_csv(dir_path + '/pages/data/' + 'processed_data_v2.csv')
    # print(activity_df.head())
    sel = activity_df[activity_df["day"] == start_date.day]
    # print(sel)


    # new_df = pd.DataFrame({'Activity Type': activity_percentages.index, 'Percentage': activity_percentages.values})

    # fig1
    fig1 = go.Figure(data=[go.Pie(labels=sel["activity_type"], values=sel["duration"], pull=[0, 0, 0, 0, 0, 0], textposition= "inside")])

    m1, m2 = 50, 80
    btn_list = []
    # activity_time = None #TODO
    for idx, activity in enumerate(list(sel["activity_type"])):
        extra = details_activity_type(value, start_date.day, activity.lower(), df2)
        # print(activity)
        # print(list(extra["name"]))
        # print(list(extra["duration"]))
        # print()
        btn_list.append(
            dict(label = activity, method = 'update',
                # in args and args2, the first dict is for go.Pie, and the sec dict is for go.Figure (I guess)
                args = [
                    {
                        'labels': [list(sel["activity_type"])], 
                        'values': [list(sel["duration"])],
                        'pull': [[0.2 if i == idx else 0. for i in range(len(sel["activity_type"]))]], 
                        'title': f'{activity} highlighted',
                    },
                    {'margin': dict(t=m1, b=m1, l=m1, r=m1)}
                ],
                args2 = [
                    {
                        'labels': [list(extra["name"])], 
                        'values': [list(extra["duration"])], 
                        'pull': [[0. for i in range(len(list(extra["name"])))]],
                        'title': f'{activity} detail',
                    }, 
                    {'margin': dict(t=m2, b=m2, l=m2, r=m2*1.9)}
                ],
            ),
        )

    # print(btn_list)

    fig1.update_layout(
        updatemenus = list([dict(
            type="buttons",
            buttons=btn_list,

            # set buttons position
            x=1.035,
            xanchor="left",
            y=0.5,
            yanchor="top",

            # set buttons menu style
            bgcolor='rgb(200, 200, 200)',
            borderwidth=2,
            bordercolor='rgb(0,0,0)',
        )]),
        margin=dict(t=m1, b=m1, l=m1, r=m1),
        title = {
            'text':f'<B>Activity Analysis</B> compared with {comparison_type} on {start_date}',
        }
    )

    # fig2
    fig2=go.Figure()
    
    fig2.add_traces(go.Bar(name='Self', x=activity_type, y=activity_time, marker_color='#66C5CC'))
    fig2.add_traces(go.Bar(name=comparison_type, x=activity_type, y=activity_time2, marker_color='#F6CF71'))

    fig2.update_layout(
        title=f'<B>Activity Analysis</B> compared with {comparison_type} on {start_date}',
        hovermode='x',
        plot_bgcolor='white',
    )
    fig2.update_xaxes(
        ticks='outside',
        showline=True,      # axis show or not
        linecolor='black',  # axis line color
        linewidth=1,        # axis thickness
    )
    fig2.update_yaxes(
        title_text="Productivity",
        ticks='outside',
        showline=True,
        linecolor='black',
        linewidth=1,
    )

    return fig1, fig2


def key_metrics_plot(comparison_type, start_date, df, user):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    dir_path = os.path.dirname(os.path.realpath(__file__))
    esm_df = pd.read_csv(dir_path + "/pages/data" + "/esm_data.csv")
    esm_df['date'] = pd.to_datetime(esm_df['responseTime_KDT']).dt.date

    esm28 = esm_df[esm_df["date"] >= start_date]
    esm28 = esm28.loc[esm_df.UID == int(user[1:])]
    esm28['date'] = pd.to_datetime(esm28.responseTime_KDT)
    esm28['day'] = esm28.date.dt.day

    esm28_day = esm28.groupby('day').mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=esm28_day.index, y=esm28_day.Attention, name="Attention level"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=esm28_day.index, y=esm28_day.Stress, name="Stress level"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Weekly Key metrics"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Days")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Attention</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Stress</b>", secondary_y=True)

    # fig.add_trace(
    #     # <extra></extra> is used to remove legend shown while hovering
    #     go.Scatter(x=df.week_day, y=df.stress, name="stress level", 
    #         hovertemplate='Stress level: %{y}<extra></extra>',
    #         line=dict(color='rgb(206, 0, 0)'),
    #     ),
    #     secondary_y=False,
    # )

    # fig.add_trace(
    #     go.Scatter(x=df.week_day, y=df.attention, name="attention level", 
    #         hovertemplate='Attention level: %{y}<extra></extra>',
    #         line=dict(color='rgb(0, 1, 255)'),
    #     ),
    #     secondary_y=True,
    # )


    if comparison_type == "Best users" or comparison_type == "All users":
        esmTop5MeanDf = pd.read_csv(dir_path + "/pages/data" + "/top5_esm_df.csv")
        fig.add_trace(
            go.Scatter(x=esmTop5MeanDf.index, y=esmTop5MeanDf.Attention, name="top 5 users attention data",
                       line = dict(dash='dash')),
            secondary_y=True,
        )
        fig.add_trace(
            go.Scatter(x=esmTop5MeanDf.index, y=esmTop5MeanDf.Stress, name="top 5 users stress data",
                line = dict(dash='dash')),
            secondary_y=True,
        )
    if comparison_type == "Worst users" or comparison_type == "All users":
        esmWorst5MeanDf = pd.read_csv(dir_path + "/pages/data" + "/bottom5_esm_data.csv")
        fig.add_trace(
            go.Scatter(x=esmWorst5MeanDf.index, y=esmWorst5MeanDf.Attention, name="Bottom 5 users attention data", 
                       line = dict(dash='dash')),
            secondary_y=True,
        )
        fig.add_trace(
                go.Scatter(x=esmWorst5MeanDf.index, y=esmWorst5MeanDf.Stress, name="Bottom 5 users stress data",
                           line = dict(dash='dash')),
                secondary_y=True,
            )


    fig.update_layout(
        title_text=f"Weekly Key Metrics (S+A) Levels after {start_date}",
        hovermode='x',
        plot_bgcolor='white',
    )
    # fig.update_xaxes(
    #     ticks='outside',
    #     showline=True,      # axis show or not
    #     linecolor='black',  # axis line color
    #     linewidth=2,        # axis thickness
    # )
    # fig.update_yaxes(
    #     secondary_y=False,
    #     title_text="stress level",
    #     ticks='outside',
    #     showline=True,
    #     linecolor='black',
    #     linewidth=2,
    # )
    # fig.update_yaxes(
    #     secondary_y=True,
    #     title_text="attention level",
    #     ticks='outside',
    #     showline=True,
    #     linecolor='black',
    #     linewidth=3,
    # )

    return fig