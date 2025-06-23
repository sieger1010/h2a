# H-2A Labor Data
### Normalized, and Combined Employment Data for H-2A Workers in the United States
<br>

## Visualization
Visualized data is available for exploration on Tableau Public. [Tableau Public Sieger.Bokschoten](https://public.tableau.com/app/profile/sieger.bokschoten/viz/H-2AWorkers/H-2AWorkersbyYearStateandIndustry/)

## Status
Exported data in the pkl and csv folders contain duplicate case numbers. I'm investigating the reason to have duplicate cases, and how to best manage them in the future.

## Purpose
This repository is intended to provide a single source for all H-2A employment data in the United States, and to make it easier to compare years together by normalizing the data. This data is intended for anyone interested in doing their own analysis using specialized software, or programs like Excel.

Modifications to the data will be limited, and will only be made to correct inconsistencies in data quality. Steps like removing white space around text, or removing obvious typos will be documented in the python code.

When analyzing H-2A data, it can be difficult to compare changes year over year for several reasons:
1. The data is not normalized across all years.
2. The program dates for the DOL go from October 1st, to September 30th. This can create confusion when comparing reported data to calendar years.
3. It's not obvious where to find historical data on the H-2A labor force.
4. Reported data changes by year. Currently, the more recent the reported year, the more data that is included.
5. Duplicated cases can be found in the data.


## Data
All data is provided from the Department of Labor's Performance Data [H-2A Performance Data](https://www.dol.gov/agencies/eta/foreign-labor/performance).

The data included in this repository are from:

[FY2025 Q2](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2025_Q2.xlsx) - 
[FY2024](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2024_Q4.xlsx) - [FY2023](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2023_Q4.xlsx) - [FY2022](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2022_Q4.xlsx) -  [FY2021](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2021.xlsx) - [FY2020](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2020.xlsx)
<br>
[FY2019](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2019.xlsx) - [FY2018](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2018_EOY.xlsx) - [FY2017](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY17.xlsx) - [FY2016](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY16_updated.xlsx) - [FY2015](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY15_Q4.xlsx) - [FY2014](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_FY14_Q4.xlsx)
<br>
[FY2013](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H2A_FY2013.xls) - [FY2012](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_FY2012.xlsx) - [FY2011](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_FY2011.xlsx) - [FY2010](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_FY2010.xlsx) - [FY2009](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H2A_FY2009.xlsx) - [FY2008](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H2A_FY2008.xlsx)

## Insights
Data insights will be provided here free for use in the future. All python scripts are being created and tested in the [Spyder IDE](https://www.spyder-ide.org/).

## Dependencies
xlrs package is used to read Excel files.<br>
xlrd package is used to read Excel files.<br>
pandas package is used to manipulate dataframes.

<br>

### Disclaimer
I make no guarantees about the accuracy of this data, but will do my best to keep it up-to-date and error-free. If you find any errors or have suggestions for improvement, please let me know, or make your own contribution!
