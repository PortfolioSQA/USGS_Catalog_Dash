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
from etl import create_dfs

# import plotly.express as px
import plotly.graph_objs as go
# from plotly.graph_objs import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#load data
sample_data = pd.read_csv('sdc_sample.csv')
df_map, df_US, df_earth = create_dfs(sample_data)

    
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
            lon=-95,
            lat=39.7342
        ),
        zoom=1.5,
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
                        html.P('Select Dates:'),
                        dcc.Slider(
                            id = 'dates',
                            min=1790,
                            max=2020,
                            step=None,
                            marks={
                                1790: 'Pre-1800',
                                1900: '1900',
                                1920: '1920',
                                1940: '1940',
                                1960: '1960',
                                1980: '1980',  
                                2000: '2000',
                                2020: 'present'
                            },
                            value = 2020
                        )  
                        # dcc.Checklist(
                        #         id = 'dates',
                        #         options=[
                        #             {'label': '2000', 'value': '2000'},
                        #             {'label': '2001', 'value': '2001'},
                        #             {'label': '2002', 'value': '2002'},
                        #             {'label': '2003', 'value': '2003'},
                        #             {'label': '2004', 'value': '2004'},
                        #             {'label': '2005', 'value': '2005'},
                        #             {'label': '2006', 'value': '2006'},
                        #             {'label': '2007', 'value': '2007'},
                        #         ],
                        #         value = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', 'nan'],
                        #         labelStyle={'display': 'inline-block'}
                        # ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                    ),
                html.Div(
                    [
                        html.P('Select Science Center:'),
                        dcc.Dropdown(
                            id='sci_topic',
                            options= [{'label': str(item),'value': str(item)}
                                      for item in set(df_map['sci_center'])],
                            # multi=True,
                            value= "Fort Collins Science Center")
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
                                  style={'margin-top': '20'})
                    ], className = "six columns"
                ),
                html.Div(
                    [
                        dash_table.DataTable(id='datatable',
                                columns=[{"name": i, "id": i} for i in ["sci_center", "kw"]],
                                style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                },
                                data=df_map.to_dict('records'),
                                editable=True,
                                sort_action="native",
                                sort_mode="multi",
                                # row_selectable="multi",
                                # selected_rows=[],
                                page_action="native",
                                page_current= 0,
                                page_size= 10,
                                )
                    ], className="six columns"
                ),
                html.Div([
                        dcc.Graph(
                            id='agg-graph'
                        )
                    ], className= 'twelve columns'
                    ),
            ], className="row")
        ], className='ten columns offset-by-one')
    )

@app.callback(
    Output('datatable', 'data'),
    [Input('dates', 'value'),
      Input('sci_topic', 'value')])
def table_selection(dates, sci_center):
    # if len(dates) == 0:
    #     return no_update
    if len(sci_center) == 0:
        return no_update
    df_ms = df_map.copy()
    df_ms = df_ms[df_ms['beg_year']< int(dates)]
    df_ms = df_ms.loc[df_ms['sci_center'] == sci_center]
    return df_ms.to_dict("records")
def update_selected_row_indices(dates, sci_center):
    # if len(dates) == 0:
    #     return no_update
    if len(sci_center) == 0:
        return no_update
    map_aux = df_map.copy()
    map_aux = map_aux[map_aux['beg_year'] < int(dates)]
    map_aux = map_aux.loc[map_aux["sci_center"] == sci_center]
    rows = map_aux.to_dict('records')
    return rows

@app.callback(
    Output('map-graph', 'figure'),
    [Input('datatable', 'data')])
def map_selection(data):
    aux = pd.DataFrame(data)
    if len(data) == 0:
        return no_update
    else:
        return {
            "data": [{
                    "type": "scattermapbox",
                    "lat": list(aux['lat']),
                    "lon": list(aux['lon']),
                    "hoverinfo": "text",
                    "hovertext": [["{}".format(i)]
                                    for i in aux['sci_center']],
                    "mode": "markers+text",
                    "name": list(aux['sci_center']),
                    "marker": {
                        "size": 8,
                        "opacity": 0.7},
            }],
            "layout": layout_map
        }



@app.callback(
    Output('agg-graph', 'figure'),
    [Input('datatable', 'data')])
def update_figure(data):
    if len(data) == 0:
        return no_update
    dff = pd.DataFrame(data)
    layout = go.Layout(
        bargap=0.05,
        bargroupgap=0,
        barmode='group',
        showlegend=False,
        dragmode="select",
        xaxis=dict(
            showgrid=False,
            nticks=50,
            fixedrange=False
        ),
        yaxis=dict(
            showticklabels=True,
            showgrid=False,
            fixedrange=False,
            rangemode='nonnegative',
            zeroline= False 
        )
    )
    data = go.Bar(
              x=dff['sci_center'],
              y=dff.groupby('sci_center', as_index = False).count()["sci_center"]
          )
    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)