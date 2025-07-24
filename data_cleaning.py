# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
The following steps are all steps taken to clean and export data for analisys.
Some values may be slightly modified, including stripping extra characters, or changing the order of dates.
The intention is to make minimal adjustements, preserving the original data as much as possible, while also correcting errors in the original data.
"""

import pandas as pd

df = pd.read_pickle('processed_exports/data_with_naics_title.pkl')
#errors need to be coerced due to an invalid datetime in 3019 due to datatype, unable to select individual row and correct
df['employment_begin_date'] = pd.to_datetime(df['employment_begin_date'], errors='coerce')
#error found at row index 62765 'employment_begin_date' == '12/20/1011' - manually changing date to 2022/12/20 as this is best guest for typo correction
# rows 62765, 119225, 137675, 191435, 115112, 111327, 1119504, 97169 all have bad dates. Correcting each to match year of 'employment_end_date'
df.iloc[62765, 14] = '2022-12-20 00:00:00'
df.iloc[119225, 14] = '2019-03-31 00:00:00'
df.iloc[137675, 14] = '2018-05-22 00:00:00'
df.iloc[191435, 14] = '2013-07-01 00:00:00'
df.iloc[115112, 14] = '2019-01-22 00:00:00'
df.iloc[111327, 14] = '2019-03-08 00:00:00'
df.iloc[111326, 14] = '2019-01-22 00:00:00'
df.iloc[119504, 14] = '2018-11-21 00:00:00' #setting employment_begin_date to previous year so it is not before employment_end_date
df.iloc[97169, 14] = '2020-07-15 00:00:00'

df['employment_begin_date'] = df['employment_begin_date'].astype('datetime64[s]')


df['employment_end_date_2'] = pd.to_datetime(df['employment_end_date'], errors='coerce')
bad_dates = df[df['employment_end_date_2'].isna()]
#bad employment_end_date found at index 17896
df.iloc[17896, 15] = '2026-06-20 00:00:00'
df['employment_end_date'] = pd.to_datetime(df['employment_end_date'])
df['employment_end_date'] = df['employment_end_date'].astype('datetime64[s]')
df = df.drop(columns='employment_end_date_2')


df['total_workers_needed'] = df['total_workers_needed'].astype('Int64')
df['total_workers_requested'] = df['total_workers_requested'].astype('Int64')
df['total_workers_certified'] = df['total_workers_certified'].astype('Int64')

#strip leading/trailing spaces, commas, periods, newlines, tabs
strip_columns = ['case_number', 'case_status', 'employer_name', 'employer_dba', 'job_title',
                 'worksite_address', 'worksite_city', 'worksite_state', 'worksite_county',
                 'housing_address', 'housing_city', 'housing_state', 'housing_county']
for col in strip_columns:
    df[col] = df[col].str.strip(' ,.\'\n\t')

#to lower/upper
to_upper = ['employer_name', 'employer_dba', 'worksite_address', 'worksite_city', 'worksite_state',
            'worksite_county', 'housing_address', 'housing_city', 'housing_state', 'housing_county']
for col in to_upper:
    df[col] = df[col].str.upper()
    
df['job_title'] = df['job_title'].str.title()

#Error when exporting to feather. worksite_postal and housing_postal contain an int object.
df['worksite_postal'] = df['worksite_postal'].astype(str)
df['housing_postal'] = df['housing_postal'].astype(str)

#Export cleaned dataset to csv, pkl, feather
df.to_csv('processed_exports/cleaned_final.csv')
df.to_pickle('processed_exports/cleaned_final.pkl')
df.to_feather('processed_exports/cleaned_final.feather')
df.to_parquet('processed_exports/cleaned_final.parquet', compression=None)
