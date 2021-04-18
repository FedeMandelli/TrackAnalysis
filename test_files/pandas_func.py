""" pandas functions """

# imports
import pandas as pd
from math import sqrt, acos, pi
from time import perf_counter

""" === Functions === """


def get_tracks_pandas(file, exp):
    """ load a give .csv file in a pandas dataframe, reformat and delete the columns accordingly to the user specific
    needs and remove the useless data.
    The useless tracks are defined as:
        * less than 25 points
        * recorded for less than 0.5 seconds
        * all the points are in a 1cm*1cm*1cm cube """
    
    def usable(tr):
        """ check if the track is usable or not based on the define conditions """
        # check total points
        if len(tr) <= 26:
            return False
        
        # check total time
        if tr['time'].max() - tr['time'].min() <= 0.5:
            return False
        
        # check if all points in 1cm
        x_move = tr['X'].max() - tr['X'].min()
        y_move = tr['Y'].max() - tr['Y'].min()
        z_move = tr['Z'].max() - tr['Z'].min()
        if max(x_move, y_move, z_move) <= 0.01:
            return False
        
        # return True if all good
        return True
    
    # load dataframe and remove, rename and insert columns for easier coding
    tracks_df = pd.read_csv(file, sep=';')
    tracks_df.rename(columns={'XSplined': 'X', 'YSplined': 'Y', 'ZSplined': 'Z'}, inplace=True)
    tracks_df.drop(columns=['VXSplined', 'VYSplined', 'VZSplined'], inplace=True)
    tracks_df.dropna(inplace=True)
    tracks_df.insert(0, 'experiment', exp)
    
    # clean useless tracks
    grouped_df = tracks_df.groupby('object')
    removed = []
    valid_tracks = []
    for num, data in grouped_df:
        if not usable(data):
            removed.append(str(num))
        else:
            valid_tracks.append(data)
    
    # reformat removed tracks information
    r_info = ', '.join(removed) if len(removed) > 0 else 'None'
    
    # general info
    info = pd.DataFrame(data=[{'experiment': exp,
                               'total': len(grouped_df),
                               'valid': len(valid_tracks),
                               'removed': len(removed),
                               'tracks removed (n.)': r_info}])
    
    # return the information
    return valid_tracks, info


def check_box(box, p):
    """ given a box and a point, check if the point is inside the box """
    
    # get box dimensions
    x_min, x_max = box[0]
    y_min, y_max = box[1]
    z_min, z_max = box[2]
    
    # check if in the box
    if x_min <= p['X'] <= x_max \
            and y_min <= p['Y'] <= y_max \
            and z_min <= p['Z'] <= z_max:
        return True
    
    # return not in the box
    return False


def format_fl(num):
    """ reformat the given number in a string with 3 decimals """
    
    return float(f'{num:.3f}')


def two_pt_dist(first, last):
    """ return the distance between two points in a 3D space """
    
    return sqrt((last['X'] - first['X']) ** 2 + (last['Y'] - first['Y']) ** 2 + (last['Z'] - first['Z']) ** 2)


def two_pt_speed(first, last):
    """ return the speed between two points in a 3D space """
    
    dist = two_pt_dist(first, last)
    time = last['time'] - first['time']
    speed = dist / time
    
    return speed


def calc_dist(tr):
    """ given a track, return the total distance, the linear distance and a dictionary with the same information
     for the XYZ axis """
    
    # 3D distance
    dist_tot = 0
    for i in range(1, len(tr)):
        d = two_pt_dist(tr.iloc[i - 1], tr.iloc[i])
        dist_tot += d
    dist_tot = format_fl(dist_tot)
    dist_lin = format_fl(two_pt_dist(tr.iloc[0], tr.iloc[-1]))
    
    # X distance
    tot_x = 0
    for i in range(1, len(tr)):
        tot_x += abs(tr.iloc[i]['X'] - tr.iloc[i - 1]['X'])
    tot_x = format_fl(tot_x)
    lin_x = format_fl(tr.iloc[-1]['X'] - tr.iloc[0]['X'])
    
    # Y distance
    tot_y = 0
    for i in range(1, len(tr)):
        tot_y += abs(tr.iloc[i]['Y'] - tr.iloc[i - 1]['Y'])
    tot_y = format_fl(tot_y)
    lin_y = format_fl(tr.iloc[-1]['Y'] - tr.iloc[0]['Y'])
    
    # Z distance
    tot_z = 0
    for i in range(1, len(tr)):
        tot_z += abs(tr.iloc[i]['Z'] - tr.iloc[i - 1]['Z'])
    tot_z = format_fl(tot_z)
    lin_z = format_fl(tr.iloc[-1]['Z'] - tr.iloc[0]['Z'])
    
    return dist_tot, dist_lin, {'Xtot': tot_x, 'Xlin': lin_x, 'Ytot': tot_y, 'Ylin': lin_y, 'Ztot': tot_z,
                                'Zlin': lin_z}


