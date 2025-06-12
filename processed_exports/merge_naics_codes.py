# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
Spyder Editor

In the original h2a orders, each order has a naics code included, but there are no naics titles available. This means individually looking up each naics code for 
it's meaning, every single time we want to compare data using that code. Here we are merging naics codes with their corresponding description by the definitions provided
from the census.gov. All naics documents are downloaded from: https://www.census.gov/naics/?48967.
"""

# Paired NAICS codes from 2022 up with NAICS 22 descriptions. NAICS definitions downloaded from: https://www.census.gov/naics/2022NAICS/2-6%20digit_2022_Codes.xlsx
# More NAICS docs available here: https://www.census.gov/naics/?48967
import pandas as pd

# even though this file is inside the 'processed_exports' folder, when running the file in the spyder editor, the working directory does not change.
df = pd.read_pickle('pkl/py_25-08.pkl')
naics_22 = pd.read_excel('naics_codes/2-6 digit_2022_Codes.xlsx')
naics_17 = pd.read_excel('naics_codes/2-6 digit_2017_Codes.xlsx')
naics_12 = pd.read_excel('naics_codes/2-digit_2012_Codes.xls')
naics_07 = pd.read_excel('naics_codes/naics07.xls', skiprows=[1])

# naics_07 has some data quality issues. They have chosen to use a dash in 3 different areas to show that a range is sharing the description, e.g. "31-33", "44-45", and "48-49".
# This is incompatible for data merging, and is not consistent with other documents, so I have decided to simply remove the dashes from 3 cells.
# It is not expected to have a significant impact on the quality of merged data.
naics_07.iloc[273, 1] = naics_07.iloc[273, 1][:2]
naics_07.iloc[1202, 1] = naics_07.iloc[1202, 1][:2]
naics_07.iloc[1378, 1] = naics_07.iloc[1378, 1][:2]
naics_07['2007 NAICS US Code'] = pd.to_numeric(naics_07['2007 NAICS US Code'])

# df['received_date'] = pd.to_datetime(df['received_date'], yearfirst=True)
df['received_date'] = df['received_date'].astype('datetime64[s]')
df['decision_date'] = df['decision_date'].astype('datetime64[s]')

# Extra space in naics code column is coming directly from naics downloaded file.
df22 = df[df['received_date'] >= '2022-01-01']
df22 = df22.merge(naics_22['2022 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_22['2022 NAICS US   Code'])
df22 = df22.rename(columns={'2022 NAICS US Title': 'naics_title'})

df17 = df[(df['received_date'] >= '2017-01-01') & (df['received_date'] < '2022-01-01')]
df17 = df17.merge(naics_17['2017 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_17['2017 NAICS US   Code'])
df17 = df17.rename(columns={'2017 NAICS US Title': 'naics_title'})

df12 = df[(df['received_date'] >= '2012-01-01') & (df['received_date'] < '2017-01-01')]
df12 = df12.merge(naics_12['2012 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_12['2012 NAICS US   Code'])
df12 = df12.rename(columns={'2012 NAICS US Title': 'naics_title'})

df07 = df[df['received_date'] < '2012-01-01']
df07 = df07.merge(naics_07['2007 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_07['2007 NAICS US Code'])
df07 = df07.rename(columns={'2007 NAICS US Title': 'naics_title'})

df2 = pd.concat([df22, df17, df12, df07])
df2 = df2.reindex(columns=['case_number', 'case_status', 'received_date', 'decision_date', 'employer_name', 'employer_dba', 'employer_naics', 'naics_title', 'soc_code', 'soc_title', 'job_title', 'total_workers_needed', 'total_workers_requested',
                  'total_workers_certified', 'employment_begin_date', 'employment_end_date', 'worksite_address', 'worksite_city', 'worksite_state', 'worksite_postal',
                  'worksite_county', 'housing_address', 'housing_city', 'housing_state', 'housing_postal', 'housing_county'])

pd.to_pickle(df2, 'processed_exports/data_with_naics_title.pkl')
df2.to_csv('processed_exports/data_with_naics_title.csv')
del [df07, df12, df17, df22, naics_07, naics_12, naics_17, naics_22, df]
