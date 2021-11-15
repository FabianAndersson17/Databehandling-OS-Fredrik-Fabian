import pandas as pd
from dash import dcc, html
import dash
from dash.dependencies import Output, Input
import plotly_express as px
import dash_bootstrap_components as dbc
from Fabian_A import data_locator


symbol_dict = dict(TENNIS="Tennis", FOTBALL="Football", TAEKWONDO="Taekwondo", SPEEDSKATING="Speed Skating")

dashboard_name_dict = dict(Sovjet_Russia ="Sovjet / Russia Dashboard", Choosen_countries = "Choosen countries Dashboard")

plot_name_dict = dict(Plot1 ="Plot 1", Plot2 = "Plot2")

plot_options_dropdown = [{"label": name, "value": symbol}
                          for name,symbol in plot_name_dict.items()]

stock_options_dropdown = [{"label": name, "value": symbol}
                          for name,symbol in symbol_dict.items()]
dashboard_names = [{"label": name, "value": symbol}
                          for name,symbol in dashboard_name_dict.items()]
plot_options_dropdown = [{"label": name, "value": symbol}
                          for name,symbol in symbol_dict.items()]

stylesheets = [dbc.themes.SOLAR]


app = dash.Dash(__name__, external_stylesheets=stylesheets,
                meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")])


@app.callback(
    Output("graph-picker", "figure"),
    Output("graph-picker2", "figure"),
    Input("sport-picker-dropdown", "value"))

def update_graph(sport):

    fig1, fig2 = data_locator(sport)

    return fig1, fig2


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Soviet", className="display-4"),
        html.Hr(),
        html.P(
            "Russia / Soviet through the Olympics", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Soviet / Russia", href="/page-1", active="exact"),
                dbc.NavLink("Choosen sports", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Img(src='assets/Flag_of_the_Soviet_Union.png')
    elif pathname == "/page-1":
        return dbc.Container([

    dbc.Card([
        dbc.CardBody(html.H1("Choosen sports dashboard (Taekwondo, Tennis, Football & Speedskating",
                             className="text-primary m-3")
    , className="mt-3"),
      ]),
    

    dbc.Row([
        dbc.Col(html.P("Choose a sport"), className="mt-1",
                lg="4", xl={"size": 2, "offset": 2}),
        dbc.Col(
            dcc.Dropdown(id='sport-picker-dropdown', className='',
                         options=stock_options_dropdown,
                         value='AAPL'
                         ),
            lg="4", xl="3")]),
        dcc.Graph(id = 'graph-picker'),
        dcc.Graph(id = 'graph-picker2')
        
            
            ])
    
    elif pathname == "/page-2":
        return  dbc.Container([

    dbc.Card([
        dbc.CardBody(html.H1("Russia / Sovjet Dashboard",
                             className="text-primary m-3")
    , className="mt-3"),
      ]),
    

    dbc.Row([
        dbc.Col(html.P("Choose a plot"), className="mt-1",
                lg="4", xl={"size": 2, "offset": 2}),
        dbc.Col(
            dcc.Dropdown(id='sport-picker-dropdown', className='',
                         options=plot_options_dropdown,
                         value='AAPL'
                         ),
            lg="4", xl="3")]),
        dcc.Graph(id = 'graph-picker'),
        dcc.Graph(id = 'graph-picker2')
        
            
            ])
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == "__main__":
    app.run_server(debug=True)