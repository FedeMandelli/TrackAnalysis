""" 3D PLOTTER """

# imports
import json
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt


# plot tracks in 3D
def plot_3d(info, *args):
    # select the list to plot
    if not args:
        tracks = info['tracks']
    else:
        if args[0] == 'landed':
            tracks = info['landed']
        elif args[0] == 'not landed':
            tracks = info['not landed']
        elif args[0] == 'mini-tracks':
            tracks = info['mini-tracks']
        else:
            tracks = []
            for track in info['tracks']:
                if track[0]['object'] in args:
                    tracks.append(track)
    
    # plot
    fig = plt.figure()
    ax = Axes3D(fig)
    
    # get points and create tracks
    for track in tracks:
        x = []
        y = []
        z = []
        point = 0
        for point in track:
            x.append(point['X'])
            y.append(point['Y'])
            z.append(point['Z'])
        ax.plot3D(x, y, z)
        ax.text(point['X'], point['Y'], point['Z'], point['object'])
    
    # plot box
    xv = [-0.04, 0.44]
    yv = [0.83, 1.45]
    zv = [-0.02, 0.2]
    
    # box_large1 = (-0.04, 0.44), (0.83, 1.45), (-0.02, 0.2)
    
    # plot settings
    ax.set_xlim3d(x_start, x_end)
    ax.set_ylim3d(y_start, y_end)
    ax.set_zlim3d(z_start, z_end)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    
    return


"""
********
* Main *
********
"""

# set path
file = "C:\\manu\\Varie\\test\\land_or_not_large1.json"

# get tracks
new_data = json.load(open(file))

# XYZ settings - default: X(-0.1, 1) Y(-0.3, 1.7) Z(-0.1, 1.2)
size = 0.1
x_start = -0.1
x_end = 1
y_start = -0.3
y_end = 1.7
z_start = -0.1
z_end = 1.2
x_size = int((x_end - x_start) / size)
y_size = int((y_end - y_start) / size)
z_size = int((z_end - z_start) / size)

# se nessun argomento vengono plottate tutte le tracce, se no a scelta tra (mini-tracks, landed, not landed, n.track)
plot_3d(new_data, 'not landed')
