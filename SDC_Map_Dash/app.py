import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import dash_bootstrap_components as dbc
import dash_table
import pandas as pd

# sample data
df = pd.read_csv("solar.csv")

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

mapbox_access_token = 'pk.eyJ1Ijoic2RjLWRhc2giLCJhIjoiY2tmMzZqb21vMDA2ejJ1cGdjeDg5OGRiOCJ9.alrKKaVlRO4DIJmMWYY1WQ'

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
			<h1>Map Query Dashboard</h1>
			<p>Select and map datasets by date and keyword(s). Note that US and global data are provided in separate tabs below.<br>
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

row = html.Div(
    [
        # START Layout for Data by
        html.Div(
            [
                dbc.Col(html.Div("Insert a date selector here", className="explore-sb-row-h2",), lg=12),
                html.Div(
                    [
                        html.Div(
                            [html.H3("Place Map Here")],
                            className="explore-sb-box header-h3",
                        ),
                    ],
                    className="col-lg-8 col-md-8 col-sm-12",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H3("Keyword Selector Here"),],
                            className="explore-sb-box header-h3",
                        ),
                    ],
                    className="col-lg-4 col-md-4 col-sm-12",
                ),
            ],
            className="row clearIt bg-light explore-sb-row",
        ),
        # END Layout for Data by
        # START Layout for Select an Organization of Interest
        # html.Div(
        #     [
        #         dbc.Col(
        #             html.Div(
        #                 "Select an Organization of Interest",
        #                 className="explore-sb-row-h2",
        #             ),
        #             lg=12,
        #         ),
        #         html.Div(
        #             [
        #                 html.Div(
        #                     [
        #                         html.H3("Total Data Published"),
        #                         html.P("3043", className="textHeader"),
        #                         dcc.Link(
        #                             "Browse These Data",
        #                             href="#",
        #                             className="browse-dr-link",
        #                         ),
        #                     ],
        #                     className="explore-sb-box header-h3",
        #                 ),
        #             ],
        #             className="col-lg-6 col-md-6 col-sm-12",
        #         ),
        #         html.Div(
        #             [
        #                 html.Div(
        #                     [
        #                         html.H3("Current Data In-Progress"),
        #                         html.P("177", className="textHeader"),
        #                     ],
        #                     className="explore-sb-box header-h3",
        #                 ),
        #             ],
        #             className="col-lg-6 col-md-6 col-sm-12",
        #         ),
        #     ],
        #     className="row clearIt bg-light explore-sb-row",
        # ),
        # # END Layout for Select an Organization of Interest
    ]
)

# START Layout for Select a Date Range
app.layout = html.Div(
    [
        row,
        # START Layout for Tabbed Content
        dbc.Row(
            [
                # dbc.Col(
                #     html.Div("Data and Statistics", className="explore-sb-row-h2",),
                #     width=12,
                # ),
                dcc.Tabs(
                    id="tabs-with-classes",
                    value="tab-1",
                    parent_className="custom-tabs",
                    className="custom-tabs-container",
                    children=[
                        dcc.Tab(
                            label="Mapped Data & Statitics",
                            value="tab-1",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="United States Data & Statistics",
                            value="tab-2",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="Global Data & Statistics",
                            value="tab-3",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                    ],
                ),
                html.Div(id="tabs-content-classes"),
            ],
            className="row clearIt bg-light explore-sb-row",
        ),
    ]
)


@app.callback(
    Output("tabs-content-classes", "children"), [Input("tabs-with-classes", "value")]
)
def render_content(tab):
    if tab == "tab-1":
        return html.Div(
            [
                html.P("Mapped Data", className="center-date-range-text"),
                html.H4("Science Centers"),
                dcc.Link(
                    "Browse These Data", href="#", className="browse-dr-link tab-link"
                ),
                html.H5("Full Details Listing", className="align-left"),
                html.Button(
                    "Download Data Table (CSV)",
                    className="btn btn-success btn-sm download-listing align-right",
                ),
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict("records"),
                ),
                dcc.Graph(
                    id="example-graph-2",
                    figure={
                        "data": [
                            {
                                "x": [1, 2, 3],
                                "y": [4, 1, 2],
                                "type": "bar",
                                "name": "SF",
                            },
                            {
                                "x": [1, 2, 3],
                                "y": [2, 4, 5],
                                "type": "bar",
                                "name": u"Montréal",
                            },
                        ],
                        "layout": {"title": "Basic non interactive",},
                    },
                ),
                dcc.Link(
                    "Learn more about how these metrics are calculated.",
                    href="#",
                    className="learn-more-link align-left",
                ),
            ]
        )
    elif tab == "tab-2":
        return html.Div(
            [
                html.P("United States Countrywide Data", className="center-date-range-text"),
                html.P("(Continental US included)"),
                html.H4("Science Centers"),
                
            ]
        )
    elif tab == "tab-3":
        return html.Div(
            [
                html.P("Worldwide Data", className="center-date-range-text"),
                html.H4("Science Centers"),
            ]
        )


# START Layout for Tabbed Content
# END Layout for Select a Date Range
if __name__ == "__main__":
    app.run_server(debug=True, port = 8080)
