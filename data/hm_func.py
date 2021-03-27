""" heatmap functions"""

# imports
import data.general_func as func
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter
import os


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
                # if it's the start of a new track, create the relative list, increase the count, set counting to True
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
def calc_tortuosity(tracks, min_l):
    tot_tort = []
    for track in tracks:
        # clean still points
        for pos in func.land_still(track, True):
            track.remove(pos)
        
        # calculations
        if len(track) >= min_l:
            
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
def calc_avg_velocity(tracks, min_l):
    means = []
    for track in tracks:
        if len(track) >= min_l:
            
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
def calc_avg_acc(tracks, min_l):
    means = []
    
    # get mean acceleration for all tracks
    for track in tracks:
        if len(track) >= min_l:
            means.append(func.calc_acc(track))
    
    # average
    if len(means) == 0:
        mean_acc = np.nan
    else:
        mean_acc = func.format_fl(sum(means) / len(means))
    
    return mean_acc


# return the average angular velocity
def calc_avg_ang_vel(tracks, min_l):
    means = []
    
    # get mean angular velocity for all tracks
    for track in tracks:
        if len(track) >= min_l:
            means.append(func.ang_vel(track))
    
    # average
    if len(means) == 0:
        mean_ang_vel = np.nan
    else:
        mean_ang_vel = int(sum(means) / len(means))
    
    return mean_ang_vel


# clean outliers
def clean_outlers(xy, yz, xz, *args):
    if args:
        # get min-max values
        min_val = args[0]
        max_val = args[1]
        
        # xy
        for i in range(len(xy)):
            for j in range(len(xy[i])):
                if not min_val <= xy[i][j] <= max_val:
                    xy[i][j] = np.nan
        # yz
        for i in range(len(yz)):
            for j in range(len(yz[i])):
                if not min_val <= yz[i][j] <= max_val:
                    yz[i][j] = np.nan
        # xz
        for i in range(len(xz)):
            for j in range(len(xz[i])):
                if not min_val <= xz[i][j] <= max_val:
                    xz[i][j] = np.nan
    
    return xy, yz, xz


# progress of the analysis
def progress(p, tsq, start):
    # update count
    p += 1
    
    # get time information
    up_now = perf_counter() - start
    for_exp = up_now / p
    for_remaining = int(for_exp * (tsq - p))
    
    # format time information
    if for_remaining >= 60:
        time_left = f'{int(for_remaining // 60)}m{int((for_remaining - (for_remaining // 60 * 60)) % 60)}s'
    else:
        time_left = f'{for_remaining}s'
    
    # calc percentage and print
    perc = f"{(p / tsq * 100):.2f}%"
    print(f'{perc} - {p}\\{tsq} - time to end: {time_left}')
    
    # return
    return p


