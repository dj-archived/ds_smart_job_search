################################################################################
# Import packages
################################################################################
import dash
import dash_table
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash_table_experiments import DataTable

import plotly.plotly as py
import plotly.graph_objs as go

import flask
from flask import Flask, send_from_directory

# Other
import io
import os
import urllib
import pandas as pd

# For web scraping
# import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import re

from dotenv import load_dotenv
from exceptions import ImproperlyConfigured

import chardet

import subprocess

pd.set_option("display.max_columns", None)
###############################################################################
def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc


################################################################################
# Call scrape function from scrape_de.py
#from scrape_de import scrape_indeed_de
################################################################################
# Website information
url_de = "http://de.indeed.com/jobs?q=data+scientist+&l={}&start={}"
################################################################################
# Variables
My_City = set(["Cologne", "Berlin", "Munich", "Dusseldorf"])
max_results_my_city = 5
# Number of pages
page = 2

# Call function
#scrape_indeed_de(url_de, My_City,max_results_my_city,page)

################################################################################
# Setting
################################################################################
if "DYNO" in os.environ:
    # the app is on Heroku
    debug = False
# google analytics with the tracking ID for this app
# external_js.append('https://codepen.io/jackdbd/pen/rYmdLN.js')
else:
    debug = True
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)

app_name = "Smart Job Search"
server = Flask(app_name, static_folder='static')
app = Dash(name=app_name, server=server, csrf_protect=False)
app.title = 'Smart Job Search'
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally=True

external_js = []
external_css = [
    # dash stylesheet
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://fonts.googleapis.com/css?family=Lobster|Raleway",
    "//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
]

theme = {"font-family": "Lobster", "background-color": "#e0e0e0"}
################################################################################
# Read Global AI data
################################################################################
# Table 1 and 2
df1_encoding = find_encoding("./data/Global-Artificial-Intelligence-Database-Asgard-2018.txt")
df_health_encoding = find_encoding("./data/df_health.txt")


df1 = pd.read_csv("./data/Global-Artificial-Intelligence-Database-Asgard-2018.csv",encoding="ISO-8859-1")
df1.insert(0, 'Index', range(1, len(df1) + 1))

# Table 2
df_health = pd.read_csv("./data/df_health.csv",encoding="ISO-8859-1")
df_health.insert(0, 'Index', range(1, len(df_health) + 1))

# Dictionary of two tables
dataframes = {'Global AI Companies': df1,'Global Health AI Companies': df_health}
print(dataframes.keys())

def get_data_object(user_selection):
    """
    For user selections, return the relevant in-memory data frame.
    """
    #return dataframes[user_selection]
    return dataframes.get(user_selection)
################################################################################
# Table 3 and 4
de_encoding = find_encoding("./data/de_indeed.txt")

df_indeed_de = pd.read_csv("./data/de_indeed.txt",sep="\t",encoding=de_encoding)
df_indeed_de.insert(0, 'Index', range(1, len(df_indeed_de) + 1))
print(df_indeed_de.head(2))

dataframes_indeed = {'Germany': df_indeed_de

}

print(dataframes_indeed.keys())

def get_data_object2(user_selection2):
    """
    For user selections, return the relevant in-memory data frame.
    """
    #return dataframes[user_selection]
    return dataframes_indeed.get(user_selection2)
################################################################################
# APP Functions and Layout
################################################################################
def create_header():
    header_style = {"background-color": theme["background-color"], "padding": "1.5rem"}
    header = html.Header(html.H1(children=app_name, style=header_style))
    return header
################################################################################
def create_content():
    content = html.Div(id='ai',
        children=[
            html.H2("Global AI companies"),
            html.Div(
                children=[
                    dcc.Markdown(
                        """
                        Top Countries in the Race for Artificial Intelligence

                        ![AI](https://asgard.vc/wp-content/uploads/2018/05/Global-Artificial-Intelligence-Landscape-Industry-Map-International-by-Asgard-Capital-2018-and-Roland-Berger-1024x678.jpg)


                        > The greater Silicon Valley area is the world’s largest AI hub, followed by London, Tel Aviv, New York, and then Beijing.
                        >
                        > Boston, Tokyo, Shanghai, Los Angeles, and Paris are still in the Top Ten 10 for global AI cities.
                        >
                        > Berlin, Toronto, Shenzhen, and Seoul follow closely.
                        >
                        > Applied AI Solutions Aren’t Deep-Tech Enough
                        """.format(
                            number="thousand"
                        ).replace(
                            "  ", ""
                        )
                    )
                ],
                className="row",
                style={"margin-bottom": 20},
            ),
            html.Hr(),
            html.H2("List of global AI companies"),
            html.Div(
                children=[
                    dcc.Dropdown(
                    id='field-dropdown',
                    options=[{'label': df, 'value': df} for df in dataframes],
                    value="Global AI Companies"),
                    DataTable(
                        id='table',
                    # rows
                        rows=[{}],
                        #columns=df_health.columns,
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        selected_row_indices=[],
                        max_rows_in_viewport=10,
                        resizable =True,
                        enable_drag_and_drop=True,
                        header_row_height=50,
                        column_widths=200,
                        row_scroll_timeout=1,
                        row_update= True,
                        editable =True)]),
            html.H2(),
            html.A(
                'Download Data',
                id='download-link',
                download="global_ai_companies.csv",
                href="",
                target="_blank"
            ),
                    ])
    return content
