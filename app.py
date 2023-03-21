import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
from dash import dcc, html, callback, Output
import pathlib
import os

# set the app layout--------------------------------------------------------------------------
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}],
                suppress_callback_exceptions=True,
                use_pages=True)
server = app.server
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()

    ],
    horizontal=True,
    vertical=False,
    pills=True,
    className="bg-light",
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Monthly Hospital Performance Dashboard",
                         style={'fontSize': 35, 'textAlign': 'center'}))
    ]),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=1, xl=1, xxl=1),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=11, xl=10, xxl=11)
        ]
    )
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)