import requests
import pandas as pd
import numpy as np


def get_traits_rarity(collection_slug, collection_size):
    url = f'https://moonrank.app/mints/{collection_slug}?after=0&seen={collection_size}&complete=true'
    response = requests.request("GET", url).json()
    data = response['mints']


    df = pd.DataFrame.from_records(data)[['name','rank','rarity']]
    df = df.rename(columns={'rank':'rarity_rank','rarity':'overall_rarity'})
    df.head()

    df_traits = pd.json_normalize(data, 'rank_explain',meta='name').drop_duplicates()

    trait_list = df_traits.attribute.unique()

    traits_pivot =df_traits.pivot(index='name', columns="attribute", values=['value','value_perc']).reset_index()
    new_colnames = []
    for lvl_1, lvl_2 in traits_pivot.columns:
        if lvl_1 == 'value_perc':
            new_colnames.append(f"{lvl_2}_rarity")
        elif lvl_1 == 'name':
            new_colnames.append('name')
        else:
            new_colnames.append(lvl_2)

    traits_pivot.columns = new_colnames

    #merge with the total rank
    traits_pivot = traits_pivot.merge(df, on='name',how='outer')

    #store empty string as NaN
    traits_pivot = traits_pivot.replace(r'^\s*$', np.nan, regex=True)
    rarity_cols = [x + '_rarity' for x in trait_list]

    traits_pivot['min_rarity'] = traits_pivot[rarity_cols].min(axis=1)
    traits_pivot['mean_rarity'] = traits_pivot[rarity_cols].mean(axis=1)
    traits_pivot['trait_n'] = traits_pivot[trait_list].count(axis=1)
    traits_pivot = traits_pivot.sort_values('rarity_rank',ascending=True).reset_index(drop=True)
    
    return traits_pivot

