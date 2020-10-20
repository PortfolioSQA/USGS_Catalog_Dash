import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from etl import create_dfs
from dash.dash import no_update
import flask

import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from wordcloud import WordCloud, STOPWORDS 
from io import BytesIO
import base64
import urllib

server = flask.Flask('app')

# sample data
# df = pd.read_csv("solar.csv")

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True

mapbox_access_token = 'pk.eyJ1Ijoic2RjLWRhc2giLCJhIjoiY2tmMzZqb21vMDA2ejJ1cGdjeDg5OGRiOCJ9.alrKKaVlRO4DIJmMWYY1WQ'

#load data
sample_data = pd.read_csv('sdc_sample.csv')
df_map = create_dfs(sample_data)

# get a set of sorted science centers
SC = set(df_map['sci_center'])
sorted_SC = sorted(SC)

# helper function to plot wordcloud
def plot_wordcloud(data):
    df = pd.DataFrame(data)
    comment_words = '' 
    stopwords = set(STOPWORDS) 
    # iterate through the csv file 
    for val in df.all_kw: 
        # typecaste each val to string 
        val = str(val) 
        # split the value 
        tokens = val.split() 
        # Converts each token into lowercase 
        for i in range(len(tokens)): 
            tokens[i] = tokens[i].lower() 
        comment_words += " ".join(tokens)+" "  
        wordcloud = WordCloud(width = 580, height = 300, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(comment_words) 
    return wordcloud.to_image()

# USGS & ScienceBase Headers and Footers
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>      
        {%css%}
	<link rel="icon" type="image/png" href="../assets/favicons/favicon-16x16.png" sizes="16x16">	
	<link rel="icon" type="image/png" href="../assets/favicons/favicon-32x32.png" sizes="32x32">
	<link href="https://fonts.googleapis.com/css?family=Abel|Asap|Barlow+Condensed|Dosis&display=swap" rel="stylesheet">	
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
	
	<!-- START USGS Google Tag Manager -->
	<script></script>
	<!-- END USGS Google Tag Manager -->	
    </head>
    <body>
	
	<!-- opening div for body -->
	<div class="tmp-container">
	  <div class="row">
		<div class="col-12"> 
		  <!-- BEGIN USGS Applications Header Template -->
		  <header id="navbar" class="header-nav"  role="banner">
			<div class="tmp-container"> 
			  <!-- primary navigation bar --> 
			  <!-- search bar-->
			  <div class="header-search"> <a class="logo-header" href="https://www.usgs.gov/" title="Home"> <img src="../assets/images/logo.png" alt="Home" class="img" border="0" /> </a> </div>
			  <!-- end search bar--> 
			</div>
			<!-- end header-container--> 
		  </header>
		  <!-- END USGS Applications Header Template --> 
		</div>
	  </div>

	  <!-- BEGIN SDC_App Header and Navigation -->
	 <!-- BEGIN Navigation Template -->	
 	<div class="row">
	<div class="col-12">
		<div class="nav-background clearIt">	
		<nav class="navbar navbar-light">
		<a class="sb navbar-brand" href="#"><img src="../assets/images/powered_by_sb.png" alt="Powered by SDC_App" /> Science Data Center</a>
		</nav>	
		</div>	
	</div>
	</div>
<!-- END Navigation Template -->
	  <!-- END SDC_App Header and Navigation -->

	  <div id="maincontent headquarters"> <!-- opening div for USGS VisId main content --> 
		<!-- BEGIN SDC_App Image and Header Content -->
		<div class="row clearIt">
		  <div class="col-md-12 top-section">
			<h1>Science Data Catalog Summary Dashboard</h1>
			<p>Map and view dataset counts by Science Data Center and/or keyword.<br>
			<a href="#">Learn more about how these metrics are calculated. </a></p>
			 <p>Questions? Contact us at: <a href="mailto:sashaqanderson@gmail.com">sashaqanderson@gmail.com</a></p>
		  </div>
		</div>
		<!-- END SDC_App Image and Header Content -->
		
			{%app_entry%}  
            {%config%}
            {%scripts%}
            {%renderer%}     
		
		<!-- End Page Content and Image Template -->
		<div class="sb-footer">
		  <div class="row">
			<div class="col-md-4 col-sm-4 col-xs-4 align-left">Contact Us: <a href="mailto:sashaqanderson@gmail.com">sashaqanderson@gmail.com</a> <br />
			  Updates: <a href="#">Sign Up</a> <br />
			  <img src="../assets/images/kisspng-quotation-marks.jpg" alt="starting quotation mark" height="15px;" /><a href="#">Cite SDC</a> </div>
			<div class="col-md-4 col-sm-4 col-xs-4 ">
			  <center>
				<br />
				<a href="#">Home</a> &nbsp;|&nbsp; <a href="#">Terms of Use</a> &nbsp;|&nbsp; <a href="#">About</a> &nbsp;|&nbsp; <a href="#">Report Problem</a>
			  </center>
			</div>
			<div class="col-md-4 col-sm-4 col-xs-4 updates">Version: 0.0.1 <br />
			  Last Updated: Tuesday, August 17, 2019 </div>
		  </div>
		</div>
	  </div><!-- closing div for USGS VisId main content -->  

	  <!-- BEGIN USGS Footer Template -->
	  <footer class="footer">
		<div class="tmp-container"> 
		  <!-- .footer-wrap --> 
		  <!-- .footer-doi -->
		  <div class="footer-doi"> 
			<!-- footer nav links -->
			<ul class="menu nav">
			  <li class="first leaf menu-links menu-level-1"><a href="https://www.doi.gov/privacy">DOI Privacy Policy</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.usgs.gov/laws/policies_notices.html">Legal</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www2.usgs.gov/laws/accessibility.html">Accessibility</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.usgs.gov/sitemap.html">Site Map</a></li>
			  <li class="last leaf menu-links menu-level-1"><a href="https://answers.usgs.gov/">Contact USGS</a></li>
			</ul>
			<!--/ footer nav links --> 
		  </div>
		  <!-- /.footer-doi -->

		  <hr>

		  <!-- .footer-utl-links -->
		  <div class="footer-doi">
			<ul class="menu nav">
			  <li class="first leaf menu-links menu-level-1"><a href="https://www.doi.gov/">U.S. Department of the Interior</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.doioig.gov/">DOI Inspector General</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.whitehouse.gov/">White House</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.whitehouse.gov/omb/management/egov/">E-gov</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.doi.gov/pmb/eeo/no-fear-act">No Fear Act</a></li>
			  <li class="last leaf menu-links menu-level-1"><a href="https://www2.usgs.gov/foia">FOIA</a></li>
			</ul>
		  </div>
		  <!-- /.footer-utl-links --> 
		  <!-- .footer-social-links -->
		  <div class="footer-social-links">
			<ul class="social">
			  <li class="follow">Follow</li>
			  <li class="twitter"> <a href="https://twitter.com/usgs" target="_blank"> <i class="fa fa-twitter-square"><span class="only">Twitter</span></i> </a> </li>
			  <li class="facebook"> <a href="https://facebook.com/usgeologicalsurvey" target="_blank"> <i class="fa fa-facebook-square"><span class="only">Facebook</span></i> </a> </li>
			  <li class="googleplus"> <a href="https://plus.google.com/112624925658443863798/posts" target="_blank"> <i class="fa fa-google-plus-square"><span class="only">Google+</span></i> </a> </li>
			  <li class="github"> <a href="https://github.com/usgs" target="_blank"> <i class="fa fa-github"><span class="only">GitHub</span></i> </a> </li>
			  <li class="flickr"> <a href="https://flickr.com/usgeologicalsurvey" target="_blank"> <i class="fa fa-flickr"><span class="only">Flickr</span></i> </a> </li>
			  <li class="youtube"> <a href="https://youtube.com/usgs" target="_blank"> <i class="fa fa-youtube-play"><span class="only">YouTube</span></i> </a> </li>
			  <li class="instagram"> <a href="https://instagram.com/usgs" target="_blank"> <i class="fa fa-instagram"><span class="only">Instagram</span></i> </a> </li>
			</ul>
		  </div>
		  <!-- /.footer-social-links --> 
		</div>
		<!-- /.footer-wrap --> 
	  </footer>
	</div>
	<!-- END USGS Footer Template- -->	
	
	<!-- START USGS Google Tag Manager (noscript) -->
	<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=" 
	height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
	<!-- END USGS Google Tag Manager (noscript) -->
    </body>
</html>
"""
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
    export_format="csv",
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=590,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=35
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-115,
            lat=40
        ),
        zoom=1.6,
        #Use these when updating the zoom level w/ datatable
        uirevision=True,
        autosize=True,
    )
)

app.layout = html.Div(
    [
        # START Layout for Data by
        html.Div(
            [
                dbc.Col(html.Div(html.Div(id='live-update-text'), className="explore-sb-row-h2",), lg=12),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id='map-graph',
                                  style={'margin-top': '10'})
                    ],
                            className="explore-sb-box header-h3",
                        ),
                    ],
                    className="col-lg-6 col-md-6 col-sm-12",
                ),
                html.Div(
                    [
                    #     html.Div(
                    # className="explore-sb-box header-h3",
                    #     ),
                    html.Div(
                        [html.Div('Select an organization of interest:'),
                                dcc.Dropdown(
                                    id='sci_topic',
                                    style={
                                        'height': '2px', 
                                        # 'width': '100px', 
                                        'font-size': "75%",
                                        'min-height': '1px',
                                        },
                                    options= [{'label': 'All Science Centers', 'value': 'all'}] + [{'label': str(item),'value': str(item)}
                                              for item in sorted_SC],
                                    value= 'all'),
                        html.P(),
                        html.Br(),
                        html.Div('Search by keyword'),
                        html.Div(dcc.Input(id='kw', type='text')),
                        html.Button('Submit', type='submit', id='button', n_clicks=0),
                        html.Div(id='output-container-button')
                        ],
                    className="explore-sb-box header-h3",
                             ),
                    html.Div(
                    dcc.Loading(id='loading-1',
                        children=[html.Div(html.Img(id='wc',
                                                style={'margin-top': '6'})),
                            ],
                        type='default'),

                    className="explore-sb-box header-h3",
                             ),   
                    ],
                    className="col-lg-6 col-md-6 col-sm-12",
                    ),
                ],
            className="row clearIt bg-light explore-sb-row",
        ),
        html.Div(
            [
                html.H4("Science Data Catalog Results"),
                html.A(
                    "Download Data Table (CSV)", id = 'download-button', 
                    download="data.csv",
                    href="",
                    target="_blank",
                    # className="btn btn-success btn-sm download-listing align-right",
                ),
                dcc.Loading(id='loading-2',
                        children=[html.Div(
                dash_table.DataTable(
                    id='datatable',
                    data=df_map.to_dict('records'),
                    columns=[
                    {"name": ["Science Center"], "id": "sci_center"},
                    {"name": ["Dataset Title"], "id": "title"},
                    {"name": ["Beginning Date (idinfo)"], "id": "beg_year"},
                    {"name": ["End Date (idinfo)"], "id": "end_year"},
                    ],
                    style_cell_conditional=[
                        {'if': {'column_id': 'beg_year'},
                          'width': '10%',
                          'textAlign': 'center'},
                        {'if': {'column_id': 'end_year'},
                          'width': '10%',
                          'textAlign': 'center'},
                        {'if': {'column_id': 'sci_center'},
                          'width': '20%'}
                    ],
                    style_header= {
                        'whiteSpace':'normal',
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'overflow': 'hidden',
                        # 'textOverflow': 'ellipsis',
                        'maxWidth': '60px',
                        'height': 'auto'
                    },
                    style_table={
                        'maxHeight': '600px',
                        'overflowY': 'scroll'
                    },
                        style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px'
                    },
                    sort_action="native",
                    sort_mode="multi",
                    # page_action="native",
                    # page_current= 0,
                    # page_size= 10,
                    # row_selectable="multi",
                    # selected_rows=[],
                    )
                )], type = "default"),
                # dcc.Graph(
                #     id="example-graph-1",
                #     figure={
                #         "data": [
                #             {
                #                 "x": [1, 2, 3],
                #                 "y": [4, 1, 2],
                #                 "type": "bar",
                #                 "name": "SF",
                #             },
                #             {
                #                 "x": [1, 2, 3],
                #                 "y": [2, 4, 5],
                #                 "type": "bar",
                #                 "name": u"Montréal",
                #             },
                #         ],
                #         "layout": {"title": "Statistics",},
                #     },
                # ),
                # dcc.Link(
                #     "Learn more about how these metrics are calculated.",
                #     href="#",
                #     className="learn-more-link align-left",
                # ),
            ]
        )
    ]
)

#______________________________________________________________________________

def filter_data(sci_center, click, state):
    df3 = df_map.copy()
    if sci_center == 'all' and (click == 0 or state == ''):
        df2 = df3.copy()
        return df2
    if sci_center == 'all' and click > 0 and state != '':
        df2 = df3.copy()
        df_temp = df2[df2['all_kw'].notna()]
        df_kw = df_temp.loc[df_temp['all_kw'].str.contains(state)]
        return df_kw
    if sci_center != 'all' and click > 0 and state != '':
        df2 = df3.copy()
        df2 = df3[df3['sci_center']==sci_center]
        df_temp = df2[df2['all_kw'].notna()]
        df_kw = df_temp.loc[df_temp['all_kw'].str.contains(state)]
        return df_kw
    if sci_center != 'all' and (click == 0 or state == ''):
        df2 = df3.copy()
        df_sc = df2.loc[df2['sci_center']==sci_center]
        return df_sc

@app.callback(
    Output('live-update-text', 'children'),
    [Input('sci_topic', 'value'),
     Input('button', 'n_clicks')],
    [State('kw', 'value')])
def set_display_livedata(sci_topic, click, state):
    #connect to database and obtain blood pressure where id=value
    df = df_map.copy()
    if sci_topic == 'all' and (click == 0 or state == ''):
        df2 = df.copy()
        row_ct = len(df2) 
        return f'Total Dataset Count: {row_ct}'
    if sci_topic == 'all' and click > 0 and state != '':
        df2 = df.copy()
        df_temp = df[df['all_kw'].notna()]
        df_kw = df_temp.loc[df_temp['all_kw'].str.contains(state)]
        row_ct = len(df_kw) 
        return f'All results for {state}: {row_ct}'  
    if sci_topic != 'all' and click > 0 and state != '':
        df2 = df.copy()
        df2 = df[df['sci_center']==sci_topic]
        df_temp = df2[df2['all_kw'].notna()]
        df_kw = df_temp.loc[df_temp['all_kw'].str.contains(state)]
        row_ct = len(df_kw) 
        return f'{sci_topic} results for {state}: {row_ct}'  
    if sci_topic != 'all' and (click == 0 or state == ''):
        df2 = df.copy()
        df2 = df[df['sci_center']==sci_topic]
        row_ct = len(df2) 
        return f'{sci_topic} Results: {row_ct}'

@app.callback(
    Output('datatable', 'data'),
    [Input('sci_topic', 'value'),
     Input('button', 'n_clicks')],
    [State('kw', 'value')])
def table_selection(sci_center, click, state):
    if (len(sci_center) == 0) and click == 0:
        return no_update
    df3 = filter_data(sci_center, click, state)
    return df3.to_dict("records")

def update_selected_row_indices(sci_center, click, state):
    if (len(sci_center) == 0) and click == 0:
        return no_update
    df4 = filter_data(sci_center, click, state)
    return df4.to_dict("records")


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
                        for i in aux['title'].str[:90]],
                    "mode": "markers+text",
                    "name": list(aux['sci_center']),
                    "marker": {
                        "size": 8,
                        "opacity": 0.7,
                        # "color": list(aux['sci_center']),
                        },
            }],
            "layout": layout_map
        }
    
@app.callback(
    Output('wc', 'src'),
    [Input('datatable', 'data'),
     Input('sci_topic', 'value'),
     Input('button', 'n_clicks')],
    [State('kw', 'value')])
def make_wordcloud(data, sci_center, click, state):
    if data:
        if sci_center == 'all' and (click == 0 or state == ''):
            
            return r'/assets/images/all_image.png'
        else:
            img = BytesIO()
            plot_wordcloud(data).save(img, format='PNG')
            return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(Output('download-button', 'href'), 
              [Input('datatable', 'data')])
def update_download_link(data):
    dff = pd.DataFrame(data)
    # df5 = 
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string


if __name__ == "__main__":
    app.run_server(debug=True, port = 8080)
