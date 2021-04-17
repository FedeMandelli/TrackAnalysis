""" 3D PLOTTER """

# imports
import pandas as pd
from numpy import array
from itertools import product
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# plot tracks in 3D
def plot_3d(an_tp):
    # load dataframe
    df = pd.read_excel(file, sheet_name='3D_data')
    
    """ === Tracks to Plot === """
    # type of track
    if 'tracks' in an_tp:
        df = df[(df['type'] == 'track')]
    if 'minitracks' in an_tp:
        df = df[(df['type'] == 'minitrack')]
    if 'landed' in an_tp:
        df = df[(df['landed'] == 'yes')]
    if 'not landed' in an_tp:
        df = df[(df['landed'] == 'no')]
    
    # track number if required
    nums = []
    for i in an_tp:
        if isinstance(i, int):
            nums.append(i)
    if nums:
        df = df[(df['object'].isin(nums))]
    
    """ === Plot === """
    # basic settings
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    
    # create tracks
    for n_track, track_data in df.groupby('object'):
        ax.plot3D(track_data['X'], track_data['Y'], track_data['Z'], label=n_track)
        ax.text(track_data.iloc[-1]['X'], track_data.iloc[-1]['Y'], track_data.iloc[-1]['Z'], n_track)
    
    # create boxes areas
    if boxes:
        for box in boxes:
            p = array(list(product(box[0], box[1], box[2])))
            rect = [[p[0], p[2], p[6], p[4]],
                    [p[1], p[3], p[7], p[5]],
                    [p[0], p[2], p[3], p[1]],
                    [p[4], p[5], p[7], p[6]],
                    [p[0], p[1], p[5], p[4]],
                    [p[2], p[3], p[7], p[6]]]
            ax.add_collection3d(Poly3DCollection(rect, facecolors='cyan', linewidths=.1, edgecolors='cyan', alpha=.05))
    
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
to_analyze = ['tracks']  # (tracks - minitracks) - (landed - not landed) - n.track
file = 'C:/manu/test/test_pandas_analysis.xlsx'

# boxes
box_large1 = (-0.04, 0.44), (0.83, 1.45), (-0.02, 0.2)
box_large2 = (0.44, 0.95), (0.83, 1.45), (-0.02, 0.2)
boxes = [box_large1]

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
