#%%
import dash_bootstrap_components as dbc
from dash import html, dcc
from numpy import place
from style import homepage_icon_style, page_style, input_style, button_style
import dash_trich_components as dtc
from helper_components import (create_offcanvans, output_card,
                               plot_histogram, plot_scatterplot, make_boxplot,
                               CorrelationMatrix
                               )
import pandas as pd
from PIL import Image

#%%
#img_explore = Image.open('/home/linagb/mysite/img/img_explore.png')
#img_ml = Image.open('/home/linagb/mysite/img/img_clickprediction.jpeg')
#img_scq = Image.open('/home/linagb/mysite/img/SCQ.png')

img_explore = Image.open('/home/lin/codebase/trivago_app/img/img_explore.png')
img_ml = Image.open('/home/lin/codebase/trivago_app/img/img_clickprediction.jpeg')
img_scq = Image.open('/home/lin/codebase/trivago_app/img/SCQ.png')

#%%
#data = pd.read_csv(r"/home/linagb/mysite/Data/train_set.csv")
data = pd.read_csv(r"/home/lin/codebase/trivago_app/Data/train_set.csv")
corr = CorrelationMatrix(data=data)
corr_data = corr.create_correlation()

corr_fig = corr.plot_correlation(corr_matrix=corr_data)

#data=data[['n_clicks', 'n_clicks']].dropna()
#%%
variables=['content_score', 'n_images',
            'distance_to_center', 'avg_rating',
            'stars', 'n_reviews', 'avg_rank',
            'avg_price', 'avg_saving_percent',
            'n_clicks'
            ]

main_layout = html.Div(
    [
        dbc.NavbarSimple(
            brand="Home",
            brand_href="/",
            light=True,
            brand_style={"color": "#FFFFFF", "backgroundColor": "#FF8B00"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Location(id="location"),
                        html.Div(id="main_content"),
                        dcc.Loading(
                            id="loading_cach_data_stored",
                            type="cube",
                            fullscreen=True,
                            children=[dcc.Store(id="cach_data_stored")
                                      ],
                        ),
                    ]
                )
            ]
        ),
    ],
    style=page_style,
)


