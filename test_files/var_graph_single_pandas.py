""" VARIABLE ANALYSIS SINGLE """

# imports
from pandas_plot_func import *
from time import perf_counter


# main function
def main():
    def load_data():
        """ read the data from all the given files, create list of dataframes with the filtered data """
        
        tracks_list = []
        for file in path_list:
            # load excel file
            df = pd.read_excel(file, sheet_name='3D_data')
            
            # filter needed data
            if 'track' in track_type:
                df = df[df['type'] == 'track'].reset_index(drop=True)
            if 'mini_track' in track_type:
                df = df[df['type'] == 'minitrack'].reset_index(drop=True)
            
            if 'landed' in track_type:
                df = df[df['landed'] == 'yes'].reset_index(drop=True)
            if 'not_landed' in track_type:
                df = df[df['landed'] == 'no'].reset_index(drop=True)
            
            if 'in_box' in track_type:
                df = df[df['in_box'] == 'yes'].reset_index(drop=True)
            
            # append track data to list
            for exp_i, exp in df.groupby('experiment'):
                for tr_i, tr_data in exp.groupby('object'):
                    tracks_list.append(tr_data)
        
        return tracks_list
    
    # starting settings
    min_track_len = 3
    x_size = int((x_end - x_start) / size)
    y_size = int((y_end - y_start) / size)
    z_size = int((z_end - z_start) / size)
    
    # create tracks list
    tot_tracks = load_data()
    
    # progress check
    tot_val = sum([x_size, y_size, z_size])
    prog = 0
    start_time = perf_counter()
    
    # create basic list of values for each axes
    x_val = [0 for _ in range(x_size)]
    y_val = [0 for _ in range(y_size)]
    z_val = [0 for _ in range(z_size)]
    
    # loop X rows
    for i in range(x_size):
        x = float(f'{(x_start + (size * i)):.2f}')
        box = (x, x + size), (y_start, y_end), (z_start, z_end)
        mini_tracks = valid(box, tot_tracks)
        
        # count of mini-tracks in box
        if analysis_type == 'count':
            x_val[i] = len(mini_tracks)
        
        # tortuosity in box
        if analysis_type == 'tortuosity':
            x_val[i] = calc_tortuosity(mini_tracks, min_track_len)
        
        # tot time in box
        if analysis_type == 'tot_time':
            x_val[i] = calc_time_in(mini_tracks, 'tot')
        
        # avg time in box
        if analysis_type == 'avg_time':
            x_val[i] = calc_time_in(mini_tracks, 'avg')
        
        # average velocity in box
        if analysis_type == 'velocity':
            x_val[i] = calc_avg_velocity(mini_tracks, min_track_len)
        
        # average acceleration in box
        if analysis_type == 'acceleration':
            x_val[i] = calc_avg_acc(mini_tracks, min_track_len)
        
        # average angular velocity in box
        if analysis_type == 'ang_vel':
            x_val[i] = calc_avg_ang_vel(mini_tracks, min_track_len)
        
        # progress
        prog = func.progress(prog, tot_val, start_time)
    
    # loop Y rows
    for i in range(y_size):
        y = float(f'{(y_start + (size * i)):.2f}')
        box = (x_start, x_end), (y, y + size), (z_start, z_end)
        mini_tracks = valid(box, tot_tracks)
        
        # count of mini-tracks in box
        if analysis_type == 'count':
            y_val[i] = len(mini_tracks)
        
        # tortuosity in box
        if analysis_type == 'tortuosity':
            y_val[i] = calc_tortuosity(mini_tracks, min_track_len)
        
        # tot time in box
        if analysis_type == 'tot_time':
            y_val[i] = calc_time_in(mini_tracks, 'tot')
        
        # avg time in box
        if analysis_type == 'avg_time':
            y_val[i] = calc_time_in(mini_tracks, 'avg')
        
        # average velocity in box
        if analysis_type == 'velocity':
            y_val[i] = calc_avg_velocity(mini_tracks, min_track_len)
        
        # average acceleration in box
        if analysis_type == 'acceleration':
            y_val[i] = calc_avg_acc(mini_tracks, min_track_len)
        
        # average angular velocity in box
        if analysis_type == 'ang_vel':
            y_val[i] = calc_avg_ang_vel(mini_tracks, min_track_len)
        
        # progress
        prog = func.progress(prog, tot_val, start_time)
    
    # loop Z rows
    for i in range(z_size):
        z = float(f'{(z_start + (size * i)):.2f}')
        box = (x_start, x_end), (y_start, y_end), (z, z + size)
        mini_tracks = valid(box, tot_tracks)
        
        # count of mini-tracks in box
        if analysis_type == 'count':
            z_val[i] = len(mini_tracks)
        
        # tortuosity in box
        if analysis_type == 'tortuosity':
            z_val[i] = calc_tortuosity(mini_tracks, min_track_len)
        
        # tot time in box
        if analysis_type == 'tot_time':
            z_val[i] = calc_time_in(mini_tracks, 'tot')
        
        # avg time in box
        if analysis_type == 'avg_time':
            z_val[i] = calc_time_in(mini_tracks, 'avg')
        
        # average velocity in box
        if analysis_type == 'velocity':
            z_val[i] = calc_avg_velocity(mini_tracks, min_track_len)
        
        # average acceleration in box
        if analysis_type == 'acceleration':
            z_val[i] = calc_avg_acc(mini_tracks, min_track_len)
        
        # average angular velocity in box
        if analysis_type == 'ang_vel':
            z_val[i] = calc_avg_ang_vel(mini_tracks, min_track_len)
        
        # progress
        prog = func.progress(prog, tot_val, start_time)
    
    # print total time
    print(f'\nTotal Time: {func.time_format(start_time)}')
    
    # plot the results
    plot_xyz_single(x_val, y_val, z_val, analysis_type, size, x_size, x_start, x_end, y_size, y_start, y_end, z_size,
                    z_start, z_end)
    
    return


""" ====== MODIFY UNDER HERE ====== """

"""	* chose the type of analysis to be performed
    * chose the size of the bin
    * check if working on the Splined file or json
        + if on the Splined (True) just insert the path
        + if on the json:
            - specify the type of track (landed, not landed, mini-tracks in box)
            - insert the directory of all the json files needed in different variables (path_1, path_2)
            - add all the directory variables in the path_list
            - if it's needed a specific track, insert the number in the num_track list
    * if necessary, adjust the area of the wind tunnel """

# main settings
analysis_type = 'count'  # count - tortuosity - tot_time - avg_time - velocity - acceleration - ang_vel
size = 0.1

# path settings
path1 = 'C:/manu/test/test_pandas_analysis.xlsx'
track_type = ('track', 'all')  # track/mini_track | landed/not_landed/all | in_box
path_list = [path1]
num_track = []  # insert numbers if you want to analyze the single track

# XYZ settings - default: S(0.1) X(-0.1, 1) Y(-0.3, 1.7) Z(-0.1, 1.2)
x_start = -0.1
x_end = 1
y_start = -0.3
y_end = 1.7
z_start = -0.1
z_end = 1.2

""" ====== LAUNCH PROGRAM ====== """
if __name__ == '__main__':
    main()
