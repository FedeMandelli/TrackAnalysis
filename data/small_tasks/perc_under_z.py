""" check raw data for z points under a given value """

# imports
import os
import csv

# settings
z = -0.02
path = 'C:\\manu\\Varie\\postproc tracks'
p_under = 0
p_all = 0

# scan all files and append the useful points to the list
for root, dirs, files in os.walk(path):
    for name in files:
        if name.startswith('Filtered_'):
            # create dictionary from csv
            points_file = os.path.join(root, name)
            csv_file = open(points_file)
            csv_dict = csv.DictReader(csv_file, delimiter=';')
            
            # count Z points under -0.02
            for pos in csv_dict:
                z_pos = float(pos['Z'])
                if z_pos <= z:
                    p_under += 1
                
                # count point
                p_all += 1

# print results
print(f"""
under:      {p_under:,}
all points: {p_all:,}
percentage: {(p_under / p_all * 100):.4f}%""")
