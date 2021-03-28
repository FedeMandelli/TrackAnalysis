""" plot the speed between two points """

# imports
import os
import data.general_func as func
import matplotlib.pyplot as plt
import numpy as np

# settings
# path = 'C:\\manu\\Varie\\test'
path = 'C:\\manu\\Varie\\postproc tracks\\EXP 2 ORIENTATION choice test'
all_tracks = []
all_speeds = []

# get all tracks
for root, dirs, files in os.walk(path):
    for name in files:
        if name.endswith("Splined.csv"):
            file = os.path.join(root, name)
            trs, info = func.get_tracks(file)
            for tr in trs:
                all_tracks.append(tr)

# get all speeds
for track in all_tracks:
    for i in range(1, len(track)):
        dist = func.two_pt_dist(track[i - 1], track[i])
        time = track[i]['time'] - track[i - 1]['time']
        speed = dist / time
        all_speeds.append(speed)

# plot
plt.hist(all_speeds, range=(0, 1), bins=500)
plt.xticks(np.arange(0, 1, 0.02))
plt.show()
