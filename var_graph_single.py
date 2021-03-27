""" VARIABLE ANALYSIS SINGLE """

# imports
import data.general_func as func
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from time import perf_counter


# main function
def main():
    # return a list of the tracks passing in a specific box
    def valid(box_in, tot):
        def check_box(box_test, p):
            x_min, x_max = box_test[0]
            y_min, y_max = box_test[1]
            z_min, z_max = box_test[2]
            if x_min <= p['X'] <= x_max and y_min <= p['Y'] <= y_max and z_min <= p['Z'] <= z_max:
                return True
            return False
        
        # settings
        founded = []
        counting = False
        count = -1
        
        # check if the position is in the desired area
        for track in tot:
            for pos in track:
                if check_box(box_in, pos):
                    # if it's the start of a new track, create the relative list,
                    # increase the count, set counting to True
                    if not counting:
                        founded.append([])
                        count += 1
                        counting = True
                    founded[count].append(pos)
                else:
                    if counting:
                        counting = False
            counting = False
        
        return founded
    
    # return the average tortuosity
    def calc_tortuosity(tracks):
        tot_tort = []
        for track in tracks:
            # clean still points
            for pos in func.land_still(track, True):
                track.remove(pos)
            
            # calculations
            if len(track) >= min_track_len:
                
                # total distance
                dist_tot = 0
                for i in range(1, len(track)):
                    dist = func.two_pt_dist(track[i - 1], track[i])
                    dist_tot += dist
                dist_tot = func.format_fl(dist_tot)
                
                # linear distance
                dist_lin = func.format_fl(func.two_pt_dist(track[0], track[-1]))
                
                # tortuosity
                try:
                    tort = func.format_fl(abs(dist_lin / dist_tot))
                    tot_tort.append(tort)
                except ZeroDivisionError:
                    print(track[0])
        
        # average tortuosity
        if len(tot_tort) > 0:
            avg_tort = func.format_fl(sum(tot_tort) / len(tot_tort))
        else:
            avg_tort = np.nan
        
        return avg_tort
    
    # return the average and the total time spent in a box
    def calc_time_in(tracks, type_t):
        time_tot = []
        for track in tracks:
            # time in the box
            start = track[0]['time']
            end = track[-1]['time']
            time_in = func.format_fl(end - start)
            time_tot.append(time_in)
        
        # average time
        if type_t == 'avg':
            try:
                time_avg = func.format_fl(sum(time_tot) / len(time_tot))
            except ZeroDivisionError:
                time_avg = np.nan
            return time_avg
        
        # total time
        else:
            if len(time_tot) == 0:
                time_tot = np.nan
            else:
                time_tot = func.format_fl(sum(time_tot))
            return time_tot
    
    # return the average velocity
    def calc_avg_velocity(tracks):
        means = []
        for track in tracks:
            if len(track) >= min_track_len:
                
                # time in
                start_time = track[0]['time']
                end_time = track[-1]['time']
                time_in = func.format_fl(end_time - start_time)
                
                # distance 3D
                dist_tot = 0
                for i in range(1, len(track)):
                    dist = func.two_pt_dist(track[i - 1], track[i])
                    dist_tot += dist
                dist_tot = func.format_fl(dist_tot)
                
                # velocity
                mean_velocity = func.format_fl(dist_tot / time_in)
                means.append(mean_velocity)
        
        # average
        if len(means) == 0:
            avg_veloc = np.nan
        else:
            avg_veloc = func.format_fl(sum(means) / len(means))
        
        return avg_veloc
    
    # return the average acceleration
    def calc_avg_acc(tracks):
        means = []
        
        # get mean acceleration for all tracks
        for track in tracks:
            if len(track) >= min_track_len:
                means.append(func.calc_acc(track))
        
        # average
        if len(means) == 0:
            mean_acc = np.nan
        else:
            mean_acc = func.format_fl(sum(means) / len(means))
        
        return mean_acc
    
    # return the average angular velocity
    def calc_avg_ang_vel(tracks):
        means = []
        
        # get mean angular velocity for all tracks
        for track in tracks:
            if len(track) >= min_track_len:
                means.append(func.ang_vel(track))
        
        # average
        if len(means) == 0:
            mean_ang_vel = np.nan
        else:
            mean_ang_vel = int(sum(means) / len(means))
        
        return mean_ang_vel
    
    # plotting function
    def plot_xyz(vx, vy, vz):
        # creating subplots
        fig, (ax, bx, cx) = plt.subplots(1, 3, sharey='row')
        
        # X plot
        ax.plot(vx)
        ax.set_title('X')
        ax.set_xticks(np.arange(x_size))
        ax.set_xticklabels(f'{i:.1f}' for i in np.arange(x_start, x_end, size))
        ax.xaxis.grid()
        
        # Y plot
        bx.plot(vy)
        bx.set_title('Y')
        bx.set_xticks(np.arange(y_size))
        bx.set_xticklabels(f'{i:.1f}' for i in np.arange(y_start, y_end, size))
        bx.xaxis.grid()
        
        # Z plot
        cx.plot(vz)
        cx.set_title('Z')
        cx.set_xticks(np.arange(z_size))
        cx.set_xticklabels(f'{i:.1f}' for i in np.arange(z_start, z_end, size))
        cx.xaxis.grid()
        
        # plotting
        fig.suptitle(analysis_type.capitalize())
        plt.tight_layout()
        print(f'time: {(perf_counter() - start_timer):.3f}s')
        plt.show()
    
    # progress of the analysis
    def progress(prog):
        # update count
        prog += 1
        
        # get time information
        up_now = perf_counter() - start_analysis
        for_exp = up_now / prog
        for_remaining = int(for_exp * (tot_val - prog))
        
        # format time information
        if for_remaining >= 60:
            time_left = f'{int(for_remaining // 60)}m{int((for_remaining - (for_remaining // 60 * 60)) % 60)}s'
        else:
            time_left = f'{for_remaining}s'
        
        # percentage
        perc = f"{(prog / tot_val * 100):.2f}%"
        print(f'{perc} - {prog}\\{tot_val} - time to end: {time_left}')
        return prog
    
    """ main start """
    # main settings
    tot_tracks = []
    min_track_len = 3
    
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
    
    # create basic list of values for each axes
    x_val = [0 for _ in range(x_size)]
    y_val = [0 for _ in range(y_size)]
    z_val = [0 for _ in range(z_size)]
    
    # progress check
    tot_val = sum([x_size, y_size, z_size])
    prog = 0
    start_analysis = perf_counter()
    
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
            x_val[i] = calc_tortuosity(mini_tracks)
        
        # tot time in box
        if analysis_type == 'tot_time':
            x_val[i] = calc_time_in(mini_tracks, 'tot')
        
        # avg time in box
        if analysis_type == 'avg_time':
            x_val[i] = calc_time_in(mini_tracks, 'avg')
        
        # average velocity in box
        if analysis_type == 'velocity':
            x_val[i] = calc_avg_velocity(mini_tracks)
        
        # average acceleration in box
        if analysis_type == 'acceleration':
            x_val[i] = calc_avg_acc(mini_tracks)
        
        # average angular velocity in box
        if analysis_type == 'ang_vel':
            x_val[i] = calc_avg_ang_vel(mini_tracks)
        
        # progress
        prog = progress(prog)
    
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
            y_val[i] = calc_tortuosity(mini_tracks)
        
        # tot time in box
        if analysis_type == 'tot_time':
            y_val[i] = calc_time_in(mini_tracks, 'tot')
        
        # avg time in box
        if analysis_type == 'avg_time':
            y_val[i] = calc_time_in(mini_tracks, 'avg')
        
        # average velocity in box
        if analysis_type == 'velocity':
            y_val[i] = calc_avg_velocity(mini_tracks)
        
        # average acceleration in box
        if analysis_type == 'acceleration':
            y_val[i] = calc_avg_acc(mini_tracks)
        
        # average angular velocity in box
        if analysis_type == 'ang_vel':
            y_val[i] = calc_avg_ang_vel(mini_tracks)
        
        # progress
        prog = progress(prog)
    
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
            z_val[i] = calc_tortuosity(mini_tracks)
        
        # tot time in box
        if analysis_type == 'tot_time':
            z_val[i] = calc_time_in(mini_tracks, 'tot')
        
        # avg time in box
        if analysis_type == 'avg_time':
            z_val[i] = calc_time_in(mini_tracks, 'avg')
        
        # average velocity in box
        if analysis_type == 'velocity':
            z_val[i] = calc_avg_velocity(mini_tracks)
        
        # average acceleration in box
        if analysis_type == 'acceleration':
            z_val[i] = calc_avg_acc(mini_tracks)
        
        # average angular velocity in box
        if analysis_type == 'ang_vel':
            z_val[i] = calc_avg_ang_vel(mini_tracks)
        
        # progress
        prog = progress(prog)
    
    # plot the results
    plot_xyz(x_val, y_val, z_val)
    
    # main return
    return


""" * Settings * """
# analysis settings
analysis_type = 'count'  # analysis type (count, tortuosity, tot_time, avg_time, velocity, acceleration, ang_vel)
size = 0.1

# path settings
splined = False
if splined:
    path = 'C:\\manu\\Varie\\test'
else:
    track_type = 'landed'  # type of track (landed, not landed, mini-tracks)
    path_1 = "C:\\manu\\Varie\\test\\land_or_not_large1.json"
    # path_2 = "C:\\manu\\Varie\\test\\land_or_not_large_2.json"
    path_list = [path_1]
    num_track = []  # insert number if you want to analyze the single track

# XYZ settings - default: X(-0.1, 1) Y(-0.3, 1.7) Z(-0.1, 1.2)
x_start = -0.1
x_end = 1
y_start = 0.7
y_end = 1.7
z_start = -0.1
z_end = 1.2
x_size = int((x_end - x_start) / size)
y_size = int((y_end - y_start) / size)
z_size = int((z_end - z_start) / size)

""" * Launch Main * """
if __name__ == '__main__':
    start_timer = perf_counter()
    main()
