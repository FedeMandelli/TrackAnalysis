""" TRACKING ANALYSIS """

# imports
import data.general_func as func
import os
import csv
import json
from shutil import copy


# main function
def main():
    """ === Analysis === """
    # create a list of all the experiments with the information stored as dictionary
    experiments = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('Splined.csv'):
                # create new experiment dictionary
                new_exp = {}
                
                # create analysis folder
                fol_name = f'Py_Analysis_{box_name}'
                a_fol = os.path.join(root, fol_name)
                if not os.path.exists(a_fol):
                    os.makedirs(a_fol)
                
                # copy figures in Py_Analysis folder
                for fig in os.listdir(os.path.join(root, 'figures')):
                    if fig[-3:] == 'png':
                        orig_png = os.path.join(root, 'figures', fig)
                        dest_png = os.path.join(root, fol_name)
                        copy(orig_png, dest_png)
                
                # populate experiment dictionary and copy csv file
                new_exp['folder'] = a_fol
                new_exp['date'] = name[18:-12]
                orig_csv = os.path.join(root, name)
                dest_csv = os.path.join(root, fol_name, f'{new_exp["date"]}_original_data.csv')
                copy(orig_csv, dest_csv)
                new_exp['csv'] = dest_csv
                
                # create list with tracks, each track is a list of its positions
                tracks, info = func.get_tracks(new_exp['csv'])
                new_exp['tracks'] = tracks
                new_exp['general info'] = info
                experiments.append(new_exp)
    
    # analyze data and export in Py_Analysis folder
    for exp in experiments:
        # analysis
        func.box_analysis(exp, box_in, box_out)
    
    """ === Export === """
    # create merged json for landed and not landed
    data = {'mini-tracks': [], 'landed': [], 'not landed': []}
    
    for exp in experiments:
        # export results
        func.export(exp)
        
        # create json for landed and not landed tracks
        func.land_not(exp)
        
        # store data for merged json
        with open(exp['json']) as file:
            new_data = json.load(file)
            for track in new_data['mini-tracks']:
                data['mini-tracks'].append(track)
            for track in new_data['landed']:
                data['landed'].append(track)
            for track in new_data['not landed']:
                data['not landed'].append(track)
    
    # create merged json
    jfile = os.path.join(path, f'land_or_not_{box_name}.json')
    with open(jfile, 'w') as file:
        json.dump(data, file)
    
    # create experiment report in main directory
    report = os.path.join(path, f'general_info_{box_name}.csv')
    report_csv = open(report, 'w', newline='')
    
    fieldnames = []
    for field in experiments[0]['general info']:
        fieldnames.append(field)
    
    writer = csv.DictWriter(report_csv, fieldnames=fieldnames)
    writer.writeheader()
    
    for exp in experiments:
        writer.writerow(exp['general info'])


""" ====== MODIFY UNDER HERE ====== """

""" * create boxes (areas) where I want to analyse tracks
    * in the section "box used" there are the boxes used for the analysis:
        + "box_in" is the box looked at (where I want to analyse)
        + "box_out" is the exclusion area
    * note:
        + "box_fake" is if I don't want to exclude anything. "box_fake" is an area outside the wind tunnel
        + "box_all" is the whole wind tunnel
    * insert the name of the box for the description of the analysis. This will be the name of the folder
    * insert the path where the files to analyze are """

# boxes definitions
box_fake = (0, 0), (0, 0), (-1, -1)
box_test = (-0.5, 0.100), (0.6, 1), (0.3, 0.6)
box_all = (-2, 2), (-2, 2), (-2, 2)

# exp1
box_large1 = (-0.04, 0.44), (0.83, 1.45), (-0.02, 0.2)
box_large2 = (0.44, 0.95), (0.83, 1.45), (-0.02, 0.2)
box_small1 = (-0.04, 0.32), (1.01, 1.45), (-0.02, 0.2)
box_small2 = (0.53, 0.90), (1.01, 1.45), (-0.02, 0.2)
box_onlytrap1 = (0.04, 0.34), (0.93, 1.35), (-0.02, 0.2)

# exp2
box_horiz1 = (-0.04, 0.44), (0.83, 1.45), (-0.02, 0.2)
box_horiz2 = (0.44, 0.95), (0.83, 1.45), (-0.02, 0.2)
box_vertical1 = (-0.04, 0.44), (1.13, 1.38), (-0.02, 0.6)
box_vertical2 = (0.44, 0.95), (1.13, 1.38), (-0.02, 0.6)

# boxes used
box_in = box_horiz2
box_out = box_fake
box_name = 'box_horiz2'  # name of the file created after the analysis

# path
path = 'C:/manu/test'

"""" ====== LAUNCH PROGRAM ====== """
if __name__ == '__main__':
    main()
