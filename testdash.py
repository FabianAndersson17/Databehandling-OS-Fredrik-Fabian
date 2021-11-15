import pandas as pd
from dash import dcc, html
import dash
from dash.dependencies import Output, Input
import plotly_express as px
import dash_bootstrap_components as dbc

symbol_dict = dict(TENN="Tennis", FOTB="Football", TAEK="Taekwando", SPEE="Speedskating")

stock_options_dropdown = [{"label": name, "value": symbol}
                          for symbol, name in symbol_dict.items()]

stylesheets = [dbc.themes.SOLAR]


app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])

app.layout = dbc.Container([

    dbc.Card([
        dbc.CardBody(html.H1("Russia / Sovjet dashboard",
                             className="text-primary m-3"))
    ], className="mt-3"),

    dbc.Row([
        dbc.Col(html.P("Choose a stock"), className="mt-1",
                lg="4", xl={"size": 2, "offset": 2}),
        dbc.Col(
            dcc.Dropdown(id='stock-picker-dropdown', className='',
                         options=stock_options_dropdown,
                         value='AAPL'
                         ),
            lg="4", xl="3")])])

@app.callback(
    Output("stock-graph", "figure"),
    Input("stock-picker-dropdown", "value"))
    
def update_graph(json_df, stock, ohlc):

    dff = pd.read_json(json_df)
    fig = px.line(dff, x=dff.index, y=ohlc, title=symbol_dict[stock])

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)