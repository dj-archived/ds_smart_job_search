import dash
import dash_table
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


import plotly.plotly as py
import plotly.graph_objs as go
from flask import Flask
import os
import pandas as pd

from dotenv import load_dotenv
from exceptions import ImproperlyConfigured

pd.set_option("display.max_columns", None)
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
# df =pd.read_csv('./data/Global-Artificial-Intelligence-Database-Asgard-2018.csv',encoding = "ISO-8859-1")

# df = df.drop('Description', 1)
# add index
# df[' index'] = range(1, len(df) + 1)

# Filter healthcare
# df_health = df[df['Category'].str.contains("Health")]
# df_health = df.loc[df.Category.str.contains('Health', na=False)]
df_health = pd.read_csv("./data/df_health.csv", encoding="ISO-8859-1")
#####################################################################
df1 = pd.read_csv("./data/de/Indeed_Germany.csv")
df1.head(2)
df1["Number"] = range(1, len(df1) + 1)

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
            html.H2("Health AI companies"),
            html.Div(
                children=[
                    dash_table.DataTable(
                        id="datatable-interactivity2",
                        columns=[
                            {"name": i, "id": i, "deletable": True}
                            for i in df_health.columns
                        ],
                        data=df_health.to_dict("rows"),
                        editable=True,
                        filtering=True,
                        sorting=True,
                        sorting_type="multi",
                        row_selectable="multi",
                        row_deletable=True,
                        selected_rows=[],
                        style_cell={"textAlign": "left"},
                        style_as_list_view=False,
                        style_cell_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "rgb(248, 248, 248)",
                            }
                        ],
                        style_header={"backgroundColor": "white", "fontWeight": "bold"},
                        pagination_mode="fe",
                        pagination_settings={
                            "displayed_pages": 1,
                            "current_page": 0,
                            "page_size": 20,
                        },
                        navigation="page",
                    )
                ]
            ),
            # 2. 2nd row: table
            html.H2("Data Scientist Positions in Germany"),
            html.Div(
                children=[
                    dash_table.DataTable(
                        id="datatable-interactivity3",
                        columns=[
                            {"name": i, "id": i, "deletable": True} for i in df1.columns
                        ],
                        data=df1.to_dict("rows"),
                        editable=True,
                        filtering=True,
                        sorting=True,
                        sorting_type="multi",
                        row_selectable="multi",
                        row_deletable=True,
                        selected_rows=[],
                        style_cell={"textAlign": "left"},
                        style_as_list_view=False,
                        style_cell_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "rgb(248, 248, 248)",
                            }
                        ],
                        style_header={"backgroundColor": "white", "fontWeight": "bold"},
                        pagination_mode="fe",
                        pagination_settings={
                            "displayed_pages": 1,
                            "current_page": 0,
                            "page_size": 20,
                        },
                        navigation="page",
                    )
                ]
            ),
        ],
        id="content",
        style={"width": "100%", "height": "100%"},
    )
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
            html.Span("Data from "),
            html.A(
                "https://asgard.vc/global-ai/",
                href="https://some-website.com/",
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run_server(debug=debug, port=port, threaded=True)
