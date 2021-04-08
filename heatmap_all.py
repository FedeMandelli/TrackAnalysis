""" HEATMAP ALL """

# imports
from data.plot_func import *
from time import perf_counter


# main
def main():
    # starting settings
    tot_tracks = []
    min_track_len = 3
    x_size = int((x_end - x_start) / size)
    y_size = int((y_end - y_start) / size)
    z_size = int((z_end - z_start) / size)
    
    # scan all tracks and create a list
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('Splined.csv'):
                points_file = os.path.join(root, name)
                # create list with tracks, each track is a list of its positions
                new_tracks, info = func.get_tracks(points_file)
                for tr in new_tracks:
                    tot_tracks.append(tr)
    print('tracks loaded')
    
    # progress check
    tot_squares = ((x_size * y_size) + (y_size * z_size) + (x_size * z_size)) * len(analysis_type)
    prog = 0
    start_time = perf_counter()
    
    # loop through analysis
    for analysis in analysis_type:
        
        # create basic XY, YZ and XZ matrix
        xy_values = [[0 for _ in range(x_size)] for _ in range(y_size)]
        yz_values = [[0 for _ in range(y_size)] for _ in range(z_size)]
        xz_values = [[0 for _ in range(x_size)] for _ in range(z_size)]
        
        # loop through XY boxes
        for i in range(y_size):
            y = float(f'{(y_start + (size * i)):.2f}')
            for j in range(x_size):
                x = float(f'{(x_start + (size * j)):.2f}')
                
                # create list of mini-tracks in box
                box = (x, x + size), (y, y + size), (z_start, z_end)
                mini_tracks = valid(box, tot_tracks)
                
                # count of mini-tracks in box
                if analysis == 'count':
                    xy_values[i][j] = len(mini_tracks)
                
                # tortuosity in box
                if analysis == 'tortuosity':
                    xy_values[i][j] = calc_tortuosity(mini_tracks, min_track_len)
                
                # average time in box
                if analysis == 'avg_time':
                    xy_values[i][j] = calc_time_in(mini_tracks, 'avg')
                
                # total time in box
                if analysis == 'tot_time':
                    xy_values[i][j] = calc_time_in(mini_tracks, 'tot')
                
                # average velocity in box
                if analysis == 'velocity':
                    xy_values[i][j] = calc_avg_velocity(mini_tracks, min_track_len)
                
                # average acceleration in box
                if analysis == 'acceleration':
                    xy_values[i][j] = calc_avg_acc(mini_tracks, min_track_len)
                
                # average angular velocity in box
                if analysis == 'ang_vel':
                    xy_values[i][j] = calc_avg_ang_vel(mini_tracks, min_track_len)
                
                # progress
                prog = func.progress(prog, tot_squares, start_time)
        
        # loop through YZ boxes
        for i in range(z_size):
            z = float(f'{(z_start + (size * i)):.2f}')
            for j in range(y_size):
                y = float(f'{(y_start + (size * j)):.2f}')
                
                # count mini-tracks in box
                box = (x_start, x_end), (y, y + size), (z, z + size)
                mini_tracks = valid(box, tot_tracks)
                
                # count of mini-tracks in box
                if analysis == 'count':
                    yz_values[i][j] = len(mini_tracks)
                
                # tortuosity in box
                if analysis == 'tortuosity':
                    yz_values[i][j] = calc_tortuosity(mini_tracks, min_track_len)
                
                # average time in box
                if analysis == 'avg_time':
                    yz_values[i][j] = calc_time_in(mini_tracks, 'avg')
                
                # total time in box
                if analysis == 'tot_time':
                    yz_values[i][j] = calc_time_in(mini_tracks, 'tot')
                
                # average velocity in box
                if analysis == 'velocity':
                    yz_values[i][j] = calc_avg_velocity(mini_tracks, min_track_len)
                
                # average acceleration in box
                if analysis == 'acceleration':
                    yz_values[i][j] = calc_avg_acc(mini_tracks, min_track_len)
                
                # average angular velocity in box
                if analysis == 'ang_vel':
                    yz_values[i][j] = calc_avg_ang_vel(mini_tracks, min_track_len)
                
                # progress
                prog = func.progress(prog, tot_squares, start_time)
        
        # loop through XZ boxes
        for i in range(z_size):
            z = float(f'{(z_start + (size * i)):.2f}')
            for j in range(x_size):
                x = float(f'{(x_start + (size * j)):.2f}')
                
                # count mini-tracks in box
                box = (x, x + size), (y_start, y_end), (z, z + size)
                mini_tracks = valid(box, tot_tracks)
                
                # count of mini-tracks in box
                if analysis == 'count':
                    xz_values[i][j] = len(mini_tracks)
                
                # tortuosity in box
                if analysis == 'tortuosity':
                    xz_values[i][j] = calc_tortuosity(mini_tracks, min_track_len)
                
                # average time in box
                if analysis == 'avg_time':
                    xz_values[i][j] = calc_time_in(mini_tracks, 'avg')
                
                # total time in box
                if analysis == 'tot_time':
                    xz_values[i][j] = calc_time_in(mini_tracks, 'tot')
                
                # average velocity in box
                if analysis == 'velocity':
                    xz_values[i][j] = calc_avg_velocity(mini_tracks, min_track_len)
                
                # average acceleration in box
                if analysis == 'acceleration':
                    xz_values[i][j] = calc_avg_acc(mini_tracks, min_track_len)
                
                # average angular velocity in box
                if analysis == 'ang_vel':
                    xz_values[i][j] = calc_avg_ang_vel(mini_tracks, min_track_len)
                
                # progress
                prog = func.progress(prog, tot_squares, start_time)
        
        # generate heatmap and save plot
        print(f'creating {analysis} heatmap')
        heatmap_all(xy_values, yz_values, xz_values, analysis, text_labels, size, x_size, x_start, x_end, y_size,
                    y_start, y_end, z_size, z_start, z_end, path)
    
    # print total time
    print(f'Total Time: {func.time_format(start_time)}')
    
    return


""" ====== MODIFY UNDER HERE ====== """

"""	* chose the size of the squares and if there should be the text inside the squares
    * insert the path of the experiments
    * if necessary, adjust the area of the wind tunnel """

# main settings
analysis_type = ['count', 'tortuosity', 'tot_time', 'avg_time', 'velocity', 'acceleration', 'ang_vel']
size = 0.1
text_labels = True  # insert text labels in squares (True, False)
path = 'C:/manu/test'

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
