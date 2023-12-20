## main script that buiilds the models
## program checks if file for artists exists and builds it if not
## reads in csv file of artist data
## uses regex for finding dates in exhibition history
## compares dates to our relevant range
## determines artists and work that is relevant
## trains model on relevant artists
## saves artists and peaks
## finds and saves changes in 2023 to compare to our predictions



import pickle
import pandas as pd
import re
import os
import logging
from exhibitHistory import run
from datetime import datetime
import matplotlib.pyplot as plt
from prophet import Prophet
from scipy.optimize import linear_sum_assignment
from prophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

if os.path.exists("artists.pkl"):
    with open("artists.pkl", "rb") as file:
        artists = pickle.load(file)

else:
    artists = run()
    with open('artists.pkl', 'wb') as file:
        pickle.dump(artists, file)
        


putondisp = []
puton2023 = []
bestPerPerson = pd.DataFrame(columns=["Date", "Predicted_Views", "Artist"])


fullWiki = pd.read_csv("artistData.csv")

def interest(name: str) -> list:
    artistdf = fullWiki[fullWiki['title'] == name]
    print(artistdf.groupby("title", as_index=False)['views'].mean())
    print(artistdf.groupby("title", as_index=False)['views'].max())
    print(artistdf.groupby("title", as_index=False)['views'].std())


# determine poi (person of interest)
# determine date and pass to respective functions
def getArt(findName: str) -> list:
    poi = next((x for x in artists if x.name == findName), None)
    for art in poi.names:
        date_pattern = re.compile(r'\([^)]+\)\s*\(([^)]+)\)')
        #print(art.exData)
        for key, val in art.exData.items():
            if len(val) != 0 and key != "legacy":
               #print(key, val)
               #print(exhibit["title"], exhibit["opening_date"])


               for k, v in val[0].items():
                   if k == "description" :
                        dateMatch =  date_pattern.search(v)
                        dateRange = dateMatch.group(1) if dateMatch else None
                        print(dateRange, past2019(dateRange))
                        if past2019(dateRange):
                            putondisp.append([findName, turnDates(dateRange)])
                        if past2023(dateRange):
                            puton2023.append([findName, turnDates(dateRange)])




# checks if the artist is relevant based on their arts exhibition history
def past2019(date_range) -> bool:
    if date_range is None:
        return False
    
    try:
        start, end = date_range.split('-')
        #print(start, end)
        if len(start.split())  != len(end.split()):
            _, end_year = end.split(",")
            start = start + "," + end_year
        #print(start, end)

        start = datetime.strptime(start, '%B %d, %Y')
        end = datetime. strptime(end, '%B %d, %Y')

        ref = datetime(2019, 1, 1)
        return start > ref or end > ref
    except:
        print("failed date_range: ", date_range)
        return False

# checks if art has been moved in 2023
def past2023(date_range) -> bool:
  if date_range is None:
        return False
  try:
        start, end = date_range.split('-')
        #print(start, end)
        if len(start.split())  != len(end.split()):
            _, end_year = end.split(",")
            start = start + "," + end_year
        #print(start, end)

        start = datetime.strptime(start, '%B %d, %Y')
        end = datetime. strptime(end, '%B %d, %Y')

        ref = datetime(2023, 1, 1)
        return start > ref or end > ref
  except:
        print("failed date_range: ", date_range)
        return False

# converts dates
def turnDates(date_range) -> list:
    start, end = date_range.split('-')
    #print(start, end)
    if len(start.split())  != len(end.split()):
        _, end_year = end.split(",")
        start = start + "," + end_year
    #print(start, end)

    start = datetime.strptime(start, '%B %d, %Y')
    end = datetime. strptime(end, '%B %d, %Y')

    return [start, end]



# builds list of art on display
for i in range(len(artists)):
    name = artists[i].name
    getArt(name)
print(putondisp)


#basic graph function with period where art is displayed
def graphPerson(name: str) -> None:
    artResponse = pd.DataFrame(putondisp, columns=['artist', 'display_period'])
    merged = pd.merge(fullWiki, artResponse, left_on='title', right_on='artist')

    merged['timestamp'] = pd.to_datetime(merged['timestamp'])

    workingDF = merged[merged["title"] == name]

    plt.figure(figsize=(10, 6))
    plt.scatter(workingDF['timestamp'], workingDF['views'], label='Wikipedia Views')
    plt.title(name + " Wikipedia Views Over Time")
    plt.xlabel('Date')
    plt.ylabel('Views')
    plt.legend()

    display_start, display_end = workingDF['display_period'].iloc[0]
    plt.axvspan(display_start, display_end, color='yellow', alpha=0.3, label='Art on Display')
    plt.legend()

    plt.show()

## builds model and graphs if uncommented
## accuracy commented out
def prophetPerson(name: str) -> list:
    artResponse = pd.DataFrame(putondisp, columns=['artist', 'display_period'])
    merged = pd.merge(fullWiki, artResponse, left_on='title', right_on='artist')

    merged['timestamp'] = pd.to_datetime(merged['timestamp'])
    workingDF = merged[merged["title"] == name]

    prophetData = workingDF[['timestamp', 'views']].rename(columns={'timestamp': 'ds', 'views': 'y'})
    model = Prophet()
    model.fit(prophetData)

    future = model.make_future_dataframe(periods=365)

    forecast = model.predict(future)

    fForecast = forecast[forecast['ds'] > max(workingDF['timestamp'])]

    best_time_to_display = fForecast.nlargest(3, 'yhat')[['ds', 'yhat']]
    best_time_to_display["Artist"] = name
    best_time_to_display.columns = ['Date', 'Predicted_Views', "Artist"]

    
    ## accuracy
    #df_cv = cross_validation(model, initial='100 days', period='180 days', horizon = '365 days')
    #cutoffs = pd.to_datetime(['2021-02-15'])
    #df_cv2 = cross_validation(model, cutoffs=cutoffs, horizon='365 days')
    #df_p = performance_metrics(df_cv)
    #print(df_p.head())
    
    # graph
    #fig, ax = plt.subplots(figsize=(10, 6))
    #model.plot(forecast, ax=ax)
    #plt.title(name + " Wikipedia Views Forecast")
    #plt.xlabel('Date')
    #plt.ylabel('Views')

    #for index, row in best_time_to_display.iterrows():
     #   plt.axvline(row['Date'], color='red', linestyle='--', label='Best Time to Display')
    #plt.legend()
   # plt.show()


    return best_time_to_display

# split jobs to run in parallel - not implemented in this version 
for i in range(100):
    name = putondisp[i][0]
    #graphPerson(name)
    print("on prophet ", i, len(putondisp))
    logging.info(f'Processing art {i} of {len(putondisp)}')

    bestPerPerson = bestPerPerson.append(prophetPerson(name), ignore_index =True)

for i in range(100):
    name = putondisp[i+ 100][0]
    #graphPerson(name)
    print("on prophet ", (100+i), len(putondisp))
    logging.info(f'Processing art {i} of {len(putondisp)}')

    bestPerPerson = bestPerPerson.append(prophetPerson(name), ignore_index =True)

for i in range(145):
    name = putondisp[i+ 200][0]
    #graphPerson(name)
    print("on prophet ", (200+i), len(putondisp))
    logging.info(f'Processing art {i} of {len(putondisp)}')

    bestPerPerson = bestPerPerson.append(prophetPerson(name), ignore_index =True)







# save python object

bestPerPerson.to_csv('grouped_data.csv', index=False)
with open('puton2023.pkl', 'wb') as file:
        pickle.dump(puton2023, file)



