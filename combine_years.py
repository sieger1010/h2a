# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
Spyder Editor

This file is used to combine all the DOL reporting data into a single dataframe. As groups of DOL reporting data are combined, 
they will be exported as a pickle file to the pkl folder for faster read access.
Combinations of years are chosen according to matching columns. When a new year is being loaded, if it has less columns than the previous year, it will no longer be grouped together.
All groups of years exported as pkl will have matching columns.
"""

# %%
print('This script takes several minutes to read all program years from excel format and export as pkl. Progress updates will be printed to the console. Script finishes after processing program year 2008.')
import pandas as pd

rename_columns = ['case_number', 'case_status', 'received_date', 'decision_date', 'employer_name', 'employer_dba', 'employer_naics', 'soc_code', 'soc_title', 'job_title', 'total_workers_needed', 'total_workers_requested',
                  'total_workers_certified', 'employment_begin_date', 'employment_end_date', 'worksite_address', 'worksite_city', 'worksite_state', 'worksite_postal',
                  'worksite_county', 'housing_address', 'housing_city', 'housing_state', 'housing_postal', 'housing_county']

py_columns = ['CASE_NUMBER', 'CASE_STATUS', 'RECEIVED_DATE', 'DECISION_DATE', 'EMPLOYER_NAME', 'TRADE_NAME_DBA', 'NAICS_CODE', 'SOC_CODE', 'SOC_TITLE', 'JOB_TITLE', 'TOTAL_WORKERS_NEEDED',
              'TOTAL_WORKERS_H2A_REQUESTED', 'TOTAL_WORKERS_H2A_CERTIFIED', 'EMPLOYMENT_BEGIN_DATE', 'EMPLOYMENT_END_DATE', 'WORKSITE_ADDRESS', 'WORKSITE_CITY',
              'WORKSITE_STATE', 'WORKSITE_POSTAL_CODE', 'WORKSITE_COUNTY', 'HOUSING_ADDRESS_LOCATION', 'HOUSING_CITY', 'HOUSING_STATE', 'HOUSING_POSTAL_CODE', 'HOUSING_COUNTY']
col_rename = dict(zip(py_columns, rename_columns))
# %%
# Get most recent data from 2025 to 2020, reduce number of columns from each data set, then concat all years and export as pickle.
py25 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2025_Q2.xlsx')
py25 = py25[py_columns]
py25 = py25.rename(columns=col_rename)
print('Processed py25')

py24 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2024_Q4.xlsx')
py24 = py24[py_columns]
py24 = py24.rename(columns=col_rename)
print('Processed py24')

py23 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2023_Q4.xlsx')
py23 = py23[py_columns]
py23 = py23.rename(columns=col_rename)
print('Processed py23')

py22 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2022_Q4.xlsx')
py22 = py22[py_columns]
py22 = py22.rename(columns=col_rename)
print('Processed py22')

py21 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2021.xlsx')
py21 = py21[py_columns]
py21 = py21.rename(columns=col_rename)
print('Processed py21')

py20 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2020.xlsx')
py20 = py20[py_columns]
py20 = py20.rename(columns=col_rename)
print('Processed py20')

df = pd.concat([py25, py24, py23, py22, py21, py20])
df = df.reset_index(drop=True)
pd.to_pickle(df, 'pkl/py_25-20.pkl')
df.to_csv('csv/py_25-20.csv')

# Remove frames no longer in use
del [py25, py24, py23, py22, py21, py20, df]
print('Exported program years 25-20 as pkl and csv then removed from memory...')
# %%
# Starting with year 2019, the column names will change, so py_columns and rename_columns need to be updated to the correct column names, then, col_rename needs to be rebuilt.
# Columns no longer existing from 2019 onwards: TOTAL_WORKERS_NEEDED, WORKSITE_ADDRESS, HOUSING_ADDRESS_LOCATION, HOUSING_CITY, HOUSING_STATE, HOUSING_POSTAL_CODE, HOUSING_COUNTY
# Columns with nan data will need to be created if 2019 and older datasets will be concatenated to py_25-20

py_columns = ['CASE_NUMBER', 'CASE_STATUS', 'CASE_RECEIVED_DATE', 'DECISION_DATE', 'EMPLOYER_NAME', 'TRADE_NAME_DBA', 'NAICS_CODE', 'SOC_CODE', 'SOC_TITLE', 'JOB_TITLE',
              'NBR_WORKERS_REQUESTED', 'NBR_WORKERS_CERTIFIED', 'JOB_START_DATE', 'JOB_END_DATE', 'WORKSITE_CITY',
              'WORKSITE_STATE', 'WORKSITE_POSTAL_CODE', 'WORKSITE_COUNTY']

rename_columns = ['case_number', 'case_status', 'received_date', 'decision_date', 'employer_name', 'employer_dba', 'employer_naics', 'soc_code', 'soc_title', 'job_title', 'total_workers_requested',
                  'total_workers_certified', 'employment_begin_date', 'employment_end_date', 'worksite_city', 'worksite_state', 'worksite_postal', 
                  'worksite_county']

col_rename = dict(zip(py_columns, rename_columns))

py19 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2019.xlsx')
py19 = py19[py_columns]
py19 = py19.rename(columns=col_rename)
print('Processed py19')

# CASE_NUMBER needs to be updated to CASE_NO for 2018 data
py_columns[0] = 'CASE_NO'
col_rename = dict(zip(py_columns, rename_columns))
py18 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY2018_EOY.xlsx')
py18 = py18[py_columns]
py18 = py18.rename(columns=col_rename)
print('Processed py18')

# CASE_NO changes back to CASE_NUMBER for 2017
py_columns[0] = 'CASE_NUMBER'
col_rename = dict(zip(py_columns, rename_columns))
py17 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY17.xlsx')
py17 = py17[py_columns]
py17 = py17.rename(columns=col_rename)
print('Processed py17')


df = pd.concat([py19, py18, py17])
df = df.reset_index(drop=True)
pd.to_pickle(df, 'pkl/py_19-17.pkl')
df.to_csv('csv/py_19-17.csv')
del [py19, py18, py17, df]
print('Exported program years 19-17 as pkl and csv then removed from memory...')
# %%

# TRADE_NAME_DBA, WORKSITE_COUNTY removed; NAICS_CODE renamed to NAIC_CODE.
py_columns = ['CASE_NUMBER', 'CASE_STATUS', 'CASE_RECEIVED_DATE', 'DECISION_DATE', 'EMPLOYER_NAME', 'NAIC_CODE', 'SOC_CODE', 'SOC_TITLE', 'JOB_TITLE',
              'NBR_WORKERS_REQUESTED', 'NBR_WORKERS_CERTIFIED', 'JOB_START_DATE', 'JOB_END_DATE', 'WORKSITE_CITY',
              'WORKSITE_STATE', 'WORKSITE_POSTAL_CODE']

rename_columns = ['case_number', 'case_status', 'received_date', 'decision_date', 'employer_name', 'employer_naics', 'soc_code', 'soc_title', 'job_title', 'total_workers_requested',
                  'total_workers_certified', 'employment_begin_date', 'employment_end_date', 'worksite_city', 'worksite_state', 'worksite_postal']

col_rename = dict(zip(py_columns, rename_columns))


py16 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY16_updated.xlsx')
py16 = py16[py_columns]
py16 = py16.rename(columns=col_rename)
print('Processed py16')


py15 = pd.read_excel('dol_reporting_data/H-2A_Disclosure_Data_FY15_Q4.xlsx')
py15 = py15[py_columns]
py15 = py15.rename(columns=col_rename)
print('Processed py15')
df = pd.concat([py16, py15])
df = df.reset_index(drop=True)
pd.to_pickle(df, 'pkl/py_16-15.pkl')
df.to_csv('csv/py_16-15.csv')
del [py16, py15, df]
print('Exported program years 16-15 as pkl and csv then removed from memory...')
# %%
# NAIC_CODE, WORKSITE_POSTAL_CODE removed; CASE_NUMBER, NBR_WORKERS_REQUESTED, JOB_START_DATE, JOB_END_DATE, WORKSITE_CITY, WORKSITE_STATE renamed.
py_columns = ['CASE_NO', 'CASE_STATUS', 'CASE_RECEIVED_DATE', 'DECISION_DATE', 'EMPLOYER_NAME', 'SOC_CODE_ID', 'SOC_TITLE', 'JOB_TITLE', 'NBR_WORKERS_CERTIFIED', 'CERTIFICATION_BEGIN_DATE', 'CERTIFICATION_END_DATE',
              'WORKSITE_LOCATION_CITY', 'WORKSITE_LOCATION_STATE']
rename_columns = ['case_number', 'case_status', 'received_date', 'decision_date', 'employer_name', 'soc_code', 'soc_title', 'job_title', 'total_workers_certified', 'employment_begin_date', 'employment_end_date',
                  'worksite_city', 'worksite_state']
col_rename = dict(zip(py_columns, rename_columns))

py14 = pd.read_excel('dol_reporting_data/H-2A_FY14_Q4.xlsx')
py14 = py14[py_columns]
py14 = py14.rename(columns=col_rename)
print('Processed py14')
py14 = py14.reset_index(drop=True)
pd.to_pickle(py14, 'pkl/py_14.pkl')
py14.to_csv('csv/py_14.csv')
del py14
print('Exported program year 14 as pkl and csv then removed from memory...')
# %%
# SOC_CODE_ID, SOC_TITLE removed; WORKSITE_LOCATION_CITY, WORKSITE_LOCATION_STATE renamed.
py_columns = ['CASE_NO', 'CASE_STATUS', 'CASE_RECEIVED_DATE', 'DECISION_DATE', 'EMPLOYER_NAME', 'JOB_TITLE', 'NBR_WORKERS_CERTIFIED', 'CERTIFICATION_BEGIN_DATE', 'CERTIFICATION_END_DATE',
              'ALIEN_WORK_CITY', 'ALIEN_WORK_STATE']
rename_columns = ['case_number', 'case_status', 'received_date', 'decision_date', 'employer_name', 'job_title', 'total_workers_certified', 'employment_begin_date', 'employment_end_date',
                  'worksite_city', 'worksite_state']
col_rename = dict(zip(py_columns, rename_columns))



py13 = pd.read_excel('dol_reporting_data/H2A_FY2013.xlsx')
py13 = py13[py_columns]
py13 = py13.rename(columns=col_rename)
print('Processed py13')


py12 = pd.read_excel('dol_reporting_data/H-2A_FY2012.xlsx')
py12 = py12[py_columns]
py12 = py12.rename(columns=col_rename)
print('Processed py12')


py11 = pd.read_excel('dol_reporting_data/H-2A_FY2011.xlsx')
py11 = py11[py_columns]
py11 = py11.rename(columns=col_rename)
print('Processed py11')


py10 = pd.read_excel('dol_reporting_data/H-2A_FY2010.xlsx')
py10 = py10[py_columns]
py10 = py10.rename(columns=col_rename)
print('Processed py10')


py09 = pd.read_excel('dol_reporting_data/H2A_FY2009.xlsx')
py09 = py09[py_columns]
py09 = py09.rename(columns=col_rename)
print('Processed py09')


py08 = pd.read_excel('dol_reporting_data/H2A_FY2008.xlsx')
py08 = py08[py_columns]
py08 = py08.rename(columns=col_rename)
print('Processed py08')

df = pd.concat([py13, py12, py11, py10, py09, py08])
df = df.reset_index(drop=True)
pd.to_pickle(df, 'pkl/py_13-08.pkl')
df.to_csv('csv/py_13-08.csv')
del [py13, py12, py11, py10, py09, py08, df]
print('Exported program years 13-08 as pkl and csv then removed from memory...')
print('Finished exporting all program years from 2025 to 2008 to pkl and csv folders.')
# %%
# Now all years will be concatenated to one dataframe
py25_20 = pd.read_pickle('pkl/py_25-20.pkl')
py19_17 = pd.read_pickle('pkl/py_19-17.pkl')
py16_15 = pd.read_pickle('pkl/py_16-15.pkl')
py14 = pd.read_pickle('pkl/py_14.pkl')
py13_08 = pd.read_pickle('pkl/py_13-08.pkl')

df = pd.concat([py25_20, py19_17, py16_15, py14, py13_08])
df = df.reset_index(drop=True)
pd.to_pickle(df, 'pkl/py_25-08.pkl')
df.to_csv('csv/py_25-08.csv')
del [df, py25_20, py19_17, py16_15, py14, py13_08]
# %%

