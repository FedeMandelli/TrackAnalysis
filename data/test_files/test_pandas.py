""" PANDAS TESTS """

# imports
import pandas as pd
import xlsxwriter

# load file
file = 'test_Splined.csv'
base_df = pd.read_csv(file, sep=';')

# clean dataframe
base_df.rename(columns={'XSplined': 'X', 'YSplined': 'Y', 'ZSplined': 'Z'}, inplace=True)
base_df.drop(columns=['VXSplined', 'VYSplined', 'VZSplined'], inplace=True)
base_df.dropna(inplace=True)

# # concatenate dataframes
# firstdf = pd.DataFrame(data=[{'nome': 'Federico', 'cognome': 'Mandelli'}])
# seconddf = pd.DataFrame(data=[{'nome': 'Manuela', 'cognome': 'Carnaghi'}])
# new = pd.concat([firstdf, seconddf],ignore_index=True)
# print(new)

# group consecutive
# newdf = pd.DataFrame({'val': [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]})
# # groupdf = newdf.groupby((newdf.val != newdf.val.shift()).cumsum())
# groupedf = newdf[newdf['val'] == 0].groupby((newdf['val'] != 0).cumsum())
# for n, data in groupedf:
#     print(data)