def calc_acc(tr):
    """ given a track, return the average acceleration """
    
    # get all speeds
    speeds = []
    for i in range(1, len(tr)):
        speed = two_pt_speed(tr.iloc[i - 1], tr.iloc[i])
        time = tr.iloc[i]['time']
        speeds.append((speed, time))
    
    # get all accelerations
    accelerations = []
    for i in range(1, len(speeds)):
        diff_speed = speeds[i][0] - speeds[i - 1][0]
        diff_time = speeds[i][1] - speeds[i - 1][1]
        acc = diff_speed / diff_time
        accelerations.append(acc)
    
    # mean acceleration
    mean_acc = format_fl(sum(accelerations) / len(accelerations))
    
    return mean_acc


def ang_vel(tr):
    """ given a track, return the average angular velocity """
    
    # get all speeds in XYZ
    speeds = []
    for i in range(1, len(tr)):
        first = tr.iloc[i - 1]
        last = tr.iloc[i]
        delta_t = last['time'] - first['time']
        vx = (last['X'] - first['X']) / delta_t
        vy = (last['Y'] - first['Y']) / delta_t
        vz = (last['Z'] - first['Z']) / delta_t
        time = tr.iloc[i]['time']
        speeds.append({'vx': vx, 'vy': vy, 'vz': vz, 'time': time})
    
    # angular velocity
    ang_vel_tot = []
    for i in range(1, len(speeds)):
        first = speeds[i - 1]
        last = speeds[i]
        den_deltat = format_fl(last['time'] - first['time'])
        num_prod_scal = (first['vx'] * last['vx']) + (first['vy'] * last['vy']) + (first['vz'] * last['vz'])
        num_vel = (sqrt((first['vx'] ** 2) + (first['vy'] ** 2) + (first['vz'] ** 2))) * \
                  (sqrt((last['vx'] ** 2) + (last['vy'] ** 2) + (last['vz'] ** 2)))
        
        if num_vel == 0:
            vel_ang = 0
        else:
            delta_angle = acos(format_fl(num_prod_scal / num_vel))
            delta_angle = delta_angle * 180 / pi
            vel_ang = format_fl(delta_angle / den_deltat)
        
        ang_vel_tot.append(vel_ang)
    
    # average
    avg_ang_vel = format_fl(sum(ang_vel_tot) / len(ang_vel_tot))
    
    return avg_ang_vel


def land_still(tr):
    """ check if in any point of the given track, the mosquito is landed or is still """
    
    # counting settings
    counting = False
    count = 0
    tol = 0.002
    landed = {}
    still = []
    
    # difference between two points
    for i in range(1, len(tr)):
        first_p = tr.iloc[i - 1]
        last_p = tr.iloc[i]
        
        # check if next point is in tolerance
        if first_p['X'] - tol <= last_p['X'] <= first_p['X'] + tol \
                and first_p['Y'] - tol <= last_p['Y'] <= first_p['Y'] + tol \
                and first_p['Z'] - tol <= last_p['Z'] <= first_p['Z'] + tol:
            counting = True
        else:
            counting = False
        
        # manage counting
        if counting:
            count += 1
        else:
            # still in the middle of the track
            if count >= 5:
                still.append({'X': tr.iloc[i]["X"], 'Y': tr.iloc[i]["Y"], 'Z': tr.iloc[i]["Z"], 'count': count})
            count = 0
    
    # landed at the end of the track
    if counting and count >= 5:
        landed = {'X': tr.iloc[-1]["X"], 'Y': tr.iloc[-1]["Y"], 'Z': tr.iloc[-1]["Z"], 'count': count}
    
    # return info
    return landed, still


