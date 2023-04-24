#!/bin/python3

import math
from io import BytesIO
from PIL import Image
import requests
import matplotlib.pyplot as plt


TILE_SIZE = 256


def point_to_pixels(lon, lat, zoom):
    """convert gps coordinates to web mercator"""
    r = math.pow(2, zoom) * TILE_SIZE
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y



zoom = 16

x, y = point_to_pixels(31.773725651762714, 36.63322994314836, zoom)
x_tiles, y_tiles = int(x / TILE_SIZE), int(y / TILE_SIZE)

# format the url
URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format
url = URL(x=x_tiles, y=y_tiles, z=zoom)

# make the request
headers = {
    'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
    }
with requests.get(url, headers=headers) as resp:
    resp.raise_for_status() # just in case
    img = Image.open(BytesIO(resp.content))



# plot the tile
fig, ax = plt.subplots()

ax.imshow(img)

ax.set_title('A Tile: zoom {0}x'.format(zoom))
fig.set_facecolor('#212529')
ax.spines['left'].set_color('gray')
ax.spines['right'].set_color('gray')
ax.spines['top'].set_color('gray')
ax.spines['bottom'].set_color('gray')
ax.tick_params(axis='x', colors='gray')
ax.tick_params(axis='y', colors='gray')
ax.title.set_color('#ffffff')

plt.show()
