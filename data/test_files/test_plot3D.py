""" test plot3D """

# imports
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import pyplot as plt


# main function
def main():
    """ === LOAD DATA === """
    # create dataframe with all tracks, reformat and grouped dataframe
    base_df = pd.read_csv(path, sep=';')
    base_df.rename(columns={'XSplined': 'X', 'YSplined': 'Y', 'ZSplined': 'Z'}, inplace=True)
    base_df.drop(columns=['VXSplined', 'VYSplined', 'VZSplined'], inplace=True)
    base_df.dropna(inplace=True)
    grouped_df = base_df.groupby('object')
    
    """ === PLOT === """
    # initial plot settings
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    
    # # get points and create tracks
    # for n, p in grouped_df:
    #     ax.plot3D(p['X'], p['Y'], p['Z'])
    
    # create rectangular box
    p = np.array([[0.2, 0, 0],
                  [0.2, 0.5, 0],
                  [0.4, 0.5, 0],
                  [0.4, 0, 0],
                  [0.2, 0, 0.2],
                  [0.2, 0.5, 0.2],
                  [0.4, 0.5, 0.2],
                  [0.4, 0, 0.2]])
    
    rectangle = [[p[0], p[1], p[2], p[3]],
                 [p[4], p[5], p[6], p[7]],
                 [p[0], p[4], p[7], p[3]],
                 [p[1], p[5], p[6], p[2]],
                 [p[0], p[4], p[5], p[1]],
                 [p[3], p[7], p[6], p[2]]]
    
    ax.add_collection3d(Poly3DCollection(rectangle, facecolors='cyan', linewidths=0.2, edgecolors='cyan', alpha=0.1))
    
    # plot settings
    ax.set_xlim3d(x_start, x_end)
    ax.set_ylim3d(y_start, y_end)
    ax.set_zlim3d(z_start, z_end)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


""" ====== MODIFY HERE ====== """
# path
path = 'test_Splined.csv'

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

""" ====== LAUNCH PROGRAM ====== """
if __name__ == '__main__':
    main()
