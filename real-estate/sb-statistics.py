#!/bin/python3

import pandas as pd
import numpy as np


df = pd.read_json('sb-converter-coastline-output.json', orient='index')
filter = df["Lat"] != ""
df = df[filter]

def stats(df):
    print('Median', round(df['m2Price'].median()))
    print('Min', round(df['m2Price'].min()))
    print('Max', round(df['m2Price'].max()))
    print('Mean (avg)', round(df['m2Price'].mean()))

    print('Median Price', round(df['Price'].median()))
    print('Min Price', round(df['Price'].min()))
    print('Max Price', round(df['Price'].max()))
    print('Mean Price', round(df['Price'].mean()))

    print(df['Price'].count())
    print()

filter = (df['Rooms'] == 1)
df10 = df[filter]

#filter = (df["Price"] < 100000) & (df["Rooms"] == 3)
#df = df[filter]

#filter = (df["Price"] < 100000) & (df["Property Size"] > 80)
#df = df[filter]

# no1 way to calculate m2 price
#df['m2Price'] = np.where(df['Price'] is np.nan, np.nan, df['Price']/df['Property Size'])

# no2 way to calculate m2 price
#df['m2Price'] = df.apply(lambda x: np.nan if x['Price'] is np.nan else x['Price']/x['Property Size'], axis=1)

# no3 way to calculate m2 price
df10.loc[df['Price'] != np.nan, 'm2Price'] = df10['Price']/df10['Property Size']
df10.loc[df['Price'] == np.nan, 'm2Price'] = np.nan
print('1+0 statistics')
stats(df10)



filter = ((df['Rooms'] == 2) & (df['Price'] < 200000))
df11 = df[filter]

# no3 way to calculate m2 price
df11.loc[df11['Price'] != np.nan, 'm2Price'] = df11['Price']/df11['Property Size']
df11.loc[df11['Price'] == np.nan, 'm2Price'] = np.nan

print('1+1 statistics')
stats(df11)



#filter = ((df['Rooms'] == 3) & (df['Price'] < 500000))
filter = ((df['Rooms'] == 3))
df21 = df[filter]

# no3 way to calculate m2 price
df21.loc[df21['Price'] != np.nan, 'm2Price'] = df21['Price']/df21['Property Size']
df21.loc[df21['Price'] == np.nan, 'm2Price'] = np.nan

print('2+1 statistics')
stats(df21)



filter = ((df['Rooms'] == 4))
df31 = df[filter]

# no3 way to calculate m2 price
df31.loc[df31['Price'] != np.nan, 'm2Price'] = df31['Price']/df31['Property Size']
df31.loc[df31['Price'] == np.nan, 'm2Price'] = np.nan

print('3+1 statistics')
stats(df31)


