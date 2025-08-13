# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 16:06:14 2025

@author: sieger1010

This file contains all steps used to create the SQLite database containing the h-2a orders.
"""
import pandas as pd
import sqlite3

df = pd.read_feather('processed_exports/cleaned_final.feather')

conn = sqlite3.connect('processed_exports/h2a.db')
df.to_sql('Orders', conn, index=False, if_exists='replace')


# cursor = conn.cursor()
# cursor.execute("PRAGMA table_info(Orders)")
# temp = cursor.fetchall()

