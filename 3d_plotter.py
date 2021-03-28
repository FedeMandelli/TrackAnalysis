""" 3D PLOTTER """

# imports
import json
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt


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
        ax.plot3D(x, y, z)
        ax.text(point['X'], point['Y'], point['Z'], point['object'])
    
    # plot settings
    ax.set_xlim3d(x_start, x_end)
    ax.set_ylim3d(y_start, y_end)
    ax.set_zlim3d(z_start, z_end)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    
    return


""" ****** MODIFY UNDER HERE ****** """

"""	* set what to plot in the 'to_analyze' list:
        + 'all' will plot all tracks will
        + 'landed' or 'not landed' will plot the full tracks, landed or not, in the box previously analyzed
        + 'minitracks' will plot all the mini-tracks in the box previously analyzed
        + n. track will plot a specific track or multiple numbers separated by comma
    * set the path of the json file with the tracks to plot
    * if necessary, adjust the area of the wind tunnel """

# main settings
to_analyze = ['all']  # all - minitracks - landed - not landed - n.track
file = "C:\\manu\\Varie\\test\\2020_07_27_15_10_09 -exp 14 big vs big\\Py_Analysis_large1\\2020_07_27_15_10_09_land_or_not.json"

# XYZ settings - default: S(0.1) X(-0.1, 1) Y(-0.3, 1.7) Z(-0.1, 1.2)
size = 0.1
x_start = -0.1
x_end = 1
y_start = -0.3
y_end = 1.7
z_start = -0.1
z_end = 1.2

""" ****** LAUNCH PROGRAM ****** """
if __name__ == '__main__':
    plot_3d(to_analyze)
