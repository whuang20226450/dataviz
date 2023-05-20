# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Main Page", href="/main")),
                dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
                dbc.NavItem(dbc.NavLink("Planning", href="/plan")),
                dbc.NavItem(dbc.NavLink("Use", href="/use")),
                dbc.NavItem(dbc.NavLink("Schedule suggestions", href="/suggest")),
            ] ,
            brand = "Tempus",
            brand_style = {"color": "white",
                           "font-family": "Arial",
                           "font-style": "italic",
                           "font-weight": "bold",
                           "font-size": "25px"
                           },
            brand_href = "/main",
            color = "dark",
            dark = True,
            links_left= True
        ), 
    ])

    return layout