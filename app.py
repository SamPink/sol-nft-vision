from distutils.log import debug
import re
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import os
import json
from flask import Flask

server = Flask(__name__)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)
app.title = "NFT Vision"

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
        # add a logo
        html.H2(
            html.Img(
                src="https://res.cloudinary.com/metaverse-holdings-limited/image/upload/v1656932068/photo_2022-07-04_11.29.59_wxg8if.jpg",
                style={"height": "50px", "width": "auto"},
            ),
            style={"text-align": "center"},
        ),
        html.Hr(),
        html.P("$SOL", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Docs", href="/docs", active="exact"),
                dbc.NavLink("Okay Bears", href="/listings/okay_bears", active="exact"),
                dbc.NavLink(
                    "Tripping Ape Tribe",
                    href="/listings/trippin_ape_tribe",
                    active="exact",
                ),
                dbc.NavLink("Primates", href="/listings/primates", active="exact"),
                dbc.NavLink("Just Ape", href="/listings/justape", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

""" with open("./data/collections.json") as f:
        collections = json.load(f)

#create dropdown for collections
dropdown_options = [{
    "label": collection['name'],
    "value": collection['slug']
} for collection in collections]

content = html.Div([html.Div(id="page-content", style=CONTENT_STYLE),dcc.Dropdown(
                id="collection-dropdown",
                options=dropdown_options,
                value=dropdown_options[0]['label'],
                style={"width": "18rem"},
            )]) """

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return index()
    elif pathname == "/listings/okay_bears":
        return listings("okay_bears")
    elif pathname == "/listings/trippin_ape_tribe":
        return listings("trippin_ape_tribe")
    elif pathname == "/listings/primates":
        return listings("primates")
    elif pathname == "/listings/justape":
        return listings("justape")
    # If the user tries to reach a different page, return a 404 message
    return html.P("404: Page not found")


def index():
    with open("./data/collections.json") as f:
        collections = json.load(f)

    df = pd.DataFrame()
    dropdown_options = []

    for collection in collections:
        try:
            # get rarity.csv from the data folder
            rarity = pd.read_csv(f"./data/{collection['slug']}/best_listings.csv")
            if rarity.empty:
                continue
            # sort by rarity rank
            rarity = rarity.sort_values(by="diff", ascending=False)

            best = rarity.head(1)[
                ["price", "rarity_rank", "extra.img", "name", "pred_SOL", "diff"]
            ]
            best["name"] = collection["name"]

            df = df.append(best)

            dropdown_options.append(
                {"label": collection["name"], "value": collection["slug"]}
            )
        except:
            print(f"{collection['slug']} is empty")

    return html.Div(
        [
            html.H1("Supported Collections"),
            html.Hr(),
            # dropdown to select collection
            html.Div(dbc.Row([card_listing(df.iloc[[i]]) for i in range(df.shape[0])])),
        ]
    )


""" #add a callback to the dropdown to go to the best listings page
@app.callback(Output("page-content", "children"), [Input("collection-dropdown", "value")])
def update_url(collection):
    return listings(collection)  """


def listings(collection=None):
    # get listings.csv from the data folder
    listings = pd.read_csv(f"./data/{collection}/best_listings.csv")

    return html.Div(
        [
            html.H1(f"{collection}"),
            html.Hr(),
            html.Div(dbc.Row([card_listing(listings.iloc[[i]]) for i in range(100)])),
        ]
    )


def card_listing(ape, listings_link=False):

    return dbc.Card(
        [
            dbc.CardImg(
                src=ape["extra.img"],
                top=True,
                style={"width": "100%", "height": "auto"},
            ),
            dbc.CardBody(
                [
                    html.H4(ape["name"].item()),
                    html.H4(f"Rarity Rank: {ape['rarity_rank'].item()}"),
                    html.P(f"Listing Price: {ape['price'].item()} SOL"),
                    html.P(f"Predicted Price: {ape['pred_SOL'].item()} SOL"),
                ]
            ),
        ],
        style={"width": "18rem"},
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
