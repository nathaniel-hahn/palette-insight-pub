
## graph to compare relative views to peaks based on quarters 
## the printed out data needs to be turned into a csv for accuracy tester
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime



df = pd.read_csv("grouped_data.csv", parse_dates=["Date"])


df_quarters = df.resample('Q', on='Date').mean()

fig, ax = plt.subplots(figsize=(12, 8))


for quarter_start, quarter_data in df.groupby(df['Date'].dt.to_period("Q")):
    top_artists = quarter_data.groupby('Artist')['Predicted_Views'].mean().sort_values(ascending=False).head(10)

    for artist in top_artists.index:
        artist_data = quarter_data[quarter_data['Artist'] == artist]
        ax.bar(artist_data['Date'], artist_data['Predicted_Views'], label=artist)
    print(top_artists)

ax.xaxis_date()
ax.set_xlabel('Date')
ax.set_ylabel('Predicted Views')
ax.set_title('Top 10 Artists Predicted Views Over Time by Quarter')

plt.xticks(rotation=45, ha='right')

ax.legend()

plt.show()
