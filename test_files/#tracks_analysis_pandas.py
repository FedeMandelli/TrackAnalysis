""" TRACKING ANALYSIS """

# imports
import pandas_func as pdfunc
import os
from shutil import copy


# main function
def main():
    """ === General Info Initialization === """
    exp_info = []
    exp_tracks = []
    exp_minitracks = []
    exp_points = []
    
    """ === Splined.csv Files Analysis === """
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('Splined.csv'):
                """ === Basic Experiment Information === """
                # get experiment name
                exp_name = os.path.split(root)[-1]
                print(exp_name, end='')
                # create analysis folder
                analysis_folder = os.path.join(root, f'Py_Analysis_{box_name}')
                if not os.path.exists(analysis_folder):
                    os.makedirs(analysis_folder)
                
                # copy figures in Py_Analysis folder
                for fig in os.listdir(os.path.join(root, 'figures')):
                    if fig[-3:] == 'png':
                        orig_png = os.path.join(root, 'figures', fig)
                        dest_png = analysis_folder
                        copy(orig_png, dest_png)
                
                # copy original csv file in Py_Analysis folder
                orig_csv = os.path.join(root, name)
                dest_csv = os.path.join(analysis_folder, f'{exp_name}_original_data.csv')
                copy(orig_csv, dest_csv)
                
                # loading tracks
                tracks, exp_df = pdfunc.get_tracks_pandas(dest_csv, exp_name)
                
                """ === Tracks and Boxes Analysis === """
                tracks_df, minitracks_df, exp_df, points = pdfunc.box_analysis(tracks, exp_df, box_in, box_out)
                
                """ === Export === """
                # create file and writer
                file_name = f'{exp_name}_{box_name}_analysis.xlsx'
                exc_w = pdfunc.pd.ExcelWriter(os.path.join(analysis_folder, file_name), engine='xlsxwriter')
                
                # export dataframes in separate sheets
                exp_export = {'General Info': exp_df,
                              'Tracks': tracks_df,
                              'Mini Tracks': minitracks_df,
                              'Points': points}
                for n, df in exp_export.items():
                    pdfunc.to_excel(df, n, exc_w)
                
                # close excel file
                exc_w.save()
                
                """ === Append to General Info === """
                exp_info.append(exp_df)
                exp_tracks.append(tracks_df)
                exp_minitracks.append(minitracks_df)
                exp_points.append(points)
                print(' *** done ***')
    
    print('exporting analysis', end='')
    """ === General Info Export === """
    # create file and writer
    file_name = f'{box_name}_analysis.xlsx'
    exc_w = pdfunc.pd.ExcelWriter(os.path.join(path, file_name), engine='xlsxwriter')
    
    # export dataframes in separate sheets
    general_export = {'General Info': pdfunc.pd.concat(exp_info, ignore_index=True),
                      'Tracks': pdfunc.pd.concat(exp_tracks, ignore_index=True),
                      'Mini Tracks': pdfunc.pd.concat(exp_minitracks, ignore_index=True),
                      'Points': pdfunc.pd.concat(exp_points, ignore_index=True)}
    for n, df in general_export.items():
        pdfunc.to_excel(df, n, exc_w)
    
    # close excel file
    exc_w.save()
    print(' *** done ***')


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
box_in = box_large1
box_out = box_fake
box_name = 'test_pandas'  # name of the file created after the analysis

# path
path = 'C:/manu/test'

"""" ====== LAUNCH PROGRAM ====== """
if __name__ == '__main__':
    main()
