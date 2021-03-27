""" general functions """

# imports
import csv
import os
from math import sqrt, acos, pi
import matplotlib.pyplot as plt
import json


# return a list of tracks in a given .csv file, clean useless data and return a report of the tracks included
def get_tracks(file):
	def usable(tr):
		# check total points
		if len(track) <= 25:
			return False
		
		# check total time
		start = tr[0]['time']
		end = tr[-1]['time']
		diff = end - start
		if diff <= 0.5:
			return False
		
		return True
	
	# read file and create a dictionary
	csv_file = open(file)
	csv_dict = csv.DictReader(csv_file, delimiter=';')
	
	# create objects list
	obj = []
	count = 1
	for pos in csv_dict:
		# if the position is the first of a new track, create a list for the track and increase the count
		if int(pos['object']) == count:
			obj.append([])
			count += 1
		obj[count - 2].append(pos)
	
	# clear NaN points, rename XYZ columns, removed useless columns and converting values for easier coding
	for track in obj:
		to_remove = []
		for point in track:
			if point['time'] != 'NaN':
				point['time'] = float(point['time'])
				point['object'] = int(point['object'])
				point['X'] = float(point.pop('XSplined'))
				point['Y'] = float(point.pop('YSplined'))
				point['Z'] = float(point.pop('ZSplined'))
				point.pop('VXSplined')
				point.pop('VYSplined')
				point.pop('VZSplined')
			else:
				to_remove.append(point)
		for i in to_remove:
			track.remove(i)
	
	# clean useless tracks
	removed = []
	for track in obj:
		if not usable(track):
			removed.append(str(track[0]['object']))
			obj.remove(track)
	if len(removed) > 0:
		r_info = ', '.join(removed)
	else:
		r_info = 'None'
	
	# general info
	total = int(obj[len(obj) - 1][0]['object'])
	valid_t = len(obj)
	removed = total - valid_t
	general = {'total': total, 'valid': valid_t, 'removed': removed, 'tracks removed (n.)': r_info}
	
	return obj, general


# check if a point is in a box or not
def check_box(box, p):
	x_min, x_max = box[0]
	y_min, y_max = box[1]
	z_min, z_max = box[2]
	if x_min <= p['X'] <= x_max and y_min <= p['Y'] <= y_max and z_min <= p['Z'] <= z_max:
		return True
	return False


# return a list of mini-tracks founded in a determined box
def valid(box_in, positions, box_not):
	# settings
	founded = []
	counting = False
	count = -1
	
	# check if the position is in the desired area
	for pos in positions:
		if check_box(box_in, pos) and not check_box(box_not, pos):
			# if it's the start of a new track, create the relative list, increase the count and set counting to True
			if not counting:
				founded.append([])
				count += 1
				counting = True
			founded[count].append(pos)
		else:
			if counting:
				counting = False
	
	return founded


# distance between two points in a 3D space
def two_pt_dist(first, last):
	return sqrt((last['X'] - first['X']) ** 2 + (last['Y'] - first['Y']) ** 2 + (last['Z'] - first['Z']) ** 2)


# speed between two 3D points
def two_pt_speed(first, last):
	dist = two_pt_dist(first, last)
	time = last['time'] - first['time']
	speed = dist / time
	return speed


# format float numbers with 3 decimals
def format_fl(num):
	return float(f'{num:.3f}')


# return total and linear distance for the whole track and for "X Y Z" axes
def calc_dist(tr):
	# total 3D distance
	dist_tot = 0
	for i in range(1, len(tr)):
		d = two_pt_dist(tr[i - 1], tr[i])
		dist_tot += d
	dist_tot = format_fl(dist_tot)
	
	# linear 3D distance
	dist_lin = format_fl(two_pt_dist(tr[0], tr[-1]))
	
	# X distance
	lin_x = format_fl(tr[-1]['X'] - tr[0]['X'])
	tot_x = 0
	for i in range(1, len(tr)):
		tot_x += abs(tr[i]['X'] - tr[i - 1]['X'])
	tot_x = format_fl(tot_x)
	
	# Y distance
	lin_y = format_fl(tr[-1]['Y'] - tr[0]['Y'])
	tot_y = 0
	for i in range(1, len(tr)):
		tot_y += abs(tr[i]['Y'] - tr[i - 1]['Y'])
	tot_y = format_fl(tot_y)
	
	# Z distance
	lin_z = format_fl(tr[-1]['Z'] - tr[0]['Z'])
	tot_z = 0
	for i in range(1, len(tr)):
		tot_z += abs(tr[i]['Z'] - tr[i - 1]['Z'])
	tot_z = format_fl(tot_z)
	
	return dist_tot, dist_lin, {'Xtot': tot_x, 'Xlin': lin_x, 'Ytot': tot_y, 'Ylin': lin_y, 'Ztot': tot_z,
								'Zlin': lin_z}


