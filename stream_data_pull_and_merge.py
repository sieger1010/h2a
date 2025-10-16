# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 16:10:00 2025

@author: sieger1010
"""

import pandas as pd
import requests
import zipfile
import io
import json
from datetime import datetime
import time
import sqlite3
import sys
import logging

########## SETTING for LIVE DATA PULL = 0, or SIMULATION DATA PULL = 1
live_pull_testing = 1

if live_pull_testing == 0:
    print('Live data being pulled from DOL Data Stream.')
else:
    print('Simulated data pull, no internet traffic, pulling local file.')

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

df_main = pd.read_csv('stream_data/stream_data.csv', index_col=0, low_memory=False)
df_main = df_main.map(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)
previous_num_rows = df_main.index.size

#get today's date so URL will work
date = datetime.today().strftime('%Y-%m-%d')

if live_pull_testing == 0:
    # The URL to fetch the ZIP file
    url = f"https://api.seasonaljobs.dol.gov/datahub-search/sjCaseData/zip/h2a/{date}"
    num_attempts = 1
    while num_attempts < 4:
        try:
            # Download the ZIP file
            response = requests.get(url, stream=True, timeout=60)
            time.sleep(1)
            print('Connection attempt:', num_attempts)
            print(f'Attempting to download file. Attempt #{num_attempts}')
            if response.status_code == 200:
                # Open the ZIP file in memory 
                print('Connection established. Sleep 2 seconds for full file download.')
                time.sleep(2)
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    # List the files in the ZIP archive
                    file_names = z.namelist()
                    print("Files in the ZIP archive:", file_names)
        
                    # Extract the first JSON file (or specify the file name)
                    if file_names:
                        with z.open(file_names[0]) as json_file:
                            # Load the JSON data
                            data = json.load(json_file)
                            #print("JSON data:", data)  # Process the data as needed
                            df = pd.json_normalize(data)
                            df = df.map(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)
                    else:
                        print("No files found in the ZIP archive.")
                        num_attempts += 1
            else:
                print(f"Failed to download ZIP file. HTTP Status Code: {response.status_code}")
                num_attempts += 1
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            num_attempts += 1
        except zipfile.BadZipFile as e:
            print(f"Invalid ZIP file: {e}")
            num_attempts += 1
    if num_attempts >= 4:
        print('download failed, terminating script...')
        sys.exit()

# live data does not contain case_status information, but it should be assumed that all cases are finalized and approved
# simulate data pull while DOL site is offline
if live_pull_testing == 1:
    with open('../USDA Census 2022/Census/h2a_json/2025-09-24.json', 'r') as file:
        data = json.load(file)
    
    df = pd.DataFrame(data)
    df = df.map(lambda x: ','.join(map(str, x)) if isinstance(x, list) else x)
# end data pull simulation



# Merge new stream data with old data
df_main = pd.concat([df_main, df]).drop_duplicates(subset='caseNumber').reset_index(drop=True)
new_num_rows = df_main.index.size

print(new_num_rows - previous_num_rows, 'new rows stored.')

# store full backup of all data
df_main.to_csv('stream_data/stream_data.csv')
df_main.to_json('stream_data/stream_data.json')
df_main.to_feather('stream_data/stream_data.feather')
conn = sqlite3.connect('stream_data/stream_data.db')
df_main.to_sql('Orders', conn, index=False, if_exists='replace')
conn.close()


# take only columns desired for regular use.
wanted_cols = ['caseNumber', 'dateSubmitted', 'dateAcceptanceLtrIssued', 'empBusinessName', 'empTradeName', 'empNaics', 'empAddr1', 'empAddr2', 'empCity', 'empState', 'empPostcode', 'empCountry',
               'empAgricAssocOrAgencyStatus', 'emppocLastname', 'emppocFirstname', 'emppocMiddlename', 'emppocJobtitle', 'emppocPhone', 'emppocPhoneext', 'emppocEmail',
               'clearanceOrder.jobTitle', 'clearanceOrder.jobWrksNeeded', 'clearanceOrder.jobWrksNeededH2a', 'clearanceOrder.jobBeginDate', 'clearanceOrder.jobEndDate', 'clearanceOrder.jobAddr1', 
               'clearanceOrder.jobCity', 'clearanceOrder.jobState', 'clearanceOrder.jobPostcode', 'clearanceOrder.jobCounty', 'clearanceOrder.housingAddr1', 'clearanceOrder.housingAddr2', 
               'clearanceOrder.housingCity', 'clearanceOrder.housingState', 'clearanceOrder.housingPostcode', 'clearanceOrder.housingCounty', 'clearanceOrder.jobWageOffer', 'clearanceOrder.jobWagePer']
df_processed = df_main[wanted_cols]

# merge naics code descriptions
naics_2022 = pd.read_excel('naics_codes/2-6 digit_2022_Codes.xlsx', header=0)
df_processed = df_processed.merge(naics_2022[['2022 NAICS US Title']], left_on='empNaics', right_on=naics_2022['2022 NAICS US   Code'], how='left')
last_col = df_processed.pop('2022 NAICS US Title')
df_processed.insert(6, 'naicsTitle', last_col)

# save processed data in the "stream_data" folder
df_processed.to_csv('stream_data/processed_stream_data.csv')
df_processed.to_feather('stream_data/processed_stream_data.feather')
conn = sqlite3.connect('stream_data/processed_stream_data.db')
df_processed.to_sql('Orders', conn, index=False, if_exists='replace')
conn.close()