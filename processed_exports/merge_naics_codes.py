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

df = pd.read_pickle('../pkl/py_25-08.pkl')
naics_22 = pd.read_excel('../naics_codes/2-6 digit_2022_Codes.xlsx')
naics_17 = pd.read_excel('../naics_codes/2-6 digit_2017_Codes.xlsx')
naics_12 = pd.read_excel('../naics_codes/2-digit_2012_Codes.xls')
naics_07 = pd.read_excel('../naics_codes/naics07.xls', skiprows=[1])

# naics_07 has some data quality issues. They have chosen to use a dash in 3 different areas to show that a range is sharing the description, e.g. "31-33", "44-45", and "48-49".
# This is incompatible for data merging, and is not consistent with other documents, so I have decided to simply remove the dashes from 3 cells.
# It is not expected to have a significant impact on the quality of merged data.
naics_07.iloc[273, 1] = naics_07.iloc[273, 1][:2]
naics_07.iloc[1202, 1] = naics_07.iloc[1202, 1][:2]
naics_07.iloc[1378, 1] = naics_07.iloc[1378, 1][:2]
naics_07['2007 NAICS US Code'] = pd.to_numeric(naics_07['2007 NAICS US Code'])

df['employment_begin_date'] = pd.to_datetime(df['employment_begin_date'], errors='coerce', yearfirst=True)
df['employment_begin_date'] = df['employment_begin_date'].astype('datetime64[s]')
df['employment_end_date'] = pd.to_datetime(df['employment_end_date'], errors='coerce', yearfirst=True)
df['employment_end_date'] = df['employment_end_date'].astype('datetime64[s]')

# Extra space is coming directly from naics downloaded file.
#df = df.merge(naics_22[['2022 NAICS US Title']], how='left', left_on='employer_naics', right_on=naics_22['2022 NAICS US   Code'])
df22 = df[df['employment_begin_date'] >= '2022-01-01']
df22 = df22.merge(naics_22['2022 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_22['2022 NAICS US   Code'])
df22 = df22.rename(columns={'2022 NAICS US Title': 'naics_title'})

df17 = df[(df['employment_begin_date'] >= '2017-01-01') & (df['employment_begin_date'] < '2022-01-01')]
df17 = df17.merge(naics_17['2017 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_17['2017 NAICS US   Code'])
df17 = df17.rename(columns={'2017 NAICS US Title': 'naics_title'})

df12 = df[(df['employment_begin_date'] >= '2012-01-01') & (df['employment_begin_date'] < '2017-01-01')]
df12 = df12.merge(naics_12['2012 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_12['2012 NAICS US   Code'])
df12 = df12.rename(columns={'2012 NAICS US Title': 'naics_title'})

df07 = df[df['employment_begin_date'] < '2012-01-01']
df07 = df07.merge(naics_07['2007 NAICS US Title'], how='left', left_on='employer_naics', right_on=naics_07['2007 NAICS US Code'])
df07 = df07.rename(columns={'2007 NAICS US Title': 'naics_title'})

df2 = pd.concat([df22, df17, df12, df07])