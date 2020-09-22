#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:33:04 2020

@author: sashaqanderson
"""
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
from dash.dash import no_update
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

# import plotly.express as px
import plotly.graph_objs as go
# from plotly.graph_objs import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

sample_data = pd.read_csv('sample_data.csv')
sample_data2 = sample_data[['name', 'date', 'mission_area','science_topic', 'lat_n', 'lon_w']]

    
# mapbox://styles/sdc-dash/ckf36pfn30e2119nyjf4nfycy
mapbox_access_token = 'pk.eyJ1Ijoic2RjLWRhc2giLCJhIjoiY2tmMzZqb21vMDA2ejJ1cGdjeDg5OGRiOCJ9.alrKKaVlRO4DIJmMWYY1WQ'
# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='SDC Datasets',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        # style="light",
        center=dict(
            lon=-80,
            lat=35.7342
        ),
        zoom=3,
    )
)


app.layout = html.Div(
    html.Div([
        html.Div(
            [
                html.H1(children='Working SDC Query Dashboard',
                        className='nine columns'),
                html.Br(),
                html.Br(),
            ], className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P('Select Mission Area(s):'),
                        dcc.Checklist(
                                id = 'miss_area',
                                options=[
                                    {'label': 'Core Science Systems', 'value': 'Core Science Systems'},
                                    {'label': 'Ecosystems', 'value': 'Ecosystems'},
                                    {'label': 'Energy and Minerals', 'value': 'Energy and Minerals'},
                                    {'label': 'Environmental Health', 'value': 'Environmental Health'},
                                    {'label': 'Land Resources', 'value': 'Land Resources'},
                                    {'label': 'Natural Hazards', 'value': 'Natural Hazards'},
                                    {'label': 'Regional Offices', 'value': 'Regional Offices'},
                                    {'label': 'Water Resources', 'value': 'Water Resources'}
                                ],
                                value = [
                                    'Core Science Systems',
                                    'Ecosystems',
                                    'Energy and Minerals',
                                    'Environmental Health',
                                    'Land Resources',
                                    'Natural Hazards',
                                    'Regional Offices',
                                    'Water Resources'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                    ),
                html.Div(
                    [
                        html.P('Select Science Topic(s) from dropdown menu:'),
                        dcc.Dropdown(
                            id='sci_topic',
                            options= [{'label': str(item),'value': str(item)}
                                      for item in set(sample_data['science_topic'])],
                            # multi=True,
                            value= "Energy Resources")
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                )],
            className='row' ),
     # Map + table + Histogram
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='map-graph',
                                  animate=True,
                                  style={'margin-top': '20'})
                    ], className = "six columns"
                ),
                html.Div(
                    [
                        dash_table.DataTable(id='datatable',
                                columns=[{"name": i, "id": i} for i in sample_data2.columns],
                                data=sample_data2.to_dict('records'),
                                editable=True,
                                sort_action="native",
                                sort_mode="multi",
                                row_selectable="multi",
                                selected_rows=[],
                                page_action="native",
                                page_current= 0,
                                page_size= 10,
                                style_table={
                                    'overflowY': 'scroll',
                                    })
                    ], className="six columns"
                ),
                html.Div([
                        dcc.Graph(
                            id='bar-graph'
                        )
                    ], className= 'twelve columns'
                    ),
            ], className="row")
        ], className='ten columns offset-by-one')
    )

@app.callback(
    Output('datatable', 'data'),
    [Input('miss_area', 'value'),
     Input('sci_topic', 'value')])
def table_selection(miss_area, sci_topic):
    df_ms = sample_data2.copy()
    df_ms = df_ms[df_ms['mission_area'].isin(miss_area)]
    df_ms = df_ms.loc[df_ms['science_topic'] == sci_topic]
    return df_ms.to_dict("records")
def update_selected_row_indices(miss_area, sci_topic):
    map_aux = sample_data.copy()
    map_aux = map_aux[map_aux['mission_area'].isin(miss_area)]
    map_aux = map_aux.loc[map_aux["science_topics"] == sci_topic]
    rows = map_aux.to_dict('records')
    return rows

def gen_map(d):
    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.
    return {
        "data": [{
                "type": "scattermapbox",
                "lat": list(d['lat_n']),
                "lon": list(d['lon_w']),
                "hoverinfo": "text",
                "hovertext": [["{} <br>{} <br>{}".format(i,j,k)]
                                for i,j,k in zip(d['name'], d['mission_area'],d['science_topic'])],
                "mode": "markers",
                "name": list(d['name']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
    }

@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'data')])
def map_selection(data):
    aux = pd.DataFrame(data)
    if len(data) == 0:
        return no_update
    return gen_map(aux)

# @app.callback(
#     Output('bar-graph', 'figure'),
#     [Input('datatable', 'data')])
# def update_figure(data):
#     dff = pd.DataFrame(data)
#     layout = go.Layout(
#         bargap=0.05,
#         bargroupgap=0,
#         barmode='group',
#         showlegend=False,
#         dragmode="select",
#         xaxis=dict(
#             showgrid=False,
#             nticks=50,
#             fixedrange=False
#         ),
#         yaxis=dict(
#             showticklabels=True,
#             showgrid=False,
#             fixedrange=False,
#             rangemode='nonnegative',
#             zeroline='hidden'
#         )
#     )
#     data = go.Bar(
#               x=dff.groupby('mission_area', as_index = False).count()['mission_area'],
#               y=dff.groupby('mission_area', as_index = False).count()['science_topic']
#           )
#     return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)