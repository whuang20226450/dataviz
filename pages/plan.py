# Import necessary libraries 
from dash import html
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import callback, clientside_callback
from dash.dependencies import Input, Output, State, ClientsideFunction


estim_time = {
    "Read News" : 20,
    "Nap" : 30,
    "Homework" : 90,
    "Sleep": 480,
    "Play LoL": 90
}

MAX_HEIGHT = 20 
MAX_LEN = 480 


def get_height (time):
    out = int(MAX_HEIGHT * (time / MAX_LEN)) 
    return out if out > 5 else 5

# Define the page layout
layout = html.Div(id="main", children=[
    html.Div(id="drag_container0", className="container", children=[
    
    dbc.Row([
        dbc.Col(
            html.Div(id = "left_container", className="lcontainer", children = [
    html.H1("Possible Activities"),
    html.Div(id="drag_container", className="container", children=[
        dbc.Card([
            dbc.CardHeader("Sleep",
                style = {"color": "white"}),
            dbc.CardBody(
                f"Estimated time: {estim_time['Sleep']} min",
                style = {"color": "white"}
            ),
        ], color = "success",
        style = {"height": f"{get_height(estim_time['Sleep'])}rem",
                 "width": "90%"}),
        dbc.Card([
            dbc.CardHeader("Read News",
                style = {"color": "white"}),
            dbc.CardBody(
                "Estimated time: 20 min",
                style = {"color": "white"}
            ),
        ], color = "success",
        style = {"height": f"{get_height(estim_time['Read News'])}rem",
                 "width": "90%"}),
        dbc.Card([
            dbc.CardHeader("Nap",
                style = {"color": "white"}),
            dbc.CardBody(
                "Estimated time: 30 min",
                style = {"color": "white"}
            ),
        ], color = "warning",
        style = {"height": f"{get_height(estim_time['Nap'])}rem",
                 "width": "90%"}),
        dbc.Card([
            dbc.CardHeader("Homework",
                style = {"color": "white"}),
            dbc.CardBody(
                "Estimated Time: 1.5 hr",
                style = {"color": "white"}
            ),
        ], color = "danger",
        style = {"height": f"{get_height(estim_time['Homework'])}rem",
                 "width": "90%"}),
        dbc.Card([
            dbc.CardHeader("Play LoL",
                style = {"color": "white"}),
            dbc.CardBody(
                "Estimated Time: 1 hr",
                style = {"color": "white"}
            ),
        ], color = "danger",
        style = {"height": f"{get_height(estim_time['Play LoL'])}rem",
                 "width": "90%"}),
    ], style={'padding': 20}) ])) , 
    dbc.Col(
    html.Div(id = "right_container", className = "rcontainer", children = [
        html.H1("Your current plan"),
        html.Div(id="drag_container2", className="container", children=[
        # dbc.Card([
        #     dbc.CardHeader("Sleep"),
        #     dbc.CardBody(
        #         "Estimated Time: 8 hr"
        #     ),
        # ],
        # style = {"height": "15rem",
        #          "width": "90%"}),
        # dbc.Card([
        #     dbc.CardHeader("Play LoL"),
        #     dbc.CardBody(
        #         "Estimated Time: 8 hr"
        #     ),
        # ],
        # style = {"height": "15rem",
        #          "width": "90%"}),
        # dbc.Card([
        #     dbc.CardHeader("Jogging"),
        #     dbc.CardBody(
        #         "Estimated Time: 8 hr"
        #     ),
        # ],
        # style = {"height": "15rem",
        #          "width": "90%"}),
    ], style={'padding': 20} )])
    
    ) ])
 ] )
])

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container0", "data-drag"),
    [Input("drag_container2", "id"), Input("drag_container", "id")]
)