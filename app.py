
#%%
from dash import html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import json
from dash.exceptions import PreventUpdate
from helper_components import (
                               plot_histogram,
                               plot_scatterplot,
                               make_boxplot,
                               CorrelationMatrix, plot_histogram,
                               plot_scatterplot, make_boxplot
                               )
import dash
from style import homepage_icon_style
from builders import (main_layout, app_description, explore_layout,
                      histogram_layout, boxplot_layout, histogram_layout,
                      scatter_layout, prediction_layout,
                      multicoll_layout, intro_layout
                      )
import builders
import logging
from urllib.parse import unquote
import joblib
import functools
import plotly.express as px


loaded_model = joblib.load(filename="/home/lin/codebase/trivago_app/bagging.model")
data = pd.read_csv(r"/home/lin/codebase/trivago_app/Data/train_set.csv")

#%%
app = dash.Dash(__name__, external_stylesheets=[
                                                dbc.themes.SOLAR,
                                                dbc.icons.BOOTSTRAP,
                                                dbc.icons.FONT_AWESOME
                                            ],
                suppress_callback_exceptions=True,
                )

app.layout = main_layout

app.validation_layout = html.Div(
    [main_layout, explore_layout, app_description, prediction_layout,
     histogram_layout,
     scatter_layout, boxplot_layout,
     multicoll_layout, intro_layout
     ]
)


# %%
@app.callback(
    Output(component_id="main_content", component_property="children"),
    Input(component_id="location", component_property="href"),
)
def show_page_display(href):
    site_page = href
    site_to_view = site_page.split("/")[-1]
    if site_to_view == "explore":
        return explore_layout
    elif site_to_view == 'predict':
        return prediction_layout
    else:
        return app_description


@app.callback(
    Output("page_content", "children"),
    [
        Input("id_hist", "n_clicks_timestamp"),
        Input("id_boxplot", "n_clicks_timestamp"),
        Input("id_scatter", "n_clicks_timestamp"),
        Input("id_corr", "n_clicks_timestamp"),
    ],
)
def sidebar_display(hist: str, boxplot: str, scatter: str, corr: str):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if not ctx.triggered:
        return intro_layout
    elif button_id == "id_hist":
        return histogram_layout
    elif button_id == "id_boxplot":
        return boxplot_layout
    elif button_id == "id_scatter":
        return scatter_layout
    elif button_id == "id_corr":
        return multicoll_layout
    else:
        return intro_layout

@functools.lru_cache(maxsize=None)
@app.callback(Output(component_id='missing_para_popup', component_property='is_open'),
              Output(component_id='desc_popup', component_property='children'),
              Output(component_id='prediction_output', component_property='children'),
              Input(component_id='submit_parameters', component_property='n_clicks'),
              Input(component_id='input_city_id', component_property='value'),
              Input(component_id='input_content_score', component_property='value'),
              Input(component_id='input_n_images', component_property='value'),
              Input(component_id='input_distance_to_center', component_property='value'),
              Input(component_id='input_avg_rating', component_property='value'),
              Input(component_id='input_stars', component_property='value'),
              Input(component_id='input_n_reviews', component_property='value'),
              Input(component_id='input_avg_rank', component_property='value'),
              Input(component_id='input_avg_price', component_property='value'),
              Input(component_id='input_avg_saving_percent', component_property='value')
              )
def make_prediction(button_click, city_id, contest_score,n_images,
                    distance_center, avg_rating, stars, n_reviews,
                    avg_rank, avg_price, avg_saving):
    inputs = [city_id, contest_score, n_images,
                  distance_center, avg_rating, stars, n_reviews,
                  avg_rank, avg_price, avg_saving
                  ]
    if not any(inputs):
        PreventUpdate

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'submit_parameters':

        if not all(inputs):
            message = ('All parameters must be provided. Either some values have not \
                        been provided or invalid values were provided. Please select the \
                       right values for all parameters from the dropdown. \
                        Then, click on predict clicks button to \
                        predict number of clicks'
                       )
            return True, message, dash.no_update

        if all(inputs):
            res = loaded_model.predict([inputs])
            prediction = round(res[0])
            return False, dash.no_update, prediction


@functools.lru_cache(maxsize=None)
@app.callback(Output(component_id='scatter_graph', component_property='figure'),
              Input(component_id='variable_select', component_property='value')
              )
def render_graph(variable_selected):
    if not variable_selected:
        PreventUpdate
    return plot_scatterplot(data=data, x_colname=variable_selected)

@functools.lru_cache(maxsize=None)
@app.callback(Output(component_id='hist_graph', component_property='figure'),
             Input(component_id='hist_variable_select', component_property='value')
             )
def render_hist_graph(hist_variable_selected):
    if not hist_variable_selected:
        PreventUpdate
    return plot_histogram(data=data, colname=hist_variable_selected)

@functools.lru_cache(maxsize=None)
@app.callback(Output(component_id='boxplot_graph', component_property='figure'),
              Input(component_id='boxplot_variable_select', component_property='value')
              )
def render_boxplot_graph(boxplot_variable_selected):
    if not boxplot_variable_selected:
        PreventUpdate
    return make_boxplot(data=data, variable_name=boxplot_variable_selected)


@app.callback(Output(component_id='project_canvans', component_property='is_open'),
              Input(component_id='proj_desc', component_property='n_clicks'),
              State(component_id='project_canvans', component_property='is_open')
              )
def toggle_project_description(proj_desc_button_clicked: str, is_open: bool) -> bool:
    """
    This function accepts click event input and the state of canvas component,
    and change the state of the canvans component when a click occurs

    Parameters
    ----------
    proj_desc_button_clicked : str
        This parameter is a count of each click made on a button.
    is_open : bool
        Has the values True or False that specifies whether the canvas component is opened or not.

    Returns
    -------
    bool
        Has values True or False that determines whether the canvans component should be open.

    """
    if proj_desc_button_clicked:
        return not is_open
    else:
        return is_open



if __name__=='__main__':
    app.run(port=8088, debug=False, use_reloader=False)


