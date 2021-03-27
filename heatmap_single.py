""" HEATMAP SINGLE """

# imports
from data.hm_func import *


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
    tot_squares = (x_size * y_size) + (y_size * z_size) + (x_size * z_size)
    prog = 0
    start_time = perf_counter()
    
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
            if analysis_type == 'count':
                xy_values[i][j] = len(mini_tracks)
            
            # tortuosity in box
            if analysis_type == 'tortuosity':
                xy_values[i][j] = calc_tortuosity(mini_tracks, min_track_len)
            
            # average time in box
            if analysis_type == 'avg_time':
                xy_values[i][j] = calc_time_in(mini_tracks, 'avg')
            
            # total time in box
            if analysis_type == 'tot_time':
                xy_values[i][j] = calc_time_in(mini_tracks, 'tot')
            
            # average velocity in box
            if analysis_type == 'velocity':
                xy_values[i][j] = calc_avg_velocity(mini_tracks, min_track_len)
            
            # average acceleration in box
            if analysis_type == 'acceleration':
                xy_values[i][j] = calc_avg_acc(mini_tracks, min_track_len)
            
            # average angular velocity in box
            if analysis_type == 'ang_vel':
                xy_values[i][j] = calc_avg_ang_vel(mini_tracks, min_track_len)
            
            # progress
            prog = progress(prog, tot_squares, start_time)
    
    # loop through YZ boxes
    for i in range(z_size):
        z = float(f'{(z_start + (size * i)):.2f}')
        for j in range(y_size):
            y = float(f'{(y_start + (size * j)):.2f}')
            
            # count mini-tracks in box
            box = (x_start, x_end), (y, y + size), (z, z + size)
            mini_tracks = valid(box, tot_tracks)
            
            # count of mini-tracks in box
            if analysis_type == 'count':
                yz_values[i][j] = len(mini_tracks)
            
            # tortuosity in box
            if analysis_type == 'tortuosity':
                yz_values[i][j] = calc_tortuosity(mini_tracks, min_track_len)
            
            # average time in box
            if analysis_type == 'avg_time':
                yz_values[i][j] = calc_time_in(mini_tracks, 'avg')
            
            # total time in box
            if analysis_type == 'tot_time':
                yz_values[i][j] = calc_time_in(mini_tracks, 'tot')
            
            # average velocity in box
            if analysis_type == 'velocity':
                yz_values[i][j] = calc_avg_velocity(mini_tracks, min_track_len)
            
            # average acceleration in box
            if analysis_type == 'acceleration':
                yz_values[i][j] = calc_avg_acc(mini_tracks, min_track_len)
            
            # average angular velocity in box
            if analysis_type == 'ang_vel':
                yz_values[i][j] = calc_avg_ang_vel(mini_tracks, min_track_len)
            
            # progress
            prog = progress(prog, tot_squares, start_time)
    
    # loop through XZ boxes
    for i in range(z_size):
        z = float(f'{(z_start + (size * i)):.2f}')
        for j in range(x_size):
            x = float(f'{(x_start + (size * j)):.2f}')
            
            # count mini-tracks in box
            box = (x, x + size), (y_start, y_end), (z, z + size)
            mini_tracks = valid(box, tot_tracks)
            
            # count of mini-tracks in box
            if analysis_type == 'count':
                xz_values[i][j] = len(mini_tracks)
            
            # tortuosity in box
            if analysis_type == 'tortuosity':
                xz_values[i][j] = calc_tortuosity(mini_tracks, min_track_len)
            
            # average time in box
            if analysis_type == 'avg_time':
                xz_values[i][j] = calc_time_in(mini_tracks, 'avg')
            
            # total time in box
            if analysis_type == 'tot_time':
                xz_values[i][j] = calc_time_in(mini_tracks, 'tot')
            
            # average velocity in box
            if analysis_type == 'velocity':
                xz_values[i][j] = calc_avg_velocity(mini_tracks, min_track_len)
            
            # average acceleration in box
            if analysis_type == 'acceleration':
                xz_values[i][j] = calc_avg_acc(mini_tracks, min_track_len)
            
            # average angular velocity in box
            if analysis_type == 'ang_vel':
                xz_values[i][j] = calc_avg_ang_vel(mini_tracks, min_track_len)
            
            # progress
            prog = progress(prog, tot_squares, start_time)
    
    # print total time
    print(f'Total Time: {time_format(start_time)}')
    
    # generate heatmap
    heatmap_single(xy_values, yz_values, xz_values, analysis_type, text_labels, size, x_size, x_start, x_end, y_size,
                   y_start, y_end, z_size, z_start, z_end)
    
    return


""" ****** MODIFY UNDER HERE ****** """

"""	* insert the path of the experiments
    * chose the type of analysis to be performed
    * chose the size of the squares and if there should be the text inside the squares
    * if necessary, adjust the area of the wind tunnel needed """

# main settings
path = 'C:\\manu\\Varie\\test'
analysis_type = 'count'  # count - tortuosity - avg_time - tot_time - velocity - acceleration - ang_vel
size = 0.1
text_labels = True  # insert text labels in squares (True, False)

# XYZ settings - default: S(0.1) X(-0.1, 1) Y(-0.3, 1.7) Z(-0.1, 1.2)
x_start = -0.1
x_end = 1
y_start = -0.3
y_end = 1.7
z_start = -0.1
z_end = 1.2

""" ****** LAUNCH PROGRAM ****** """
if __name__ == '__main__':
    main()
