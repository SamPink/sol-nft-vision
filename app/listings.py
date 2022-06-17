import requests
import pandas as pd
import time 

def get_listings(slug):
    LIMIT = 20
    offset = 0
    search = True
    all_listings = pd.DataFrame()
    while search:
        try:
            resp = requests.get(f"https://api-mainnet.magiceden.dev/v2/collections/{slug}/listings?offset={offset}&limit={LIMIT}")

            df = pd.json_normalize(resp.json())
            
            if df.empty:
                search = False
            else:
                all_listings = all_listings.append(df)

                offset += LIMIT

                time.sleep(1)
        except Exception as e:
            print(e)
            search = False
        
    return all_listings
