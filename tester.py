## accuracy tester compares the forecast to the actual moves by the cma


import pandas as pd
import pickle

with open("puton2023.pkl", 'rb') as pickle_file:
    data = pickle.load(pickle_file)
    # Process the data or print it



names = []


names_found = []


for item in data:
    names.append(item[0])


names = list(set(names))




data2 = pd.read_csv("galleryData.csv")

for item in data2["name"]:
    name = item.split("  ")
    names_found.append(name[0])
    print(name[0])

names_found = list(set(names_found))

common_names_count = 0

for name in names_found:
    if name in names:
        common_names_count += 1


print(common_names_count / len(names_found))
