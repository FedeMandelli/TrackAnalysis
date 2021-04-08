""" VARIABLE ANALYSIS ALL """

# imports
from data.plot_func import *
import json
from time import perf_counter


# main function
def main():
    # starting settings
    tot_tracks = []
    min_track_len = 3
    x_size = int((x_end - x_start) / size)
    y_size = int((y_end - y_start) / size)
    z_size = int((z_end - z_start) / size)
    
    # get tracks based on type of files analyzed
    if splined:
        # scan all tracks and create a list
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('Splined.csv'):
                    points_file = os.path.join(root, name)
                    
                    # create list with tracks, each track is a list of its positions
                    new_tracks, info = func.get_tracks(points_file)
                    for tr in new_tracks:
                        tot_tracks.append(tr)
    else:
        for j in path_list:
            with open(j) as file:
                data = json.load(file)
                for tr in data[track_type]:
                    if not num_track:
                        tot_tracks.append(tr)
                    else:
                        if tr[0]['object'] in num_track:
                            tot_tracks.append(tr)
    print('tracks loaded')
    
    # progress check
    tot_val = sum([x_size, y_size, z_size]) * len(analysis_type)
    prog = 0
    start_time = perf_counter()
    
    # loop through analysis
    for analysis in analysis_type:
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
            if analysis == 'count':
                x_val[i] = len(mini_tracks)
            
            # tortuosity in box
            if analysis == 'tortuosity':
                x_val[i] = calc_tortuosity(mini_tracks, min_track_len)
            
            # tot time in box
            if analysis == 'tot_time':
                x_val[i] = calc_time_in(mini_tracks, 'tot')
            
            # avg time in box
            if analysis == 'avg_time':
                x_val[i] = calc_time_in(mini_tracks, 'avg')
            
            # average velocity in box
            if analysis == 'velocity':
                x_val[i] = calc_avg_velocity(mini_tracks, min_track_len)
            
            # average acceleration in box
            if analysis == 'acceleration':
                x_val[i] = calc_avg_acc(mini_tracks, min_track_len)
            
            # average angular velocity in box
            if analysis == 'ang_vel':
                x_val[i] = calc_avg_ang_vel(mini_tracks, min_track_len)
            
            # progress
            prog = func.progress(prog, tot_val, start_time)
        
        # loop Y rows
        for i in range(y_size):
            y = float(f'{(y_start + (size * i)):.2f}')
            box = (x_start, x_end), (y, y + size), (z_start, z_end)
            mini_tracks = valid(box, tot_tracks)
            
            # count of mini-tracks in box
            if analysis == 'count':
                y_val[i] = len(mini_tracks)
            
            # tortuosity in box
            if analysis == 'tortuosity':
                y_val[i] = calc_tortuosity(mini_tracks, min_track_len)
            
            # tot time in box
            if analysis == 'tot_time':
                y_val[i] = calc_time_in(mini_tracks, 'tot')
            
            # avg time in box
            if analysis == 'avg_time':
                y_val[i] = calc_time_in(mini_tracks, 'avg')
            
            # average velocity in box
            if analysis == 'velocity':
                y_val[i] = calc_avg_velocity(mini_tracks, min_track_len)
            
            # average acceleration in box
            if analysis == 'acceleration':
                y_val[i] = calc_avg_acc(mini_tracks, min_track_len)
            
            # average angular velocity in box
            if analysis == 'ang_vel':
                y_val[i] = calc_avg_ang_vel(mini_tracks, min_track_len)
            
            # progress
            prog = func.progress(prog, tot_val, start_time)
        
        # loop Z rows
        for i in range(z_size):
            z = float(f'{(z_start + (size * i)):.2f}')
            box = (x_start, x_end), (y_start, y_end), (z, z + size)
            mini_tracks = valid(box, tot_tracks)
            
            # count of mini-tracks in box
            if analysis == 'count':
                z_val[i] = len(mini_tracks)
            
            # tortuosity in box
            if analysis == 'tortuosity':
                z_val[i] = calc_tortuosity(mini_tracks, min_track_len)
            
            # tot time in box
            if analysis == 'tot_time':
                z_val[i] = calc_time_in(mini_tracks, 'tot')
            
            # avg time in box
            if analysis == 'avg_time':
                z_val[i] = calc_time_in(mini_tracks, 'avg')
            
            # average velocity in box
            if analysis == 'velocity':
                z_val[i] = calc_avg_velocity(mini_tracks, min_track_len)
            
            # average acceleration in box
            if analysis == 'acceleration':
                z_val[i] = calc_avg_acc(mini_tracks, min_track_len)
            
            # average angular velocity in box
            if analysis == 'ang_vel':
                z_val[i] = calc_avg_ang_vel(mini_tracks, min_track_len)
            
            # progress
            prog = func.progress(prog, tot_val, start_time)
        
        # plot and save the results
        print(f'creating {analysis} plot')
        plot_xyz_all(x_val, y_val, z_val, analysis, size, x_size, x_start, x_end, y_size, y_start, y_end, z_size,
                     z_start, z_end, path)
    
    # print total time
    print(f'Total Time: {func.time_format(start_time)}')
    
    return


""" ====== MODIFY UNDER HERE ====== """

""" * chose the size of the bin
    * check if working on the Splined file or json
        + if on the Splined (True) just insert the path
        + if on the json:
            - specify the type of track (landed, not landed, mini-tracks in box)
            - insert the path where the folder with the plots will be created
            - insert the directory of all the json files needed in different variables (path_1, path_2)
            - add all the directory variables in the path_list
            - if it's needed a specific track, insert the number in the num_track list
    * if necessary, adjust the area of the wind tunnel """

# main settings
analysis_type = ['count', 'tortuosity', 'tot_time', 'avg_time', 'velocity', 'acceleration', 'ang_vel']
size = 0.1

# path settings
splined = True
if splined:
    path = 'C:/manu/Varie/test'
else:
    track_type = 'landed'  # type of track (landed, not landed, mini-tracks)
    path = 'C:\\manu\\Varie\\test'  # path where the folder with graphs will be created
    path_1 = "C:\\manu\\Varie\\test\\land_or_not_large_1.json"
    # path_2 = "C:\\manu\\Varie\\test\\land_or_not_large_2.json"
    path_list = [path_1]
    num_track = []  # insert number if you want to analyze the single track

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
