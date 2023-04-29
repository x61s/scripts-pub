import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_json('sb-converter-coastline-output.json', orient='index')
filter = df["Lat"] != ""
df = df[filter]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
m = 'o'
# m = '^'

filter = (df['Rooms'] == 1)
df1 = df[filter]
xs = df1['Property Size']
ys = df1['SeaDistance']
zs = df1['Price']
ax.scatter(xs, ys, zs, marker=m, label='1+0', s=10, color='lightblue')

filter = ((df['Rooms'] == 2) & (df['Price'] < 200000))
#filter = ((df['Rooms'] == 2) & (df['Price'] > 90000) & (df['Price'] < 95000))
df2 = df[filter]
xs = df2['Property Size']
ys = df2['SeaDistance']
zs = df2['Price']
c = df2['Price'].count()
ax.scatter(xs, ys, zs, marker=m, label='1+1', s=20, color='lightgreen')
#ax.scatter(xs, ys, zs, marker=m, label='{0} obj 1+1 for 90.000 - 95.000 €'.format(c), s=20, color='lightgreen')


filter = (df['Rooms'] == 3)
df3 = df[filter]
xs = df3['Property Size']
ys = df3['SeaDistance']
zs = df3['Price']
ax.scatter(xs, ys, zs, marker=m, label='2+1', s=30, color='red')


filter = (df['Rooms'] == 4)
df4 = df[filter]
xs = df4['Property Size']
ys = df4['SeaDistance']
zs = df4['Price']
ax.scatter(xs, ys, zs, marker=m, label='3+1', s=40, color='white')


ax.set_xlabel('X Property Size')
ax.set_ylabel('Y Distance To The Sea')
ax.set_zlabel('Z Price')



#ax.set_title('Price, Size & Distance')

fig.set_facecolor('#212529')
ax.set_facecolor('#212529')

ax.xaxis.line.set_color("gray")
ax.yaxis.line.set_color("gray")
ax.zaxis.line.set_color("gray")

ax.xaxis.label.set_color("gray")
ax.yaxis.label.set_color("gray")
ax.zaxis.label.set_color("gray")

ax.tick_params(axis='x', colors='gray')
ax.tick_params(axis='y', colors='gray')
ax.tick_params(axis='z', colors='gray')

ax.title.set_color('#ffffff')

legend = plt.legend(loc="upper right", edgecolor="black")
legend.get_frame().set_alpha(None)
legend.get_frame().set_facecolor((0, 0, 0, 0.2))
for text in legend.get_texts():
    plt.setp(text, color = 'w')

ax.grid(False) 
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

plt.show()
