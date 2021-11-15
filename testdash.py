import pandas as pd
from dash import dcc, html
import dash
from dash.dependencies import Output, Input
import plotly_express as px
import dash_bootstrap_components as dbc



stylesheets = [dbc.themes.MATERIA]


app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

app.layout = dbc.Container([

    dbc.Card([
        dbc.CardBody(html.H1("Sovjet Dashboard",
                             className="text-primary m-3"))
    ], className="mt-3")])



if __name__ == "__main__":
    app.run_server(debug=True)