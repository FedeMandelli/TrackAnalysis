""" test plot3D """

# imports
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
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

    # get points and create tracks
    for n, p in grouped_df:
        ax.plot3D(p['X'], p['Y'], p['Z'])

    # plot
    plt.show()


""" ====== MODIFY HERE ====== """
path = 'test_Splined.csv'

""" ====== LAUNCH PROGRAM ====== """
if __name__ == '__main__':
    main()
