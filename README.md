
Palette Insight 
By Nathaniel Hahn and Camden Larson

This is a project designed to forecast and associate trends with the CMA collection.
It consists of multiple preprocessing steps which can be computationally heavy

To run the program make sure you have the following:
numpy
pickle
pandas
re
os
requests
seaborn
numpy
matplotlib
prophet
scipy

Once these are properly installed, you can begin running the program

first, run wikiRunner.py to build your view data set. I would change the for loop to only run once to speed this up
once the csv is saved run readArtists.py
This is extremely computationally heavy and took my system running in parallel multiple hours to complete
I would adjust the for loop at the end to only run 10 or so times - adjust comments as needed if you want to see accuracy or graphs
Lastly, run chisel.py to see the predictions and a graph of when each peak is relative to the artist and views

To compare the predictions to the actual museum exhibits create a csv of each name and quarter from the chisel output, then run tester.py

An easier way to forcast the data is using a python note book that I have attached. Simply add artistData.csv, artists.pkl, and exhibitHistory.py and run the notebook. This will provide 5 example graphs.


Data from the main run can be found here:
https://drive.google.com/drive/folders/1k9VqzdxlIUjndyFY9EFC98rPAlTduPMd?usp=sharing




Please reach out to us with any questions.
Nathaniel Hahn - nrh51@case.edu
Camnden Larson - sl117@case.edu
