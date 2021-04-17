""" check unfiltered data for useful data and plot """

# imports
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

"""used to check if the points between z-0.04 and z0.1
and in the y zone of the trap where significant in number and position"""

# settings
path = 'C:\\manu\\Varie\\test'
# path = 'C:\\manu\\Varie\\postproc tracks'
x_values = []
y_values = []
z_values = []

# scan all files and append the useful points to the list
for root, dirs, files in os.walk(path):
    for name in files:
        if name.startswith('Filtered_'):
            
            # create dictionary from csv
            points_file = os.path.join(root, name)
            csv_file = open(points_file)
            csv_dict = csv.DictReader(csv_file, delimiter=';')
            
            # get Z points
            for pos in csv_dict:
                z = float(pos['Z'])
                y = float(pos['Y'])
                if -0.04 <= z <= 0.1:
                    if 0.85 <= y <= 1.55:
                        x_values.append(float(pos['X']))
                        y_values.append(y)
                        z_values.append(z)

# print values
print(f'n. points: {len(x_values)}')

# plot points
fig, (wind, z_plot) = plt.subplots(1, 2)

wind.scatter(x_values, y_values, s=5)
wind.set_aspect('equal', adjustable='box')
wind.set_xlim(-0.1, 1)
wind.set_ylim(0.85, 1.55)
wind.set_xticks(np.arange(-0.1, 1, 0.1))
wind.set_yticks(np.arange(0.85, 1.55, 0.05))

z_plot.hist(z_values, bins=70)
plt.show()
