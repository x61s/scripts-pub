#!/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dfWeb = pd.read_json('for-sale-2023-04-09.json', orient='index')
axWeb = dfWeb.plot(kind='scatter', x='Property Size', y='Price', color='red', label='RH Web scraping')

dfSahibinden = pd.read_json('sahibinden-converted-output.json', orient='index')
axSahibinden = dfSahibinden.plot(ax=axWeb, kind='scatter', x='Property Size', y='Price', color='purple', label='Sahibinden Web scraping')
print(dfSahibinden)

dfTelegram = pd.read_json('tg-output.json', orient='index')
dfTelegram.replace('', np.NaN, inplace=True)
print(dfTelegram)

P = dfTelegram.plot(ax=axSahibinden, kind='scatter', x='Property Size', y='Price', alpha=1.0, color='lightblue', label='Telegram public chat')

P.legend(facecolor='darkgray')

P.set_title('Prices scatter 2023-04-17 [Sahibinden]')
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

plt.show()
