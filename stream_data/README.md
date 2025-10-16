# H-2A Order Data from Seasonal Jobs API
Data pulled from https://api.seasonaljobs.dol.gov/datahub-search/sjCaseData/zip/h2a/{date} (replace {date} with todays date in yyyy-mm-dd format).

## stream_data.xxx (Temporarily Only Available in .feather)
These files are complete, raw data coming from the stream api, it contains 180 columns of data, which may be more than needed for most users. No information is lost, so if you need something that's not included in the processed_stream_data, this is where you can find it.

## processed_stream_data.xxx

These files are reduced size files containing basic information from the orders.

Columns available:
* Case Number
* Date order submitted and accepted
* Employer business name & DBA name
* NAICS code and title
* Employer address
* Employer point of contact - name, job title, phone, and email
* Worker job title
* Number of workers needed and number requested/approved
* Employment start and end date
* Worksite address
* Housing address
* Contract wage and payment period (hourly, weekly, monthly, etc)

## Excel Users
Download the csv files, and then save as an xlsx on your computer.

## SQL Users
SQLite files are available for download, both files use the .db extension.

## Web Application Developers
The full raw dataset is saved in the original json format.

## Python or Other Specialized Data Analysis Users
Both datasets are available in csv, or feather.