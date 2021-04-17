""" PANDAS TESTS """

# imports
import pandas as pd

# get file
file = 'C:/manu/test/2020_08_21_17_46_35 - exp 28 vert vs vert/Py_Analysis_test/2020_08_21_17_46_35 - exp 28 vert vs vert_test_analysis.xlsx'
df = pd.read_excel(file, sheet_name='tracks_data')
print(df)