app_description = dbc.Container(
    style=page_style,
    children=[
        dbc.Row(html.H2("Click prediction", style=input_style)),

        dbc.Row(
            children=[
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    src=img_explore,
                                    top=True,
                                    style=homepage_icon_style,
                                ),
                                dbc.CardLink(
                                    children=[
                                        dbc.CardImgOverlay(
                                            [
                                                dbc.CardBody(
                                                    html.H1(
                                                        "Exploratory Analysis",
                                                        style={"margin": "5%", 'color': '#FF8B00'},
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    href="explore",
                                ),
                            ],
                            style={"width": "18rem", "height": "18rem"},
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    src=img_ml,
                                    top=True,
                                    style=homepage_icon_style,
                                ),
                                dbc.CardLink(
                                    children=[
                                        dbc.CardImgOverlay(
                                            [
                                                dbc.CardBody(
                                                    html.H1(
                                                        "Click Prediction",
                                                        style={"margin": "5%", 'color': '#FF8B00'},
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    href="predict",
                                ),
                            ],
                            style={"width": "18rem", "height": "18rem"},
                        )
                    ]
                ),
            ]
        ),

        html.Br(),

        dbc.Row(
            [

              dbc.Col(lg=1),
              dbc.Col(lg=6,
                    children=[
                        dbc.Label('Business Problem Design'), html.Br(),
                        dbc.Card(
                            [
                                dbc.CardImg(
                                    src=img_scq,
                                    top=True,
                                    style=homepage_icon_style,
                                ),
                            ],
                        )
                    ]
                ),
              dbc.Col(lg=5)


            ]
        )
    ]
)


explore_layout = html.Div(
    [
        dtc.SideBar(
            [
                dtc.SideBarItem(id="id_hist", label="Visualize data distribution",
                                icon="fas fa-chart-bar"
                                ),
                dtc.SideBarItem(id="id_boxplot", label="Visualize Outliers",
                                icon="fas fa-chart-line"
                                ),
                dtc.SideBarItem(id="id_scatter", label="Visualize relationship",
                                icon="fas fa-chart-area"
                                ),

                dtc.SideBarItem(id="id_corr", label="Estimate correlation",
                                icon="fas fa-signal"
                                ),
            ],
            bg_color="#0088BC",
        ),
        html.Div([], id="page_content"),
    ]
)

histogram_layout = html.Div(
    children=[
        dbc.Row([
            dbc.Col(lg=3,
                    children=[
                        dbc.Label('Select variable to plot histogram', style=input_style),
                        html.Br(),
                        dcc.Dropdown(id='hist_variable_select',
                                 options=[{'label': var, 'value': var}
                                          for var in variables
                                          ]
                                 )
                            ]
                    ),
            dcc.Loading(type='circle',
            children=[dbc.Col(lg=9,
                            children=[
                                dcc.Graph(id='hist_graph')
                            ]

                        )
                    ]
            )
        ])
    ]
)

boxplot_layout = html.Div(
    children=[
        dbc.Row([
            dbc.Col(lg=3,
                    children=[
                        dbc.Label('Select variable for boxplot', style=input_style),
                        html.Br(),
                        dcc.Dropdown(id='boxplot_variable_select',
                                 options=[{'label': var, 'value': var}
                                          for var in variables
                                          ]
                                 )
                            ]
                    ),
            dcc.Loading(type='circle',
            children=[dbc.Col(lg=9,
                            children=[
                                dcc.Graph(id='boxplot_graph')
                            ]

                        )
                    ]
            )
        ])
    ]
)



scatter_layout = html.Div(
    children=[
        dbc.Row([
            dbc.Col(lg=3,
                    children=[
                        dbc.Label('Select Variable to plot scatterplot with n_clicks', style=input_style),
                        html.Br(),
                        dcc.Dropdown(id='variable_select',
                                 options=[{'label': var, 'value': var}
                                          for var in variables
                                          ]
                                 )
                            ]
                    ),
            dcc.Loading(type='circle',
            children=[dbc.Col(lg=9,
                            children=[
                                dcc.Graph(id='scatter_graph')
                            ]

                        )
                    ]
            )
        ])
    ]
)

multicoll_layout = html.Div(
    children=[dbc.Row(
                    dcc.Loading(type='circle',
                                children=[dbc.Col(id='corr_graph',
                                             children=[dcc.Graph(id='multicorr_graph',
                                                                 figure=corr_fig
                                                                 )
                                                       ]
                                        )
                                          ]
                            )
                )
              ]
)


prediction_layout = html.Div(
    children=[
        dbc.Row([
              dbc.Col([
                  dbc.Modal(id='missing_para_popup', is_open=False,
                      children=[
                      dbc.ModalBody(id='desc_popup')
                  ])
              ]
                      )
             ]
            ),

        dbc.Row([
        html.Br(), html.Br(),
        dbc.Col(dbc.Button('Project description',
                           id='proj_desc',
                           n_clicks=0,
                           style=button_style

                           )
            ),
        dbc.Col(children=[
                        html.Div(
                                children=[create_offcanvans(id='project_canvans',
                                                    title='Clicks Predictor',
                                                    is_open=False
                                                    )
                                            ]
                            ),
                        ]
                )
    ]),

    dbc.Row(
        children=[
            output_card(id="prediction_output",
                        card_label="Clicks Prediction",
                        card_size=2,
                        icon = 'fas fa-mouse-pointer'
                        ),

            dbc.Col(
                children=[
                    dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        dbc.Label('Describes content quality provided for hotel from 0 (worst) to 100 (best)',
                                                  style=input_style
                                                  ),
                                        html.Br(),
                                        dcc.Input(id='input_content_score',
                                                placeholder="content score",
                                                min=0, max=100, type='number',
                                                debounce=True
                                            )
                                    ]
                                    ),
                                dbc.Col(
                                    children=[
                                        dbc.Label('Number of images that are available for the given hotel',
                                                  style=input_style
                                                  ),
                                        html.Br(),
                                        dcc.Input(id='input_n_images', placeholder='number of images',
                                                  type='number',
                                                  min=0, debounce=True
                                                  )

                                    ]
                                    ),
                                dbc.Col(
                                    children=[
                                        dbc.Label('Distance (in meters) of the hotel to the nearest city center',
                                                  style=input_style
                                                  ),
                                        html.Br(),
                                        dcc.Input(id='input_distance_to_center',
                                                  placeholder='Distance to center',
                                                  type='number',
                                                  min=1, debounce=True
                                                  )
                                    ]
                                )
                                ]
                        ),
                    html.Br(),
                    dbc.Row(
                        children=[
                                dbc.Col(
                                    children=[
                                        dbc.Label('Average rating of the hotel on a scale from 0 (worst) to 100 (best)',
                                                  style=input_style
                                                  ),
                                        html.Br(),
                                        dcc.Input(id='input_avg_rating',
                                                  placeholder='Average rating',
                                                  type='number',
                                                  min=1, debounce=True
                                                )
                                    ]
                                    ),
                                dbc.Col(
                                    children=[
                                        dbc.Label('Stars for the hotel from 1 (worst) to 5 stars (best)',
                                                  style=input_style
                                                  ),
                                        html.Br(),
                                        dcc.Input(id='input_stars',
                                                  placeholder='Number of Stars', type='number',
                                                  min=1, max=5, debounce=True
                                                )
                                    ]
                                    ),
                                dbc.Col(
                                    children=[
                                        dbc.Label('Number of reviews that are available for that hotel',
                                                  style=input_style
                                                  ),
                                        html.Br(),
                                        dcc.Input(
                                            id='input_n_reviews',
                                            placeholder='Number of reviews',
                                            type='number', min=0, debounce=True
                                        )
                                    ]
                                )
                                ]
                    ),
                    html.Br(),
                    dbc.Row(
                        children=[
                                dbc.Col(
                                    children=[
                                        dbc.Label('Average position the hotel had in the list',
                                                  style=input_style
                                                ),
                                        html.Br(),
                                        dcc.Input(
                                            id='input_avg_rank',
                                            placeholder='Average rank, minimum value is 1, maximum value is 100',
                                            type='number', min=1, max=100, debounce=True
                                        )
                                    ]
                                    ),
                                dbc.Col(
                                    children=[
                                        dbc.Label('Average price in Euro of the hotel',
                                                  style=input_style
                                                ),
                                        html.Br(),
                                        dcc.Input(
                                            id='input_avg_price',
                                            placeholder='Average price, minimum is 0',
                                            type='number', min=1, debounce=True
                                        )
                                    ]
                                    ),
                                dbc.Col(
                                    children=[
                                        dbc.Label('Average saving users achieve on this hotel by using trivago',
                                                  style=input_style
                                                  ),
                                        html.Br(),
                                        dcc.Input(
                                            id='input_avg_saving_percent',
                                            placeholder='Average saving percent, minimum is 0',
                                            type='number', min=1, debounce=True
                                        )
                                    ]
                                )
                                ]
                    ),
                    html.Br(),
                    dbc.Row(
                        children=[
                            dbc.Col(lg=4,
                                children=[
                                            dbc.Label('Describes the city the hotel is located in',
                                                      style=input_style
                                                      ),
                                            html.Br(),
                                            dcc.Input(
                                                id='input_city_id',
                                                placeholder='Select city_id',
                                                min=1, max=878736, type='number', debounce=True
                                            )
                                        ]
                            ),

                            dbc.Col(lg=4,
                                   children=[
                                    #html.Br(),
                                    dbc.Label(''),
                                    dbc.Button(id='submit_parameters',
                                                children='Predict Clicks',
                                                style=button_style
                                            )
                                ]
                            )

                        ]
                    )

                ]
            )
        ]
    )
    ]
)

intro_layout = dbc.Container(
    children=[
        dcc.Markdown(
            '''
                ### Exploratory analysis and visualization

                Exploratory analysis provides important insights that describes the data
                and serves as basis on which to narrow down the selection of algorithmns
                that will produce good results.

                #### Visualizations
                Various plots are use to visualize characteristics of the data
                to ascertain if certain assumptions are met for certain models to be used.

                __Histogram__: is used to visualize the distribution of data for
                                continuous variables.

                The result shows that most of the variables are right skewed.


                __Boxplot__: is used to visualize the presence of outliers for various
                            variables.

                __Scatterplot__: is used to visualize whether there is a linear relationship
                                between predictor variables and the outcome variable.

                __Heatmap__: is used to visualize correlation between variables


                Click to expand the sidebar and visualize the results.

            ''', style=input_style
        )
    ]
)





