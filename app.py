import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import os


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
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
        html.H2("SOL NFT Vision", className="display-4"),
        html.Hr(),
        html.P(
            "$SOL", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Best Listings", href="/listings", active="exact"),
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
        return index()
    elif pathname == "/listings":
        return listings('okay_bear')
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

def index():
    #read all of the folders in data
    folders = os.listdir("./data")
    
    #create a dropdown menu with all of the folders
    dropdown = dbc.DropdownMenu(
        children=[dbc.DropdownMenuItem(f"{folder}", href=f"/listings/{folder}") for folder in folders],
        label="Select a collection",
        className="mb-3",
    )
    return html.Div([dropdown, html.Hr()])

def listings(collection=None):
    #get listings.csv from the data folder
    listings = pd.read_csv(f"./data/{collection}/best_listings.csv")

    
    
    return html.Div(
        [html.H1(f"{collection}"), 
         html.Hr(), 
         html.Div(
                dbc.Row([card_listing(listings.iloc[[i]]) for i in range(100)])
        ),])

def card_listing(ape):

    return dbc.Card(
        [
            dbc.CardImg(
                    src=ape["extra.img"],
                    top=True,
                    style={"width": "100%", "height": "auto"},
                ),
                dbc.CardBody(
                    [
                        html.H4(f"Rarity Rank: {ape['rarity.moonrank.rank'].item()}"),
                        html.P(f"Listing Price: {ape['price'].item()} SOL"),
                        html.P(f"Predicted Price: {ape['pred_SOL'].item()} SOL"),
                    ]
                ),
        ],
        style={"width": "18rem"},
    )

if __name__ == "__main__":
    app.run_server(port=8887, debug=True)