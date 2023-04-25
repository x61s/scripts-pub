import overpy

api = overpy.Overpass()

bot = 36.61986688336028
lef = 31.762677282989497
top = 36.63746852292138
rgt = 31.78588008930335

# fetch the coastline
result = api.query("""
    nwr({0},{1},{2},{3}) [natural=coastline];
    (._;>;);
    out body;
    """.format(bot,lef,top,rgt))

nodes = []

for way in result.ways:
    print("  Nodes:")
    for node in way.nodes:
        #print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
        nodes.append((float(node.lat), float(node.lon)))

for node in nodes:
    print(node)
