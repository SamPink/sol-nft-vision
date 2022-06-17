import pandas as pd
import os

def calculate_best_listings(slug):
    listings = pd.read_csv(f"data/{slug}/listings.csv")
    
    predicted = pd.read_csv(f"data/{slug}/predicted.csv")
    
    #join the two dataframes on mint
    df = listings.merge(predicted, left_on="tokenMint", right_on="mint")
    
    df_1 = df[['pred_SOL','price', 'name','rarity_rank','trait_n', 'extra.img']]
    
    #get difference between predicted and actual
    df_1['diff'] = df_1['pred_SOL'] - df_1['price']
    
    #order by difference
    return df_1.sort_values(by='diff', ascending=False)
    
    
    
    