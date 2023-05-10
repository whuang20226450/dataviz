import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os
import plotly.figure_factory as ff
from dash import callback



dir_path = os.path.dirname(os.path.realpath(__file__))
esm_df = pd.read_csv(dir_path + "/esm_data.csv")
uid = 3024
esm_df = esm_df.loc[esm_df['UID'] == uid]
esm_df['responseTime_KDT'] = pd.to_datetime(esm_df['responseTime_KDT'])
esm_df['month'] = esm_df['responseTime_KDT'].dt.month
esm_df['day'] = esm_df['responseTime_KDT'].dt.day

dir_path = os.path.dirname(os.path.realpath(__file__))
ac_df = pd.read_csv(dir_path + "/activity.csv")
figX = px.bar(ac_df, x='day', y='time')

# z = [esm_df.Attention]
# fig = px.imshow(z, x=esm_df.responseTime_KDT, text_auto=False, height=160)
# # fig.update_layout(height=160, width=900,margin=dict(l=70, r=70, t=70, b=70), legend=dict(x=2,font=dict(size= 20)))
# # fig.update_traces(width=1)
# fig.update_layout(bargap=0.2, showlegend=False)

# fig.update_yaxes(showticklabels=False)

# z = [esm_df.Attention.to_numpy()]
# fig = ff.create_annotated_heatmap(z, colorscale='Viridis')
# fig.update_layout(height=200)

navigationModal = dbc.Modal([
            dbc.ModalHeader("Navigate to other pages"),
            dbc.ModalBody([
                dcc.Link('Go to Use page', href='/use'),
                html.Br(),
                dcc.Link('Go to Analysis page', href='/analysis')
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close", className="ml-auto")
            ),
        ], id="nav_modal", centered=True)
    # ], style={'position': 'fixed', 'bottom': 10, 'right': 10})

modal = dbc.Modal(
            [
                dbc.ModalHeader("App Usage history"),
                dbc.ModalBody([
                    # html.H4(id='hover_info'),
                    dcc.Graph(
                        id='modal_graph',
                        figure=figX
                    )
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            is_open=False,
            id="modal",
            centered=True,
            size="lg",
            style={'position': 'fixed', 'width': '50%', 'zIndex': 9999, 'border-color':"black", 'margin-left':"20%", 'margin-top':"10%", 'margin-bottom':"10%",  'top': 0, 'left': 0, 'right': 0, 'bottom': 0},
            fade=True
        )





# app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = dbc.Container([
        html.Div(
        children = [
            html.Div(
                className = "content",
                children=[
                    html.Header(
                        style={'color':'#7FDBFF'},
                    ),
                    html.Div(className = "dropdown",
                             children = [
                                dcc.Dropdown(
                                id="picked_day",
                                options=[                  
                                        {'label': 'Today', 'value': 29},
                                        {'label': 'Yesterday', 'value': 30},
                                ],
                                value = 29,
                    )
                             ],
                             style={"width": "25%"})
                    ,
                    html.Div(dcc.Graph(id='heatmap'),
                            style={'padding-left':'0px', 'width':'100%'}),
                    html.Div(dcc.Graph(id='routine',
                                    #    hoverData={'points': [{'pointNumber': None}]}
                                    ),
                            style={'width':'100%'},
                            ),
                    modal,
                    dbc.Row(
                        dbc.Col(dbc.Button("Other Pages", id="open"), className="text-right", width=12),
                        justify="end"
                    ),
                    navigationModal
                ]
            )
        ]
    ) 
])

@callback(Output("heatmap", "figure"), Input("picked_day", "value"))
def updateGraph(picked_day):
    new_esm_df = esm_df.loc[(esm_df['month']==4) & (esm_df['day']==picked_day)]
    z = [new_esm_df.Attention.to_numpy()]
    fig1 = ff.create_annotated_heatmap(z, colorscale='Viridis')
    fig1.update_layout(height=200, width=1050)
    
    return fig1

@callback(Output("routine", "figure"),[ Input("picked_day", "value"), Input("routine", "hoverData")])
def updateRoutine(picked_day, hoverData):
    if(picked_day==29):
        app_df = pd.read_csv(dir_path + '/User3041/AppUsageStatEntity-5565824000.csv')
        # ph_df = pd.read_csv(dir_path + '/P3041/PhysicalActivityEventEntity-5565824000.csv')
    else:
        app_df = pd.read_csv(dir_path + '/User3041/AppUsageStatEntity-5571008000.csv')
        # ph_df = pd.read_csv(dir_path + '/P3041/PhysicalActivityEventEntity-5571008000.csv')
    
    # app_df = app_df.drop_duplicates(subset='timestamp', keep='first')
    app_df.timestamp = pd.to_datetime(app_df.timestamp)

    # ph_df = pd.read_csv(dir_path + '/P3041/PhysicalActivityEventEntity-5571008000.csv')
    # ph_df.timestamp = pd.to_datetime(ph_df.timestamp)
    # ph_df = ph_df.loc[(ph_df.confidence>=0.98) & (ph_df.type != 'STILL') & (ph_df.type != 'UNKNOWN') & (ph_df.type != 'TILTING')]
    # ph_df.rename(columns={'type': 'name'}, inplace=True)
    # merged_df = pd.merge(app_df, ph_df, how="outer", on=['timestamp', 'name'])
    ac = ["activity"] * len(app_df)

    fig2 = px.bar(app_df,x='timestamp', y=ac, color='name', orientation='h')
    fig2.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', paper_bgcolor='white')
    fig2.update_yaxes(showticklabels=False, showgrid=False)
    fig2.update_xaxes(title='time')
    fig2.update_traces(hovertemplate="<b>%{x}</b>", 
                  hoverinfo='text', 
                #   line=dict(color='#1f77b4', width=3, opacity=0.7),
                  hoverlabel=dict(bgcolor='#1f77b4'))
    # if hoverData is not None:
    #     point_index = hoverData['points'][0]['pointIndex']
    #     fig2.data[point_index].marker.line.width = 2
    #     fig2.data[point_index].marker.line.color = 'black'
    #     # fig2.data[point_index].text = fig2.data[point_index]['y']
    # else:
    #     for trace in fig2.data:
    #         trace.marker.line.width = 0
    #         trace.marker.line.color = 'rgba(0, 0, 0, 0)'
    #         trace.text = None
    
    return fig2

@callback(
    Output("modal", "is_open"),
    # Output("hover_info","children"),
    [Input("routine", "clickData"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)

def toggle_modal(hover_data,close_button, is_open):
    # return is_open, hover_data
    if hover_data or close_button:
        # x = hover_data['points'][0]['x']
        # y = hover_data['points'][0]['y']
        # text = "x = "+str(x)+" & y = "+str(y)
        # , str(hover_data['points'][0]['value'])
        return not is_open
    return is_open

@callback(
    Output("nav_modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# if __name__ == '__main__':
#     app.run_server(debug=True)
