""" PANDAS PLOT FUNCTIONS """

# imports
import pandas as pd
import data.general_func as func
import numpy as np
import matplotlib.pyplot as plt
import os


# return a list of the tracks passing in a specific box
def valid(box_in, tot):
    founded = []
    for track in tot:
        # get box dimensions
        x_min_in, x_max_in = box_in[0]
        y_min_in, y_max_in = box_in[1]
        z_min_in, z_max_in = box_in[2]
        
        # check if passes in the box
        track['temp_box'] = 'no'
        track.loc[(track['X'] >= x_min_in) & (track['X'] <= x_max_in)
                  & (track['Y'] >= y_min_in) & (track['Y'] <= y_max_in)
                  & (track['Z'] >= z_min_in) & (track['Z'] <= z_max_in), 'temp_box'] = 'yes'
        
        # get tracks founded
        mini_found = track[track['temp_box'] == 'yes'].groupby((track['temp_box'] != 'yes').cumsum())
        for t in mini_found:
            founded.append(t)
    
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


# plotting function
def plot_xyz_single(vx, vy, vz, an_tp, sz, x_sz, x_st, x_end, y_sz, y_st, y_end, z_sz, z_st, z_end):
    # creating subplots
    fig, (ax, bx, cx) = plt.subplots(1, 3, sharey='row')
    
    # X plot
    ax.plot(vx)
    ax.set_title('X')
    ax.set_xticks(np.arange(x_sz))
    ax.set_xticklabels(f'{i:.1f}' for i in np.arange(x_st, x_end, sz))
    ax.xaxis.grid()
    
    # Y plot
    bx.plot(vy)
    bx.set_title('Y')
    bx.set_xticks(np.arange(y_sz))
    bx.set_xticklabels(f'{i:.1f}' for i in np.arange(y_st, y_end, sz))
    bx.xaxis.grid()
    
    # Z plot
    cx.plot(vz)
    cx.set_title('Z')
    cx.set_xticks(np.arange(z_sz))
    cx.set_xticklabels(f'{i:.1f}' for i in np.arange(z_st, z_end, sz))
    cx.xaxis.grid()
    
    # plotting
    fig.suptitle(an_tp.capitalize())
    plt.tight_layout()
    plt.show()


# plotting function
def plot_xyz_all(vx, vy, vz, an_tp, sz, x_sz, x_st, x_end, y_sz, y_st, y_end, z_sz, z_st, z_end, p):
    # creating subplots
    fig, (ax, bx, cx) = plt.subplots(1, 3, sharey='row')
    ax.plot(vx)
    bx.plot(vy)
    cx.plot(vz)
    
    # X plot
    ax.set_xticks(np.arange(x_sz))
    ax.set_xticklabels(f'{i:.1f}' for i in np.arange(x_st, x_end, sz))
    ax.xaxis.grid()
    
    # Y plot
    bx.set_xticks(np.arange(y_sz))
    bx.set_xticklabels(f'{i:.1f}' for i in np.arange(y_st, y_end, sz))
    bx.xaxis.grid()
    
    # Z plot
    cx.set_xticks(np.arange(z_sz))
    cx.set_xticklabels(f'{i:.1f}' for i in np.arange(z_st, z_end, sz))
    cx.xaxis.grid()
    
    # plotting
    fig.suptitle(an_tp.capitalize(), size=36)
    ax.set_title('X')
    bx.set_title('Y')
    cx.set_title('Z')
    plt.tight_layout()
    
    # save plot
    fig.set_size_inches(32, 18)
    save_path = os.path.join(p, 'variables_graphs')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    plt.savefig(f'{save_path}\\{an_tp}.jpg', dpi=300)