# return the average acceleration in the track
def calc_acc(tr):
	# get all speeds
	speeds = []
	for i in range(1, len(tr)):
		speed = two_pt_speed(tr[i - 1], tr[i])
		time = tr[i]['time']
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


# return the average angular velocity
def ang_vel(tr):
	# get all speeds in XYZ
	speeds = []
	for i in range(1, len(tr)):
		first = tr[i - 1]
		last = tr[i]
		delta_t = last['time'] - first['time']
		vx = (last['X'] - first['X']) / delta_t
		vy = (last['Y'] - first['Y']) / delta_t
		vz = (last['Z'] - first['Z']) / delta_t
		time = tr[i]['time']
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


# check if a mosquito has landed or is still
def land_still(tr, *args):
	# counting settings
	counting = False
	count = 0
	tol = 0.002
	landed = {}
	still = []
	tort_clean = []
	
	# difference between two points
	for i in range(1, len(tr)):
		first_p = tr[i - 1]
		last_p = tr[i]
		
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
				still.append({'X': tr[i]["X"], 'Y': tr[i]["Y"], 'Z': tr[i]["Z"], 'count': count})
				# get positions for tortuosity cleaning
				for pos in range(i - count, i):
					tort_clean.append(tr[pos])
			count = 0
	
	# landed at the end of the track
	if counting and count >= 5:
		landed = {'X': tr[-1]["X"], 'Y': tr[-1]["Y"], 'Z': tr[-1]["Z"], 'count': count}
		# get positions for tortuosity cleaning
		for pos in range(- count, -1):
			tort_clean.append(tr[pos])
	
	# return info or tortuosity
	if args:
		return tort_clean
	else:
		return landed, still


# plot speed
def plot_speed(tr, n_tr, n_min, path):
	# linear 3D speed
	linear = []
	for i in range(1, len(tr)):
		linear.append(two_pt_speed(tr[i - 1], tr[i]))
	
	# plot
	plt.plot(linear)
	plt.ylabel('speed')
	plt.xlabel('points')
	image_path = f'{path}\\track_{n_tr}_{n_min}.jpg'
	plt.tight_layout()
	plt.savefig(image_path)
	plt.close()
	
	return


# plot tracks in 3D
def plot_3d(tracks):
	ax = plt.axes(projection='3d')
	for track in tracks:
		x = []
		y = []
		z = []
		for point in track:
			x.append(point['X'])
			y.append(point['Y'])
			z.append(point['Z'])
			ax.plot3D(x, y, z)
	plt.tight_layout()
	plt.show()
	
	return


