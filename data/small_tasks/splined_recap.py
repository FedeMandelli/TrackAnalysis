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
            for n, p in track.groupby('object'):
                ax.plot3D(p['X'], p['Y'], p['Z'])
        
        # plot
        plt.show()
    
    # create tracks info dataframe
    tracks_info_cols = ['experiment', 'num track', 'points', 'tot time', 'still', 'x move', 'y move', 'z move']
    tracks_info_df = pd.DataFrame(columns=tracks_info_cols)
    
    # create experiment info dataframe
    exp_info_cols = ['experiment', 'total', 'still', 'normal', 'points', 'time normal', 'time sum']
    exp_info_df = pd.DataFrame(columns=exp_info_cols)
    
    # search and analyze Splined.csv
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('Splined.csv'):
                # basic info
                folder = root.split(os.path.sep)[-1]
                still_points = []
                time_exp = 0
                
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
                    time_exp += tot_time
                    x_move = track_data['X'].max() - track_data['X'].min()
                    y_move = track_data['Y'].max() - track_data['Y'].min()
                    z_move = track_data['Z'].max() - track_data['Z'].min()
                    still = 'yes' if all(p < min_still for p in [x_move, y_move, z_move]) else 'no'
                    
                    # append to the still points list
                    if still == 'yes':
                        still_points.append(track_data)
                    
                    # append to tracks info dataframe
                    tracks_info_df = tracks_info_df.append({'experiment': folder,
                                                            'num track': n_track,
                                                            'points': points,
                                                            'tot time': tot_time,
                                                            'x move': x_move,
                                                            'y move': y_move,
                                                            'z move': z_move,
                                                            'still': still},
                                                           ignore_index=True)
                
                # append to experiment info dataframe
                exp_info_df = exp_info_df.append({'experiment': folder,
                                                  'total': len(grouped_df),
                                                  'still': len(still_points),
                                                  'normal': len(grouped_df) - len(still_points),
                                                  'points': len(base_df),
                                                  'time normal': base_df['time'].max() - base_df['time'].min(),
                                                  'time sum': time_exp},
                                                 ignore_index=True)
    
    # export info
    excel_writer = pd.ExcelWriter(os.path.join(path, 'tracks_recap.xlsx'), engine='xlsxwriter')
    tracks_info_df.to_excel(excel_writer, sheet_name='Tracks', index=False)
    exp_info_df.to_excel(excel_writer, sheet_name='Experiments', index=False)
    excel_writer.save()
    
    # plot points
    # plot_still_points()


""" ****** MODIFY UNDER HERE ****** """
path = 'C:/manu/test'
min_still = 0.01

""" ****** LAUNCH PROGRAM ****** """
if __name__ == '__main__':
    main()
