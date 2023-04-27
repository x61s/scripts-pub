#!/bin/python3

import math
from io import BytesIO
from PIL import Image
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import product
import overpy


TILE_SIZE = 256


def point_to_pixels(lon, lat, zoom):
    """convert gps coordinates to web mercator"""
    r = math.pow(2, zoom) * TILE_SIZE
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y


def get_coastline(bot, lef, top, rgt):
    api = overpy.Overpass()

    # fetch the coastline
    result = api.query("""
        nwr({0},{1},{2},{3}) [natural=coastline];
        (._;>;);
        out body;
        """.format(bot,lef,top,rgt))

    coastline = {}
    node = 0

    for way in result.ways:
        print("  Nodes:")
        for node in way.nodes:
            print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
            coastline[node] = {
                'Lat': float(node.lat),
                'Lon': float(node.lon)
                }

    return coastline


def get_highway(bot, lef, top, rgt):
    api = overpy.Overpass()

    # fetch D-400 trunk coords
    result = api.query("""
        way({0},{1},{2},{3}) ["highway"~"^(trunk)"];
        (._;>;);
        out body;
        """.format(bot,lef,top,rgt))

    highway = {}
    node = 0

    for way in result.ways:
        print("Name: %s" % way.tags.get("name", "n/a"))
        print("  Highway: %s" % way.tags.get("highway", "n/a"))
        print("  Nodes:")
        for node in way.nodes:
            print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
            highway[node] = {
                'Lat': float(node.lat),
                'Lon': float(node.lon)
                }

    return highway


zoom = 15

df = pd.read_json('sb-converter-mercator-output.json', orient='index')
filter = df["Lat"] != ""
df = df[filter]

#filter = (df["Price"] < 100000) & (df["Rooms"] == 3)
#df = df[filter]

#filter = (df["Price"] < 100000) & (df["Property Size"] > 80)
#df = df[filter]

print(df)

top, bot = df.Lat.astype(float).max(), df.Lat.astype(float).min()
lef, rgt = df.Lon.astype(float).min(), df.Lon.astype(float).max()

print('top', top)
print('bot', bot)
print('lef', lef)
print('rgt', rgt)

x0, y0 = point_to_pixels(lef, top, zoom)
x1, y1 = point_to_pixels(rgt, bot, zoom)

print('x0', x0, 'y0', y0)
print('x1', x1, 'y1', y1)

x0_tile, y0_tile = int(x0 / TILE_SIZE), int(y0 / TILE_SIZE)
x1_tile, y1_tile = math.ceil(x1 / TILE_SIZE), math.ceil(y1 / TILE_SIZE)

assert (x1_tile - x0_tile) * (y1_tile - y0_tile) < 50, "That's too many tiles!"





# full size image we'll add tiles to
img = Image.new('RGB', (
    (x1_tile - x0_tile) * TILE_SIZE,
    (y1_tile - y0_tile) * TILE_SIZE))

# loop through every tile inside our bounded box
for x_tile, y_tile in product(range(x0_tile, x1_tile), range(y0_tile, y1_tile)):
    URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format
    headers = {
        'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
        }
    with requests.get(URL(x=x_tile, y=y_tile, z=zoom), headers=headers) as resp:
        resp.raise_for_status() # just in case
        tile_img = Image.open(BytesIO(resp.content))

    # add each tile to the full size image
    img.paste(
        im=tile_img,
        box=((x_tile - x0_tile) * TILE_SIZE, (y_tile - y0_tile) * TILE_SIZE))




# cropping img by min/max points
x, y = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE

img = img.crop((
    int(x0 - x),  # left
    int(y0 - y),  # top
    int(x1 - x),  # right
    int(y1 - y))) # bottom




fig, ax = plt.subplots()

# add points to the scatter
ax.scatter(df.Lon.astype(float), df.Lat.astype(float), alpha=0.5, c='red', s=10, label='Apartments')

# add coastline points to the scatter
coastline = get_coastline(bot, lef, top, rgt)
dfCoastline = pd.DataFrame.from_dict(coastline, orient = 'index')
print(dfCoastline)
ax.scatter(dfCoastline.Lon.astype(float), dfCoastline.Lat.astype(float), alpha=0.5, c='blue', s=2, label='Coastline points')

# add highway points to the scatter
highway = get_highway(bot, lef, top, rgt)
dfHighway = pd.DataFrame.from_dict(highway, orient = 'index')
print(dfHighway)
ax.scatter(dfHighway.Lon.astype(float), dfHighway.Lat.astype(float), alpha=0.5, c='black', s=5, label='Highway points')


ax.imshow(img, extent=(lef, rgt, bot, top))

ax.set_ylim(bot, top)
ax.set_xlim(lef, rgt)

ax.set_title('Map 2023-04-24 [Sahibinden]')
fig.set_facecolor('#212529')
ax.spines['left'].set_color('gray')
ax.spines['right'].set_color('gray')
ax.spines['top'].set_color('gray')
ax.spines['bottom'].set_color('gray')
ax.tick_params(axis='x', colors='gray')
ax.tick_params(axis='y', colors='gray')
ax.title.set_color('#ffffff')

fig.legend(labelcolor='black')


plt.show()