# export results in Py_Analysis folder
def export(exp):
	# create mini-tracks csv
	path = os.path.join(exp['folder'], f'{exp["date"]}_mini_tracks.csv')
	mini_tracks_csv = open(path, 'w', newline='')
	
	fieldnames = []
	for tr_info in exp['analysis']:
		if tr_info['n. points'] > 2:
			for field in tr_info:
				fieldnames.append(field)
			break
	
	writer = csv.DictWriter(mini_tracks_csv, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(exp['analysis'])
	
	# create general info csv
	path = os.path.join(exp['folder'], f'{exp["date"]}_general_info.csv')
	total_csv = open(path, 'w', newline='')
	
	fieldnames = []
	for field in exp['general info']:
		fieldnames.append(field)
	
	writer = csv.DictWriter(total_csv, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerow(exp['general info'])
	
	return


# create json file with landed or not landed tracks passing in box
def land_not(exp):
	exp['json'] = os.path.join(exp['folder'], f'{exp["date"]}_land_or_not.json')
	data = {'tracks': exp['tracks'],
			'mini-tracks': exp['mini-tracks'],
			'landed': exp['landed'],
			'not landed': exp['not landed']}
	with open(exp['json'], 'w') as jfile:
		json.dump(data, jfile)
	
	return


'''
*********************
* Main Box Analysis *
*********************
'''


def box_analysis(exp, box_in, box_out):
	# update general info e create analysis
	exp['general info']['mini-tracks'] = 0
	exp['general info']['unique tracks'] = 0
	exp['general info']['total time (sec)'] = 0
	exp['general info']['total distance (mt)'] = 0
	exp['general info']['landed'] = []
	exp['general info']['additional info'] = ''
	exp['analysis'] = []
	exp['mini-tracks'] = []
	in_box = []
	
	# cycle through tracks for box analysis
	for track in exp['tracks']:
		
		# check if passes in the box
		box_one_tracks = valid(box_in, track, box_out)
		if box_one_tracks:
			exp['general info']['unique tracks'] += 1
			in_box.append(track)
			
			# land or still
			land_info, still_info = land_still(track)
			
			mini_land = ''
			if land_info:
				if check_box(box_in, land_info):
					mini_land = f'x{land_info["X"]}, y{land_info["Y"]}, z{land_info["Z"]}, {land_info["count"]}p'
					exp['general info']['landed'].append(track[0]['object'])
			
			mini_still = ''
			if still_info:
				still_list = []
				for p in still_info:
					if check_box(box_in, p):
						still_list.append(f'x{p["X"]}, y{p["Y"]}, z{p["Z"]}, {p["count"]}p')
				mini_still = ' - '.join(still_list)
			
			# analyze data
			for mini_track in box_one_tracks:
				
				# general info
				exp['mini-tracks'].append(mini_track)
				num_track = mini_track[0]['object']
				num_found = box_one_tracks.index(mini_track) + 1
				num_tot = len(box_one_tracks)
				num_points = len(mini_track)
				track_info = {'n. track': num_track,
							  'n. mini-track': f'{num_found} of {num_tot}',
							  'n. points': num_points}
				exp['general info']['mini-tracks'] += 1
				
				# analysis needed if there's more than 1 position in the box
				if num_points > 2:
					
					# time calculations
					time_start = mini_track[0]['time']
					time_end = mini_track[-1]['time']
					time_in = format_fl(time_end - time_start)
					track_info['time in box (sec)'] = time_in
					exp['general info']['total time (sec)'] += time_in
					
					# distance calculations
					distance_tot, distance_lin, axis_dist = calc_dist(mini_track)
					track_info['3D total distance (mt)'] = distance_tot
					track_info['3D linear distance (mt)'] = distance_lin
					
					track_info['X total distance (mt)'] = axis_dist['Xtot']
					track_info['X linear distance (mt)'] = axis_dist['Xlin']
					track_info['X linear distance abs (mt)'] = abs(axis_dist['Xlin'])
					
					track_info['Y total distance (mt)'] = axis_dist['Ytot']
					track_info['Y linear distance (mt)'] = axis_dist['Ylin']
					track_info['Y linear distance abs (mt)'] = abs(axis_dist['Ylin'])
					
					track_info['Z total distance (mt)'] = axis_dist['Ztot']
					track_info['Z linear distance (mt)'] = axis_dist['Zlin']
					track_info['Z linear distance abs (mt)'] = abs(axis_dist['Zlin'])
					
					# tortuosity
					try:
						track_info['3D tortuosity'] = format_fl(abs(distance_lin / distance_tot))
					except ZeroDivisionError:
						pass
					try:
						track_info['X tortuosity'] = format_fl(abs(axis_dist['Xlin'] / axis_dist['Xtot']))
					except ZeroDivisionError:
						pass
					try:
						track_info['Y tortuosity'] = format_fl(abs(axis_dist['Ylin'] / axis_dist['Ytot']))
					except ZeroDivisionError:
						pass
					try:
						track_info['Z tortuosity'] = format_fl(abs(axis_dist['Zlin'] / axis_dist['Ztot']))
					except ZeroDivisionError:
						pass
					
					exp['general info']['total distance (mt)'] += distance_tot
					
					# flight speed calculation
					mean_speed = format_fl(distance_tot / time_in)
					track_info['flight speed (m/s)'] = mean_speed
					first = mini_track[0]
					last = mini_track[-1]
					
					mean_x_speed = format_fl((last['X'] - first['X']) / time_in)
					track_info['X flight speed (m/s)'] = mean_x_speed
					
					mean_y_speed = format_fl((last['Y'] - first['Y']) / time_in)
					track_info['Y flight speed (m/s)'] = mean_y_speed
					
					mean_z_speed = format_fl((last['Z'] - first['Z']) / time_in)
					track_info['Z flight speed (m/s)'] = mean_z_speed
					
					# acceleration
					mean_acc = calc_acc(mini_track)
					track_info['acceleration (m/s2)'] = mean_acc
					
					# angular velocity
					mean_ang_vel = ang_vel(mini_track)
					track_info['angular velocity'] = mean_ang_vel
				
				# info about landing
				track_info['landing'] = mini_land
				track_info['still'] = mini_still
				
				# plot speed
				# plot_speed(mini_track, num_track, num_found, exp['folder'])
				
				# append track info
				exp['analysis'].append(track_info)
				
				# additional info if multiple mini-tracks
				if len(box_one_tracks) > 1 and num_found == 1:
					if exp['general info']['additional info'][-6:] == 'passes':
						exp['general info']['additional info'] += ', '
					exp['general info']['additional info'] += f'Track {num_track} has {num_tot} passes'
	
	# manage landed tracks for json file
	exp['landed'] = []
	exp['not landed'] = []
	for track in in_box:
		if track[0]['object'] in exp['general info']['landed']:
			exp['landed'].append(track)
		else:
			exp['not landed'].append(track)
	
	# reformat information
	exp['general info']['total time (sec)'] = format_fl(exp['general info']['total time (sec)'])
	exp['general info']['total distance (mt)'] = format_fl(exp['general info']['total distance (mt)'])
	exp['general info']['landed'] = ', '.join(str(i) for i in exp['general info']['landed'])
	
	# plot minitracks
	# plot_3d(exp['mini-tracks'])
	
	return
