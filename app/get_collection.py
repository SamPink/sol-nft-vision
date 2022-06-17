import os

import sales
import rarity
import listings

collections = [
    {"name": "Okay Bear", "slug": "okay-bear", "size": 10000},
    {"name": "Trippin' Ape Tribe", "slug": "trippin_ape_tribe", "size": 10000},
]

def get_data_for_collection(slug_name, size):
    # make folder for slug in data if not exists
    if not os.path.exists(f"data/{slug_name}"):
        os.makedirs(f"data/{slug_name}")

    #df_transactions = sales.get_sales(slug_name)

    #df_transactions.to_csv(f"data/{slug_name}/transactions.csv")

    df_rarity = rarity.get_traits_rarity(collection_slug=slug_name,collection_size=size)

    df_rarity.to_csv(f"data/{slug_name}/rarity.csv")

    df_listings = listings.get_listings(slug_name)

    df_listings.to_csv(f"data/{slug_name}/listings.csv")


    #run model 

    #best value listings
    
get_data_for_collection(collections[1]["slug"], collections[1]["size"])