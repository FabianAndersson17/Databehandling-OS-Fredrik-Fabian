import pandas as pd
from dash import dcc, html
import dash
from dash.dependencies import Output, Input
import plotly_express as px
import dash_bootstrap_components as dbc
from FredrikH import testfunc
from Fabian_A import data_locator

symbol_dict = dict(TENNIS="Tennis", FOTBALL="Football", TAEKWONDO="Taekwondo", SPEEDSKATING="Speed Skating")

stock_options_dropdown = [{"label": name, "value": symbol}
                          for name,symbol in symbol_dict.items()]

stylesheets = [dbc.themes.SOLAR]


app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

app.layout = dbc.Container([

    dbc.Card([
        dbc.CardBody(html.H1("Russia / Sovjet dashboard",
                             className="text-primary m-3"))
    ], className="mt-3"),
    

    dbc.Row([
        dbc.Col(html.P("Choose a sport"), className="mt-1",
                lg="4", xl={"size": 2, "offset": 2}),
        dbc.Col(
            dcc.Dropdown(id='sport-picker-dropdown', className='',
                         options=stock_options_dropdown,
                         value='AAPL'
                         ),
            lg="4", xl="3")]),
        dcc.Graph(id = 'graph-picker')
        
            
            ])

@app.callback(
    Output("graph-picker", "figure"),
    Input("sport-picker-dropdown", "value"))

def update_graph(sport):

    fig = data_locator(sport)

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)