# calculate total time and format
def time_format(start):
    tot_time = perf_counter() - start
    tot_time_h = int(tot_time // 3600) if tot_time >= 3600 else 0
    tot_time_m = int((tot_time - (tot_time_h * 3600)) // 60) if tot_time >= 60 else 0
    tot_time_s = int(tot_time - (tot_time_h * 3600) - (tot_time_m * 60))
    time_stamp = f'{tot_time_h}h {tot_time_m}m {tot_time_s}s'
    return time_stamp


# create three heatmaps in XY, YZ ad XZ
def heatmap_single(val_xy, val_yz, val_xz, an_tp, txt_l, sz, x_sz, x_st, x_end, y_sz, y_st, y_end, z_sz, z_st, z_end):
    # filter values if needed
    val_xy, val_yz, val_xz = clean_outlers(val_xy, val_yz, val_xz)
    
    # convert values in numpy array
    val_xy = np.array(val_xy)
    val_yz = np.array(val_yz)
    val_xz = np.array(val_xz)
    
    # plot starting settings
    fig, (ax, bx, cx) = plt.subplots(1, 3)
    im_ax = ax.imshow(val_xy, cmap='jet', interpolation='nearest', origin='lower')
    im_bx = bx.imshow(val_yz, cmap='jet', interpolation='nearest', origin='lower')
    im_cx = cx.imshow(val_xz, cmap='jet', interpolation='nearest', origin='lower')
    
    # XY axes
    ax.set_xticks(np.arange(-.5, x_sz - 1))
    ax.set_xticklabels(f'{i:.2f}' for i in np.arange(x_st, x_end, sz))
    ax.set_yticks(np.arange(-.5, y_sz - 1))
    ax.set_yticklabels(f'{i:.2f}' for i in np.arange(y_st, y_end, sz))
    
    # YZ axes
    bx.set_xticks(np.arange(-.5, y_sz - 1))
    bx.set_xticklabels(f'{i:.2f}' for i in np.arange(y_st, y_end, sz))
    bx.set_yticks(np.arange(-.5, z_sz - 1))
    bx.set_yticklabels(f'{i:.2f}' for i in np.arange(z_st, z_end, sz))
    
    # XZ axes
    cx.set_xticks(np.arange(-.5, x_sz - 1))
    cx.set_xticklabels(f'{i:.2f}' for i in np.arange(x_st, x_end, sz))
    cx.set_yticks(np.arange(-.5, z_sz - 1))
    cx.set_yticklabels(f'{i:.2f}' for i in np.arange(z_st, z_end, sz))
    
    # text annotations
    if txt_l:
        # XY
        for i in range(y_sz):
            for j in range(x_sz):
                ax.text(j, i, val_xy[i, j], ha="center", va="center", color="w")
        # YZ
        for i in range(z_sz):
            for j in range(y_sz):
                bx.text(j, i, val_yz[i, j], ha="center", va="center", color="w")
        # XZ
        for i in range(z_sz):
            for j in range(x_sz):
                cx.text(j, i, val_xz[i, j], ha="center", va="center", color="w")
    
    # color bar
    ax.figure.colorbar(im_ax, ax=ax, orientation='horizontal')
    bx.figure.colorbar(im_bx, ax=bx, orientation='horizontal')
    cx.figure.colorbar(im_cx, ax=cx, orientation='horizontal')
    
    # plot
    fig.suptitle(an_tp.capitalize())
    ax.set_title('XY')
    bx.set_title('YZ')
    cx.set_title('XZ')
    fig.tight_layout()
    plt.show()


# create three heatmaps in XY, YZ ad XZ
def heatmap_all(val_xy, val_yz, val_xz, an_tp, txt_l, sz, x_sz, x_st, x_end, y_sz, y_st, y_end, z_sz, z_st, z_end, p):
    # filter values if needed
    val_xy, val_yz, val_xz = clean_outlers(val_xy, val_yz, val_xz)
    
    # convert values in numpy array
    val_xy = np.array(val_xy)
    val_yz = np.array(val_yz)
    val_xz = np.array(val_xz)
    
    # plot starting settings
    fig, (ax, bx, cx) = plt.subplots(1, 3)
    im_ax = ax.imshow(val_xy, cmap='jet', interpolation='nearest', origin='lower')
    im_bx = bx.imshow(val_yz, cmap='jet', interpolation='nearest', origin='lower')
    im_cx = cx.imshow(val_xz, cmap='jet', interpolation='nearest', origin='lower')
    
    # XY axes
    ax.set_xticks(np.arange(-.5, x_sz - 1))
    ax.set_xticklabels(f'{i:.2f}' for i in np.arange(x_st, x_end, sz))
    ax.set_yticks(np.arange(-.5, y_sz - 1))
    ax.set_yticklabels(f'{i:.2f}' for i in np.arange(y_st, y_end, sz))
    
    # YZ axes
    bx.set_xticks(np.arange(-.5, y_sz - 1))
    bx.set_xticklabels(f'{i:.2f}' for i in np.arange(y_st, y_end, sz))
    bx.set_yticks(np.arange(-.5, z_sz - 1))
    bx.set_yticklabels(f'{i:.2f}' for i in np.arange(z_st, z_end, sz))
    
    # XZ axes
    cx.set_xticks(np.arange(-.5, x_sz - 1))
    cx.set_xticklabels(f'{i:.2f}' for i in np.arange(x_st, x_end, sz))
    cx.set_yticks(np.arange(-.5, z_sz - 1))
    cx.set_yticklabels(f'{i:.2f}' for i in np.arange(z_st, z_end, sz))
    
    # text annotations
    if txt_l:
        # XY
        for i in range(y_sz):
            for j in range(x_sz):
                ax.text(j, i, val_xy[i, j], ha="center", va="center", color="w")
        # YZ
        for i in range(z_sz):
            for j in range(y_sz):
                bx.text(j, i, val_yz[i, j], ha="center", va="center", color="w")
        # XZ
        for i in range(z_sz):
            for j in range(x_sz):
                cx.text(j, i, val_xz[i, j], ha="center", va="center", color="w")
    
    # color bar
    ax.figure.colorbar(im_ax, ax=ax, orientation='horizontal')
    bx.figure.colorbar(im_bx, ax=bx, orientation='horizontal')
    cx.figure.colorbar(im_cx, ax=cx, orientation='horizontal')

    # plot
    fig.suptitle(an_tp.capitalize(), size=36)
    ax.set_title('XY')
    bx.set_title('YZ')
    cx.set_title('XZ')
    fig.tight_layout()
    
    # save plot
    fig.set_size_inches(32, 18)
    save_path = os.path.join(p, f'heatmaps_{sz * 100}cm')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(f'{save_path}\\{an_tp}.jpg', dpi=300)
