""" splined file analysis """

# imports
import os
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt


# main function
def main():
    def plot_still_points():
        # plot
        fig = plt.figure()
        ax = Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)
        
        # get points and create tracks
        for track in still_points:
            for n, points in track.groupby('object'):
                ax.plot3D(points['X'], points['Y'], points['Z'])
        
        # plot
        plt.show()
    
    # create info dataframe
    info_df = pd.DataFrame()
    still_points = []
    
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('Splined.csv'):
                folder = root.split(os.path.sep)[-1]
                
                # create dataframe with all tracks, reformat and grouped dataframe
                base_df = pd.read_csv(os.path.join(root, name), sep=';')
                base_df.rename(columns={'XSplined': 'X', 'YSplined': 'Y', 'ZSplined': 'Z'}, inplace=True)
                base_df.drop(columns=['VXSplined', 'VYSplined', 'VZSplined'], inplace=True)
                base_df.dropna(inplace=True)
                grouped_df = base_df.groupby('object')
                
                # analyze tracks
                for n_track, track_data in grouped_df:
                    # get track information
                    points = track_data['object'].count()
                    tot_time = track_data['time'].max() - track_data['time'].min()
                    x_move = track_data['X'].max() - track_data['X'].min()
                    y_move = track_data['Y'].max() - track_data['Y'].min()
                    z_move = track_data['Z'].max() - track_data['Z'].min()
                    still = 'yes' if all(p < 0.01 for p in [x_move, y_move, z_move]) else 'no'
                    
                    # append to the still points list
                    if still == 'yes':
                        still_points.append(track_data)
                    
                    # append to info dataframe
                    info_df = info_df.append({'folder': folder,
                                              'num track': n_track,
                                              'points': points,
                                              'tot time': tot_time,
                                              'x move': x_move,
                                              'y move': y_move,
                                              'z move': z_move,
                                              'still': still}, ignore_index=True)
    
    # export info
    # info_df.to_excel(os.path.join(path, 'tracks_recap.xlsx'), index=False)
    
    # plot points
    plot_still_points()


""" ****** MODIFY UNDER HERE ****** """
path = 'C:/manu/Varie/postproc tracks'

""" ****** LAUNCH PROGRAM ****** """
if __name__ == '__main__':
    main()
