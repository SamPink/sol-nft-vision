import requests
import pandas as pd
import time
import json
import os

import sales as sales

slug_name = "degods"


# make folder for slug in data if not exists
if not os.path.exists(f"data/{slug_name}"):
    os.makedirs(f"data/{slug_name}")

transactions = sales.get_sales(slug_name)

transactions.to_csv(f"data/{slug_name}/transactions.csv")
