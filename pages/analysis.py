import dash, plot_fig
from dash import dcc, html, Dash, Input, Output, State, ALL, Patch
import dash_bootstrap_components as dbc
from datetime import date
import plotly.express as px
import datetime
from dash import callback
from dash import get_asset_url


external_stylesheets = [dbc.themes.BOOTSTRAP]
# app = Dash(__name__, external_stylesheets=external_stylesheets)

# inferences_fake/figs_fake should be generated from elsewhere
inferences_fake = ['High correlation between your most productive days and more than 7 hours of sleep', 'High correlation between your least productive days and high amount of phone use']
figs_fake = [plot_fig.main_fig]*3
inferences_dash_list = []
for idx, (inference, fig) in enumerate(zip(inferences_fake, figs_fake)):
    div = html.Div(
                        [
                            dbc.Button(
                                inference,
                                id={"type": "collapse-button", "index": idx},
                                className="mb-1",
                                color="gray",
                                n_clicks=0,
                            ),
                            dbc.Collapse(
                                dbc.Card(dbc.CardBody(
                                    dcc.Graph(figure=fig),
                                )),
                                id={"type": "collapse", "index": idx},
                                is_open=False,
                            ),
                        ]
                    )
    inferences_dash_list.append(div)


graph_types=['Weekly Productivity', 'Monthly Productivity', 'Activity Analysis', 'Weekly Key Metrics (S+A) Levels']
comparison_types=['Self', 'All users', 'Best users', 'Worst users']


#Web format
layout = dbc.Container([
        html.Div(
        [
            # dbc.NavbarSimple(
            #     [
            #         dbc.Button("Main page", color="light", className='btn btn-outline-Secondary'),
            #     ],
            #     brand='Analysis',
            #     sticky="top",
            #     color='dark',
            #     dark='True',
            # ),
            dbc.Container(
                [
                    # range select
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("Graph", style={'font-weight': 'bold'}),
                                        dbc.Select(
                                            options=[{'label': i, 'value': i} for i in graph_types],
                                            id="graph-select",
                                            placeholder=graph_types[0],
                                            size='sm',
                                            value=graph_types[0]
                                        ),
                                    ]
                                ),
                                width=2,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("Comparison", style={'font-weight': 'bold'}),
                                        dbc.Select(
                                            options=[{'label': i, 'value': i} for i in comparison_types],
                                            id="comparison-select",
                                            placeholder=comparison_types[0],
                                            size='sm',
                                            value=comparison_types[0],
                                        )
                                    ]
                                ),
                                width=2,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Label("Start date", style={'font-weight': 'bold', 'margin-bottom': '0'}),
                                        html.Br(),
                                        dcc.DatePickerSingle(
                                            id='startDate-select',
                                            min_date_allowed=date(2018, 1, 5),
                                            max_date_allowed=date(2023, 9, 19),
                                            initial_visible_month=date(2019, 4, 1),
                                            date=date(2019, 4, 28),
                                        ),
                                    ],
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    dbc.Button(
                                        [html.Img(src = get_asset_url('q.jpg'), height='70'),],
                                        id="hover-target",
                                        color="white",
                                        n_clicks=0,
                                    ),
                                    dbc.Popover(
                                        [
                                            dbc.PopoverHeader("Plot Explanation"),
                                            dbc.PopoverBody("", id='explantion-body'),
                                        ],
                                        target="hover-target",
                                        trigger="hover",
                                        # style={'width': '300px'}
                                    ),
                                ],
                                width={"size": 1, "offset": 3},
                            ),

                        ],
                        style={"height": "15vh", "background-color": "white"},
                        align='center',
                    ),

                    # plots
                    dbc.Row(
                        "",
                        style={"height": "70vh"},
                        align="center",
                        justify="center",
                        id='figs',
                    ),

                    # inference
                    dbc.Row(
                        html.Div(
                            [
                                html.H4("Inference", className="mt-3"),
                            ] + inferences_dash_list,
                        ),
                        style={"background-color": "rgb(173, 181, 189)", 'border-radius': '5px', },
                        className="text-white"
                    ),
                    dbc.Row(style={"height": "5vh"},)
                ]
            ),
        ],
    ) 
])



# see "dash: pattern matching callback"
@callback(
    Output({"type": "collapse", "index": ALL}, "is_open"),
    [Input({"type": "collapse-button", "index": ALL}, "n_clicks")],
)
def toggle_collapse(n):
    return [False if n_click % 2 == 0 else True for n_click in n]



# for plots
@callback(
    Output("figs", "children"),
    Input("graph-select", "value"),
    Input("comparison-select", "value"),
    Input("startDate-select", "date"),
    Input("user-dropdown", "value")
)
def fig_callback(graph_type, comparison_type, start_date, value):
    fig = plot_fig.plot_main(graph_type, comparison_type, date.fromisoformat(start_date), value)
    return fig



# plot explantion popover callback
@callback(
    Output("explantion-body", "children"),
    Input("graph-select", "value"),
    Input("comparison-select", "value"),
    Input("startDate-select", "date"),
)
def popover_callback(graph_type, comparison_type, start_date):

    if graph_type == graph_types[0]:
        body = 'In this plot, x-axis represents the 7 days of the week. On the y-axis, the function y = 1/(work time) is plotted.'
    elif graph_type == graph_types[1]:
        body = 'In this plot, starting from the selected date, each slot indicates the users productivity'
    elif graph_type == graph_types[2]:
        body = 'In this plot, user can use the button to hightlight the selected activity type on the pie chart.\
            Further click will show detail app usage distribution of the selected activity type.'
    elif graph_type == graph_types[3] or graph_type == graph_types[4]:
        body = 'In this plot, “S” stands for stress and “A” stands for attention.\
            On x-axis days of the weeks are plotted while on the y-axis relevant characteristic is depicted.'

    return body


# if __name__ == '__main__':
#     app.run_server(debug=True)