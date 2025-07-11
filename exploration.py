# -*- coding: utf-8 -*-
"""
This document shows steps taken to produce data insights on H-2A labor.

@author: sieger1010
"""
import pandas as pd

df = pd.read_pickle('pkl/py_25-08.pkl')

# Remove duplicates, determined by case_number and case_status
df1 = df.drop_duplicates(subset=['case_number'], keep='last')

df2 = df.drop_duplicates(subset=['case_number', 'case_status'], keep='last')

df3 = df[df.duplicated(subset=['case_number'], keep=False)]
df3 = df3.sort_values(by=['employment_begin_date', 'case_number'], ascending=False).reset_index(drop=True)

#remove all leading and trailing spaces, periods, tabs, and new lines, then return unique rows.
worksite_addresses = (
df[['worksite_address', 'worksite_city', 'worksite_state', 'worksite_postal', 'worksite_county']]
    .apply(lambda x: x.str.strip(' .\t\n'), axis=1)
    .drop_duplicates(keep='first')
    )
housing_addresses = (
    df[['housing_address', 'housing_city', 'housing_state', 'housing_postal', 'housing_county']]
    .apply(lambda x: x.str.strip(' .\t\n'), axis=1)
    .drop_duplicates(keep='first')
    )
