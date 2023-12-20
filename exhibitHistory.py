##builder file that creates a python object holding each artists art
## each artwork also has an exhibition history
## this file is called from readArtists.py

import requests
import pandas as pd
import numpy as np
import re
import csv
from dataclasses import dataclass



@dataclass
class artWork:
    title: str
    onDispaly: bool
    exData: list


@dataclass
class poi:
    name: str
    total: int
    onDisplay: int
    names: list


def run() -> list:
    artists = {}

    with open("artistData.csv", 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            artist = row['title']

            artists[artist] = artists.get(artist, 0) + 1

    #print(artists)

    url = "https://openaccess-api.clevelandart.org/api/artworks/"
    found = []

    for artist in artists.items():
        print(artist[0])

        params = {
            #'limit':  10,
            'artists': artist[0]}
        exhibition_data = []
        poiWorks = []
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            onDisp = []
            

            for item in data["data"]:
                disp =False
                #print("Current location: ", item["current_location"])
                #print("On exhibit?  ", item["current_exhibition"])
                #print("exhibitions: ", item["exhibitions"])
                exhibition_data.append(item["exhibitions"])
                if "current_exhibition" in item:
                    onDisp.append(item)
                    disp = True
                poiWorks.append(artWork(item["title"], disp, item["exhibitions"]))
            found.append(poi(artist[0], (len(exhibition_data) + 1), (len(onDisp) + 1), poiWorks))


            date_pattern = re.compile(r'\([^)]+\)\s*\(([^)]+)\)')



        else:
            print("failed: ", response.status_code)

    #print(found)
    return found