def create_content2():
    content = html.Div(
        children=[
            html.Hr(),
            html.H2("Data Scientist Positions in Germany"),
            html.Div(
                children=[
                    html.Button("Search Indeed", id='button',n_clicks_timestamp=0),
                    html.Div(id='button-container')
                ]),
            html.Div(
                children=[
                    dcc.Dropdown(
                    id='field-dropdown2',
                    options=[{'label': df, 'value': df} for df in dataframes_indeed],
                    value="Germany"),
                    DataTable(
                        id='table_indeed',
                        rows=[{}],
                        #columns=df_health.columns,
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        selected_row_indices=[],
                        max_rows_in_viewport=10,
                        resizable =True,
                        enable_drag_and_drop=True,
                        header_row_height=50,
                        column_widths=200,
                        row_scroll_timeout=1,
                        row_update= True,
                        editable =True)]),
            html.H2(),
            html.A(
                'Download Data Scientist Jobs',
                id='download-link2',
                download="data_scientist_position.txt",
                href="",
                target="_blank"
            ),
            html.Hr(),

    ])
    return content
################################################################################
# Footer
def create_footer():
    footer_style = {"background-color": theme["background-color"], "padding": "0.5rem"}
    p0 = html.P(
        children=[
            html.Span("Built with "),
            html.A(
                "Plotly Dash", href="https://github.com/plotly/dash", target="_blank"
            ),
            html.H2(),
        ]
    )
    p1 = html.P(
        children=[
            html.H2(),
            html.Span("Global AI Company Data from "),
            html.A(
                "https://asgard.vc/global-ai/",
                href="https://some-website.com/",
                target="_blank",
            ),
            html.H2(),
            html.Span("Job data from "),
            html.A(
                "https://de.indeed.com/",
                href="https://de.indeed.com/",
                target="_blank",
            ),
        ]
    )

    div = html.Div([p0, p1])
    footer = html.Footer(children=div, style=footer_style)
    return footer
################################################################################
# Layout
def serve_layout():
    layout = html.Div(
        children=[create_header(), create_content(), create_content2(), create_footer()],
        className="container",
        style={"font-family": theme["font-family"]},
    )
    return layout

################################################################################
# Callbacks
################################################################################
app.layout = serve_layout
for js in external_js:
    app.scripts.append_script({"external_url": js})
for css in external_css:
    app.css.append_css({"external_url": css})
################################################################################
################################################################################
# Display table
@app.callback(Output('table', 'rows'), [Input('field-dropdown', 'value')])
def update_table(user_selection):
    """
    For user selections, return the relevant table
    """
    df_select = get_data_object(user_selection)
    print(type(df_select))
    if df_select is not None:
        df = df_select.to_dict('records')
        return df
    else:
        print('Data is not selected yet')
################################################################################
# Download table link
@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('table', 'rows')])
def update_download_link(rows):
    dff = pd.DataFrame(rows)
    txt_string = dff.to_csv(index=False,
        header = True,
        columns=["Index","Country","State","City","Name","Category","Description","Website"],
        encoding="ISO-8859-1"
        )
    txt_string = "data:text/csv;charset=ISO-8859-1," + urllib.parse.quote(txt_string)
    return txt_string
################################################################################
################################################################################
# Display ds table
@app.callback(
    dash.dependencies.Output('table_indeed', 'rows'), [dash.dependencies.Input('field-dropdown2', 'value')])
def update_table2(user_selection2):
    """
    For user selections, return the relevant table
    """
    df_select_indeed = get_data_object2(user_selection2)
    print(type(df_select_indeed))
    if df_select_indeed is not None:
        df_indeed_result = df_select_indeed.to_dict('records')
        return df_indeed_result
    else:
        print('Indeed data is not selected yet')

# Download table link

@app.callback(
    dash.dependencies.Output('download-link2', 'href'),
    [dash.dependencies.Input('table_indeed', 'rows')])
def update_download_link(rows):
    dff2 = pd.DataFrame(rows)
    txt_string2 = dff2.to_csv(index=False,
        header = True,
        sep="\t",
        )
    # ignore encoding here
    txt_string2 = "data:text/csv;charset=de_encoding," + urllib.parse.quote(txt_string2)
    return txt_string2
################################################################################
# Click button and scrape data on indeed
@app.callback(
    dash.dependencies.Output('button-container', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def displayClick(n_clicks):
    if n_clicks is None:
        msg ='Using pre-downloaded data from Indeed'
    else:
        print('search indeed.de')
        subprocess.call(" python scrape_de.py 1", shell=True)
        print('finished searching')
        #os.system('scrape_de.py 1')
        msg = 'Download the latest data from Indeed'

    return html.Div(msg)
############################################################################### # facicon
@app.server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(server.root_path, 'static'),
    'favicon.ico', mimetype='image/vnd.microsoft.icon')



################################################################################
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run_server(port=port, threaded=True, debug=True) #debug=debug,