def to_excel(df, sheet_name, writer):
    """ export a pandas dataframe in a table in a given excel sheet """
    
    # create sheet with dataframe
    df.to_excel(writer, sheet_name=sheet_name, startrow=1, header=False, index=False)
    worksheet = writer.sheets[sheet_name]
    
    # get columns settings
    col_set = [{'header': column} for column in df.columns]
    max_row, max_col = df.shape
    
    # create and insert the table
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': col_set})
    
    # change the width of the columns
    for i, col in enumerate(df.columns):
        column_len = max(df[col].astype(str).str.len().max(), len(col) + 2)
        worksheet.set_column(i, i, column_len)
    
    # create hidden sheet for plot3D
    if sheet_name == 'Points':
        df.to_excel(writer, sheet_name='3D_data', index=False)
        writer.sheets['3D_data'].hide()
    
    return


""" === Main Analysis === """


def box_analysis(tracks, exp_info, box_in, box_out):
    """ given a list of tracks (organized in a pandas dataframe) and an area represented as a box with XYZ coordinates,
    return three pandas dataframes with the analysis of the single tracks, the minitracks in the box and a general
    recap of all the experiment information """
    
    # create dataframes and general information dictionary
    tracks_df = pd.DataFrame()
    minitracks_df = pd.DataFrame()
    minitracks = []
    general_info = {'mini tracks': 0,
                    'unique tracks': 0,
                    'tot time': 0,
                    'tot dist': 0,
                    'landed': ''}
    
    """ === Track Analysis === """
    for track in tracks:
        track['type'] = 'track'
        track['landed'] = 'no'
        
        # check if in passes in the desired area
        x_min_in, x_max_in = box_in[0]
        y_min_in, y_max_in = box_in[1]
        z_min_in, z_max_in = box_in[2]
        x_min_out, x_max_out = box_out[0]
        y_min_out, y_max_out = box_out[1]
        z_min_out, z_max_out = box_out[2]
        
        track['in_box'] = 'no'
        track.loc[((track['X'] >= x_min_in) & (track['X'] <= x_max_in)
                   & (track['Y'] >= y_min_in) & (track['Y'] <= y_max_in)
                   & (track['Z'] >= z_min_in) & (track['Z'] <= z_max_in))
                  & ~((track['X'] >= x_min_out) & (track['X'] <= x_max_out)
                      & (track['Y'] >= y_min_out) & (track['Y'] <= y_max_out)
                      & (track['Z'] >= z_min_out) & (track['Z'] <= z_max_out)), 'in_box'] = 'yes'
        
        # track information
        box_pass = 'yes' if 'yes' in track['in_box'].values else 'no'
        points = track['object'].count()
        tot_time = track['time'].max() - track['time'].min()
        track_info = {'experiment': track.iloc[0]['experiment'],
                      'n. track': track.iloc[0]['object'],
                      'points': points,
                      'tot time': tot_time,
                      'in box': box_pass,
                      'landing': '',
                      'still': ''}
        
        # land or still
        land_info, still_info = land_still(track)
        if land_info:
            if check_box(box_in, land_info):
                track['landed'] = 'yes'
                mini_land = f'x{land_info["X"]}, y{land_info["Y"]}, z{land_info["Z"]}, {land_info["count"]}p'
                track_info['landing'] = mini_land
                if general_info['landed'] != '':
                    gil = ', '.join([general_info['landed'], str(track.iloc[0]['object'])])
                else:
                    gil = str(track.iloc[0]['object'])
                general_info['landed'] = gil
        if still_info:
            still_list = []
            for p in still_info:
                if check_box(box_in, p):
                    still_list.append(f'x{p["X"]}, y{p["Y"]}, z{p["Z"]}, {p["count"]}p')
            mini_still = ' - '.join(still_list)
            track_info['still'] = mini_still
        
        """ === Mini Tracks Analysis === """
        if box_pass == 'yes':
            general_info['unique tracks'] += 1
            
            # group points in box creating mini-tracks
            in_box_df = track[track['in_box'] == 'yes'].groupby((track['in_box'] != 'yes').cumsum())
            n_minitracks = len(in_box_df)
            track_info['minitracks'] = n_minitracks
            
            # loop minitracks
            count = 0
            for mini_i, minitrack_data in in_box_df:
                general_info['mini tracks'] += 1
                minitrack_data['type'] = 'minitrack'
                minitracks.append(minitrack_data)
                # general information
                count += 1
                minitrack_info = {'n. track': minitrack_data.iloc[0]['object'],
                                  'n. mini-track': f'{count} of {n_minitracks}',
                                  'points': len(minitrack_data)}
                
                # analysis needed if there's more than 2 positions in the box
                if len(minitrack_data) > 2:
                    # time calculations
                    time_start = minitrack_data['time'].min()
                    time_end = minitrack_data['time'].max()
                    time_in = format_fl(time_end - time_start)
                    general_info['tot time'] += time_in
                    minitrack_info['time in box'] = time_in
                    
                    # distance calculations
                    distance_tot, distance_lin, axis_dist = calc_dist(minitrack_data)
                    general_info['tot dist'] += distance_tot
                    minitrack_info['3D tot dist'] = distance_tot
                    minitrack_info['3D lin dist'] = distance_lin
                    
                    minitrack_info['X tot dist'] = axis_dist['Xtot']
                    minitrack_info['X lin dist'] = axis_dist['Xlin']
                    minitrack_info['X lin dist abs'] = abs(axis_dist['Xlin'])
                    
                    minitrack_info['Y tot dist'] = axis_dist['Ytot']
                    minitrack_info['Y lin dist'] = axis_dist['Ylin']
                    minitrack_info['Y lin dist abs'] = abs(axis_dist['Ylin'])
                    
                    minitrack_info['Z tot dist'] = axis_dist['Ztot']
                    minitrack_info['Z lin dist'] = axis_dist['Zlin']
                    minitrack_info['Z lin dist abs'] = abs(axis_dist['Zlin'])
                    
                    # tortuosity
                    try:
                        minitrack_info['3D tortuosity'] = format_fl(abs(distance_lin / distance_tot))
                    except ZeroDivisionError:
                        pass
                    try:
                        minitrack_info['X tortuosity'] = format_fl(abs(axis_dist['Xlin'] / axis_dist['Xtot']))
                    except ZeroDivisionError:
                        pass
                    try:
                        minitrack_info['Y tortuosity'] = format_fl(abs(axis_dist['Ylin'] / axis_dist['Ytot']))
                    except ZeroDivisionError:
                        pass
                    try:
                        minitrack_info['Z tortuosity'] = format_fl(abs(axis_dist['Zlin'] / axis_dist['Ztot']))
                    except ZeroDivisionError:
                        pass
                    
                    # flight speed calculation
                    mean_speed = format_fl(distance_tot / time_in)
                    minitrack_info['flight speed (m/s)'] = mean_speed
                    first = minitrack_data.iloc[0]
                    last = minitrack_data.iloc[-1]
                    
                    mean_x_speed = format_fl((last['X'] - first['X']) / time_in)
                    minitrack_info['X flight speed (m/s)'] = mean_x_speed
                    
                    mean_y_speed = format_fl((last['Y'] - first['Y']) / time_in)
                    minitrack_info['Y flight speed (m/s)'] = mean_y_speed
                    
                    mean_z_speed = format_fl((last['Z'] - first['Z']) / time_in)
                    minitrack_info['Z flight speed (m/s)'] = mean_z_speed
                    
                    # acceleration
                    mean_acc = calc_acc(minitrack_data)
                    minitrack_info['acceleration (m/s2)'] = mean_acc
                    
                    # angular velocity
                    mean_ang_vel = ang_vel(minitrack_data)
                    minitrack_info['angular velocity'] = mean_ang_vel
                
                # landing or still information
                minitrack_info['landing'] = track_info['landing']
                minitrack_info['still'] = track_info['still']
                
                # combine minitracks information
                minitracks_df = minitracks_df.append([minitrack_info], ignore_index=True)
        
        # combine tracks information
        tracks_df = tracks_df.append([track_info], ignore_index=True)
    
    """ === Plot 3D Data === """
    points_df = pd.concat(tracks + minitracks, ignore_index=True)
    
    """ === Experiment Information and Return === """
    # update experiment info
    for i in general_info:
        exp_info[i] = general_info[i]
    
    # move number of tracks removed to the end
    tracks_removed = exp_info.pop('tracks removed (n.)')
    exp_info.insert(len(exp_info.columns), 'tracks removed (n.)', tracks_removed)
    
    # return
    return tracks_df, minitracks_df, exp_info, points_df
