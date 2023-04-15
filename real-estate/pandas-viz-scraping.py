#!/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json('for-sale-2023-04-09.json', orient='index')
print(df)

P = df.plot(kind='scatter', x='Property Size', y='Price', color='red')

P.set_title('Prices scatter - most dense dataframe segment with distance to the sea')
P.set_facecolor('#000000')
P.xaxis.label.set_color('gray')
P.yaxis.label.set_color('gray')
P.spines['left'].set_color('gray')
P.spines['right'].set_color('gray')
P.spines['top'].set_color('gray')
P.spines['bottom'].set_color('gray')
P.tick_params(axis='x', colors='gray')
P.tick_params(axis='y', colors='gray')
P.title.set_color('#ffffff')

fig = P.get_figure()
fig.set_facecolor('#212529')
fig.set_edgecolor('#212529')

for index, row in df.iterrows():
    print(index, row['Property ID'], row['Property Size'], row['Price'], row['Rooms'], row['Distance to the sea'], row['Year Built'])
    dist = row['Distance to the sea']
    if not pd.isna(dist):
        dist = int(dist)
        if dist <= 10: dist *= 1000 # There is no property at 10 meters to the sea in Avsallar
        if dist > 10 and dist < 30: dist *= 100 # There is no property closer than 30 and farther than 3 km from RH company to sale

        hint = str(dist)

        rooms = row['Rooms']
        if not pd.isna(rooms):
            hint = str(dist) + '/' + str(int(rooms))

        plt.annotate(hint, (float(row['Property Size']), float(row['Price']) + 1500), color='#ffffff', ha='center', va="center")

plt.show()
