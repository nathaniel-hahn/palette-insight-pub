## wiki test api script
## simple grabber that takes in a title and date and then searches wikimedia


import requests
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
#import logging


#logging.basicConfig(level=logging.DEBUG,
 #                   format="%(asctime)s %(levelname)s %(message)s")



def get_pageviews(article_title, start_date, end_date):
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
    endpoint = f"en.wikipedia/all-access/all-agents/{article_title}/daily"

    params = {
        'start': start_date,
        'end': end_date
    }

    url = f"{base_url}/{endpoint}/{start_date}/{end_date}"

    # Set a custom User-Agent header
    headers = {
        'User-Agent': 'put your user agent here)'  ## edit before running!!
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    print(response)

    return data['items']



## tester to make sure we have access to wikipedia
article_title = "Twilight_in_the_Wilderness"
start_date = "20190101"  # Replace with your desired start date in the format YYYYMMDD
end_date = "20230101"    # Replace with your desired end date in the format YYYYMMDD

pageviews_data = get_pageviews(article_title, start_date, end_date)


df = pd.DataFrame(pageviews_data)
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H')
df = df[['timestamp', 'views']]

