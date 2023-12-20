
# runner file for the wikimedia stats
# calls wikiGrab.py n times based on what you are doing
# passes the expected dates in as well
# builds artistData.csv 


import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from prophet import Prophet
from wikiGrab import get_pageviews
#import logging
import re
from pathlib import Path


#logging.basicConfig(level=logging.DEBUG,
#                    format="%(asctime)s %(levelname)s %(message)s")
dataPath = Path("artistData.csv")
full_data = pd.DataFrame()
if False: # dataPath.is_file():
    full_data = pd.read_csv("artistData.csv")
else:
    for i in range(3):
        url = "https://openaccess-api.clevelandart.org/api/creators/"
        skipVal = i * 1000
        print("sk ", skipVal)
        params = {
            'skip': skipVal,
            'limit':  1000}
        print(url, params)
        response = requests.get(url, params=params)
        data = response.json()
        print(len(data["data"]))
        for j,art in enumerate(data['data']):
            print("currently at: ", i, j)
            name = art["name"]
            adjName = name.replace(" ", "_")
            try:
                data = get_pageviews(adjName, 20190101, 20230101)

                if data:
                    df = pd.DataFrame(data)
                    df['title'] = name  # Add a 'title' column
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H')
                    full_data = pd.concat([full_data, df])
            except Exception as e:
                print("falied: ", name )

full_data.to_csv("artistData.csv", encoding='utf-8', index=False)



