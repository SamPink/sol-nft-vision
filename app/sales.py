import http.client
import pandas as pd
import time

NUM_SALES = 30000
LIMIT = 100


def get_request(slug, offset):
    conn = http.client.HTTPSConnection("api-mainnet.magiceden.dev")
    payload = ""
    headers = {}

    conn.request(
        "GET",
        f"/v2/collections/{slug}/activities?offset={offset}&limit={LIMIT}&type=buyNow",
        payload,
        headers,
    )
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    return data


def get_sales(slug):
    offset = 0
    search = True
    all_trades = pd.DataFrame()
    while search:
        try:
            sales_page = get_request(slug=slug, offset=offset)

            df = pd.read_json(sales_page)
            
            if df.empty:
                search = False

            all_trades = all_trades.append(df)
            
            print(f"df is now {all_trades.shape[0]}")

            offset += LIMIT

            time.sleep(1)
        except Exception as e:
            print(e)
            search = False

        # limit to 100 calls
        if offset > NUM_SALES:
            search = False

    return all_trades
