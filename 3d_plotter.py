""" 3D PLOTTER """

# imports
import json
import numpy as np
from itertools import product
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# plot tracks in 3D
def plot_3d(an_tp):
    # starting settings
    info = json.load(open(file))
    
    # select the list to plot
    if 'all' in an_tp:
        tracks = info['tracks']
    else:
        if 'landed' in an_tp:
            tracks = info['landed']
        elif 'not landed' in an_tp:
            tracks = info['not landed']
        elif 'minitracks' in an_tp:
            tracks = info['mini-tracks']
        else:
            tracks = []
            for track in info['tracks']:
                if track[0]['object'] in an_tp:
                    tracks.append(track)
    
    # plot
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    
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
        ax.plot3D(x, y, z, label=point['object'])
        ax.text(point['X'], point['Y'], point['Z'], point['object'])
    
    # create boxes areas
    if boxes:
        for box in boxes:
            p = np.array(list(product(box[0], box[1], box[2])))
            rectangle = [[p[0], p[2], p[6], p[4]],
                         [p[1], p[3], p[7], p[5]],
                         [p[0], p[2], p[3], p[1]],
                         [p[4], p[5], p[7], p[6]],
                         [p[0], p[1], p[5], p[4]],
                         [p[2], p[3], p[7], p[6]]]
            ax.add_collection3d(
                    Poly3DCollection(rectangle, facecolors='cyan', linewidths=0.1, edgecolors='cyan', alpha=0.05))
    
    # plot settings
    ax.set_xlim3d(x_start, x_end)
    ax.set_ylim3d(y_start, y_end)
    ax.set_zlim3d(z_start, z_end)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # ax.legend()
    plt.show()
    
    return


""" ====== MODIFY UNDER HERE ====== """

"""	* set what to plot in the 'to_analyze' list:
        + 'all' will plot all tracks will
        + 'landed' or 'not landed' will plot the full tracks, landed or not, in the box previously analyzed
        + 'minitracks' will plot all the mini-tracks in the box previously analyzed
        + n. track will plot a specific track or multiple numbers separated by comma
    * set the path of the json file with the tracks to plot
    * define the areas to show in the plot and put them in the boxes list
    * if necessary, adjust the area of the wind tunnel """

# main settings
to_analyze = ['all']  # all - minitracks - landed - not landed - n.track
file = 'C:/manu/test/2020_07_27_14_21_03 - exp 13 small vs small/Py_Analysis_large1/2020_07_27_14_21_03_land_or_not.json'

# boxes
box_large1 = (-0.04, 0.44), (0.83, 1.45), (-0.02, 0.2)
box_large2 = (0.44, 0.95), (0.83, 1.45), (-0.02, 0.2)
boxes = []

# XYZ settings - default: S(0.1) X(-0.1, 1) Y(-0.3, 1.7) Z(-0.1, 1.2)
size = 0.1
x_start = -0.1
x_end = 1
y_start = -0.3
y_end = 1.7
z_start = -0.1
z_end = 1.2

""" ====== LAUNCH PROGRAM ====== """
if __name__ == '__main__':
    plot_3d(to_analyze)
