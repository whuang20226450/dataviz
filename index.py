# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import main, analysis, plan, use, suggest

# Connect the navbar to the index
from components import navbar

# Define the navbar
nav = navbar.Navbar()

server = app.server

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Br(),
    html.Br(),
    html.Div(id='page-content', children=[]), 
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/analysis':
        return analysis.layout
    if pathname == '/plan':
        return plan.layout
    if pathname == '/use':
        return use.layout
    if pathname == '/suggest':
        return suggest.layout
    if pathname == '/main':
        return main.layout
    else: # if redirected to unknown link
        return main.layout

# Run the app on localhost:8050
if __name__ == '__main__':
    display_page("/main")
    app.run_server(debug=True, dev_tools_props_check=False)