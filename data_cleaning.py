# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
The following steps are all steps taken to clean and export data for analisys.
Some values may be slightly modified, including stripping extra characters, or changing the order of dates.
The intention is to make minimal adjustements, preserving the original data as much as possible, while also correcting errors in the original data.
"""

import pandas as pd
import sqlite3


df = pd.read_pickle('processed_exports/data_with_naics_title.pkl')
#errors need to be coerced due to an invalid datetime in 3019 due to datatype, unable to select individual row and correct
df['employment_begin_date'] = pd.to_datetime(df['employment_begin_date'], errors='coerce')

#To find bad dates in employment begin date, open df in the spyder variable explorer and sort column descending.
#Results should not be ommitted from the dataset, because even though employment_begin_date is far out of range, the case status is marked as "Certified".
#Cause of the error is unknown, possibly human error on data entry of work order, dates should be manually corrected to best estimate based on end_employment_date
bad_dates = df[df['employment_begin_date'] > '2025-12-31']

bad_indices = bad_dates.index.tolist()

#For now, I'm deciding to impute the begin_employment_year based on the received_date year.
#This seems like a good enough solution for now, and will make updating data more automatic in the future.
#Edge cases may create incorrect data, but at this time only 7 rows seem to have issues, and none of them are negatively impacted.
for index in bad_indices:
    #preserve original date information so only year will change
    old_timestamp = df.iloc[index, 14]
    received_date_year = df.iloc[index, 2].year
    
    #overwrite bad year with same year as the received_date
    new_timestamp = pd.Timestamp(year=received_date_year, month=old_timestamp.month, day=old_timestamp.day,
                                 hour=old_timestamp.hour, minute=old_timestamp.minute, second=old_timestamp.second) 
    df.iloc[index, 14] = new_timestamp


df['employment_begin_date'] = df['employment_begin_date'].astype('datetime64[s]')


df['employment_end_date'] = pd.to_datetime(df['employment_end_date'], errors='coerce')


# employment_end_date years are appearing much higher than expected range, this is causing the dates to be misinterpreted as datetime[ns]
# correcting all out of range dates in a similar way to the previous example of employment_begin_date should correct the column.
bad_dates = df[df['employment_end_date'] > pd.to_datetime('2028-01-01')]
bad_indices = bad_dates.index.tolist()

for index in bad_indices:
    row = df.iloc[index]
    begin_date = row['employment_begin_date']
    end_date = row['employment_end_date']
    if begin_date.month > end_date.month:
        # If emp end month is less than the start month, it's safe to say the workers are returning in the next calendar year, so +1 to year.
        new_timestamp = pd.Timestamp(year=(begin_date.year + 1), month=end_date.month, day=end_date.day,
                                     hour=end_date.hour, minute=end_date.minute, second=end_date.second)
        df.iloc[index, 15] = new_timestamp
    else:
        new_timestamp = pd.Timestamp(year=begin_date.year, month=end_date.month, day=end_date.day,
                                     hour=end_date.hour, minute=end_date.minute, second=end_date.second)
        df.iloc[index, 15] = new_timestamp
    

df['employment_end_date'] = pd.to_datetime(df['employment_end_date'])
df['employment_end_date'] = df['employment_end_date'].astype('datetime64[s]')
#df = df.drop(columns='employment_end_date_2')


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
df['employer_naics'] = df['employer_naics'].astype(str)

# Dataset contains some completely duplicated rows. Remove only rows that are fully duplicated.
df = df.drop_duplicates()
# Need to reindex
df = df.reset_index(drop=True)

#Export cleaned dataset to csv, pkl, feather
df.to_csv('processed_exports/cleaned_final.csv')
df.to_pickle('processed_exports/cleaned_final.pkl')
df.to_feather('processed_exports/cleaned_final.feather')
df.to_parquet('processed_exports/cleaned_final.parquet', compression=None)
#Finally, export as SQLite DB
conn = sqlite3.connect('processed_exports/h2a.db')
df.to_sql('Orders', conn, index=False, if_exists='replace')
conn.close()
