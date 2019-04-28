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
from flask import Flask
import os
import pandas as pd



pd.set_option("display.max_columns", None)

from dotenv import load_dotenv
from exceptions import ImproperlyConfigured
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

app_name = "AI Job Search"
server = Flask(app_name)
app = Dash(name=app_name, server=server, csrf_protect=False)

#app.config.suppress_callback_exceptions = True

#app.scripts.config.serve_locally=True

external_js = []

external_css = [
    # dash stylesheet
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://fonts.googleapis.com/css?family=Lobster|Raleway",
    "//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
]

theme = {"font-family": "Lobster", "background-color": "#e0e0e0"}
################################################################################
# Read data
# Table 1
df1 = pd.read_csv("./data/Global-Artificial-Intelligence-Database-Asgard-2018.csv",encoding="ISO-8859-1")
df1.insert(0, 'Index', range(1, len(df1) + 1))
#df1['index'] = range(1, len(df1) + 1)


# Table 2
df_health = pd.read_csv("./data/df_health.csv", encoding="ISO-8859-1")
df_health.insert(0, 'Index', range(1, len(df_health) + 1))
#####################################################################
dataframes = {'Global AI Companies': df1,'Global Health AI Companies': df_health}


def get_data_object(user_selection):
    """
    For user selections, return the relevant in-memory data frame.
    """
    return dataframes[user_selection]

#####################################################################
# df_health.to_csv('./data/df_health.csv')
################################################################################
def create_header():
    header_style = {"background-color": theme["background-color"], "padding": "1.5rem"}
    header = html.Header(html.H1(children=app_name, style=header_style))
    return header


#########################
def create_content():
    content = html.Div(
        children=[
            html.H2("Global AI companies"),
            html.Hr(),
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
                    options=[{'label': df, 'value': df} for df in dataframes]),
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

                    ])
    return content


#########################
def create_footer():
    footer_style = {"background-color": theme["background-color"], "padding": "0.5rem"}
    p0 = html.P(
        children=[
            html.Span("Built with "),
            html.A(
                "Plotly Dash", href="https://github.com/plotly/dash", target="_blank"
            ),
        ]
    )
    p1 = html.P(
        children=[
            html.Span("Global AI Company Data from "),
            html.A(
                "https://asgard.vc/global-ai/",
                href="https://some-website.com/",
                target="_blank",
            ),
            html.Span("Job data from"),
            html.A(
                "https://de.indeed.com/",
                href="https://de.indeed.com/",
                target="_blank",
            ),
        ]
    )

    div = html.Div([p0, p1])  # , a_fa
    footer = html.Footer(children=div, style=footer_style)
    return footer


#########################
def serve_layout():
    layout = html.Div(
        children=[create_header(), create_content(), create_footer()],
        className="container",
        style={"font-family": theme["font-family"]},
    )
    return layout


# TODO: callbacks
################################################################################
app.layout = serve_layout
for js in external_js:
    app.scripts.append_script({"external_url": js})
for css in external_css:
    app.css.append_css({"external_url": css})

@app.callback(Output('table', 'rows'), [Input('field-dropdown', 'value')])
def update_table(user_selection):
    """
    For user selections, return the relevant table
    """
    df = get_data_object(user_selection)
    return df.to_dict('records')
    ß
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run_server(port=port, threaded=True, debug=True) #debug=debug,
