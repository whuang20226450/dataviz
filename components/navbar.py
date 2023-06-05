# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import os
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(dir_path + '/data/' + 'processed_data_v2.csv')

users = list(df["user_id"].unique())
# print(users)

# Define the navbar structure
def Navbar():

    # layout = html.Div([
    #     dbc.NavbarSimple(
    #         children=[
    #             dbc.NavItem(dbc.NavLink("Main", href="/main")),
    #             dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
    #             dbc.NavItem(dbc.NavLink("Plan", href="/plan")),
    #             dbc.NavItem(dbc.NavLink("Use", href="/use")),
    #             # dbc.NavItem(dbc.NavLink("Schedule suggestions", href="/suggest")),
    #             html.Span(),
    #             html.Span(
    #                 dcc.Dropdown(
    #                     options=users,
    #                     value="P0705",
    #                     id = "user-dropdown",
    #                     style={
    #                         'width': '150%',
    #                         'background-color': '#f9f9f9',
    #                     }
    #                 ), 
    #             ),
                
    #         ] ,
    #         brand = "Tempus",
    #         brand_style = {"color": "white",
    #                        "font-family": "Arial",
    #                        "font-style": "italic",
    #                        "font-weight": "bold",
    #                        "font-size": "28px"
    #                        },
    #         brand_href = "/main",
    #         color = "dark",
    #         dark = True,
    #         links_left = True
    #     ), 
    # ])


    layout = html.Div(
        [
            dbc.Navbar(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                        dbc.NavbarBrand(
                                            "Tempus", 
                                            className="ms-2",
                                            style = {
                                                "font-family": "Arial",
                                                "font-style": "italic",
                                                "font-weight": "bold",
                                                "font-size": "25px"
                                            },
                                        ),
                                        href="/main",
                                        style={"textDecoration": "none"},
                                    ),
                                    width={"size": 1},
                                ),
                                dbc.Col(
                                    [
                                        dbc.Nav(
                                            [
                                                dbc.NavItem(dbc.NavLink("Main", href="/main")),
                                                dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
                                                dbc.NavItem(dbc.NavLink("Plan", href="/plan")),
                                                dbc.NavItem(dbc.NavLink("Use", href="/use")),
                                            ]
                                        ),
                                    ],
                                    width={"size": 3},
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        options=users,
                                        value="P0705",
                                        id = "user-dropdown",
                                        style={
                                            # 'width': '150%',
                                            'background-color': '#E3F4F4',
                                        }
                                    ),
                                    width={"size": 2, "offset": 6},
                                ),
                            ],
                            align="center",
                            # justify="between",
                            style={'width': '100%'},
                        ),                        
                    ],
                ),
                color="dark",
                dark=True,
            ),
        ],
    )


    return layout