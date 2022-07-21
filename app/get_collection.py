import os
import json 
import pandas as pd

import sales
import rarity
import listings
import best_listings as best

#dissable pandas warnings
pd.options.mode.chained_assignment = None

#read data/collections.json to a json object
with open("data/collections.json") as f:
    collections = json.load(f)

def get_data_for_collection(collection, update_listings=False):
    slug_name = collection["slug"]
    # make folder for slug in data if not exists
    if not os.path.exists(f"data/{slug_name}"):
        os.makedirs(f"data/{slug_name}")

    if not os.path.exists(f"data/{slug_name}/transactions.csv"):
        df_transactions = sales.get_sales(slug_name, max_sales=30000)

        df_transactions.to_csv(f"data/{slug_name}/transactions.csv")

    if not os.path.exists(f"data/{slug_name}/rarity.csv"):
        #if collection has a slug_moon_rank, use that
        if "slug_moon_rank" in collection:
            df_rarity = rarity.get_traits_rarity(collection_slug=collection["slug_moon_rank"],collection_size=collection["size"])
        else:
            df_rarity = rarity.get_traits_rarity(collection_slug=slug_name,collection_size=collection["size"])

        df_rarity.to_csv(f"data/{slug_name}/rarity.csv")

    if not os.path.exists(f"data/{slug_name}/listings.csv") or update_listings:
        df_listings = listings.get_listings(slug_name)
        
        if df_listings.empty == False:
            df_listings.to_csv(f"data/{slug_name}/listings.csv")


    if not os.path.exists(f"data/{slug_name}/predicted.csv"):
        print(1)
        #calculate predicted prices
        #@hpink97
    else:
        df_best = best.calculate_best_listings(slug_name)

        df_best.to_csv(f"data/{slug_name}/best_listings.csv")
 
 
for collection in collections:
    get_data_for_collection(collection, update_listings=True) 