# Import necessary libraries 
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.express as px
import pandas as pd
from dash import callback
from datetime import date
import random




# Define the page layout
layout = dbc.Container([
        html.Div(
        children = [
            html.Div(
                className = "content",
                children=[
                    html.Header(
                        style={'color':'#7FDBFF'},
                    ),
                    html.Div(
                                    [
                                        dbc.Label("Date to show: ", style={'font-weight': 'bold',
                                                                           'margin-bottom': '0',
                                                                           'margin-right': '10'}),
                                        html.Br(),
                                        dcc.DatePickerSingle(
                                            id='picked_day',
                                            min_date_allowed=date(2023, 1, 5),
                                            max_date_allowed=date(2023, 9, 19),
                                            initial_visible_month=date(2023, 5, 4),
                                            date=date(2023, 5, 4),
                                        )
                                    ],
                                ),
                    
                ]
            ),
                html.Div(dcc.Graph(id='use'),
                    style={'padding-left':'0px', 'width':'100%'}),
        ]
        )
])



@callback(Output("use", "figure"), Input("picked_day", "date"))
def updateGraph(picked_day):
    i1 = random.randint(0, 1)
    i2 = random.randint(0, 1)
    i3 = random.randint(0, 1)
    df = pd.DataFrame([
    dict(Task="Planned", Start='2023-05-22 00:00', Finish=f'2023-05-22 0{7+i1}:00', Planned = "yes", Activity = "Sleep"),
    dict(Task="Planned", Start=f'2023-05-22 0{7+i1}:00', Finish='2023-05-22 09:00', Planned = "yes", Activity = "Activ1"),
    dict(Task="Planned", Start='2023-05-22 09:00', Finish='2023-05-22 10:30', Planned = "yes", Activity = "Activ2"),
    dict(Task="Planned", Start='2023-05-22 10:30', Finish=f'2023-05-22 {12+i2}:00', Planned = "yes", Activity = "Activ3"),
    dict(Task="Planned", Start=f'2023-05-22 {12+i2}:00', Finish='2023-05-22 14:00', Planned = "yes", Activity = "Activ4"),
    dict(Task="Planned", Start='2023-05-22 14:00', Finish='2023-05-22 17:00', Planned = "yes", Activity = "Activ5"),
    dict(Task="Planned", Start='2023-05-22 17:00', Finish=f'2023-05-22 {19+i3}:00', Planned = "yes", Activity = "Activ7"),
    dict(Task="Planned", Start=f'2023-05-22 {19+i3}:00', Finish='2023-05-22 23:59', Planned = "yes", Activity = "Activ8"),
    
    dict(Task="Actual", Start='2023-05-22 00:00', Finish=f'2023-05-22 0{7+i1}:00', Planned = "yes", Activity = "Sleep"),
    dict(Task="Actual", Start=f'2023-05-22 0{7+i1}:00', Finish='2023-05-22 09:00', Planned = "no", Activity = "Activ1"),
    dict(Task="Actual", Start='2023-05-22 09:00', Finish='2023-05-22 10:30', Planned = "yes", Activity = "Activ2"),
    dict(Task="Actual", Start='2023-05-22 10:30', Finish=f'2023-05-22 {12+i2}:00', Planned = "no", Activity = "Activ3"),
    dict(Task="Actual", Start=f'2023-05-22 {12+i2}:00', Finish='2023-05-22 14:00', Planned = "yes", Activity = "Activ4"),
    dict(Task="Actual", Start='2023-05-22 14:00', Finish='2023-05-22 17:00', Planned = "yes", Activity = "Activ5"),
    dict(Task="Actual", Start='2023-05-22 17:00', Finish=f'2023-05-22 {19+i3}:00', Planned = "no", Activity = "Activ7"),
    dict(Task="Actual", Start=f'2023-05-22 {19+i3}:00', Finish='2023-05-22 23:59', Planned = "yes", Activity = "Activ8"),

    ])
    fig = px.timeline(df, 
                      x_start="Start", 
                      x_end="Finish", 
                      y="Task", 
                      color="Planned",
                      hover_name = "Activity",
                      title = f"Actual vs planned schedule on {picked_day}",
                      color_discrete_sequence = ["seagreen", "orangered"]
                      )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(plot_bgcolor = "white", 
                      paper_bgcolor = "white")

    return fig
