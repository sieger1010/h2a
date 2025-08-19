# List of major changes

## 8/19/2025
New data from DOL Q3 was released around 8/15/2025 and has now been added to this dataset.

The process of adding the data introduced some previously unforseen issues with the data cleaning process, and found a minor issue with the merge_naics_codes script where the index of the full dataset was not being reset. This caused issues in the data_cleaning script with being unable to find the correct row based on index number.

The data_cleaning script has been updated to fix dates that are assumed to be human error during the DOL data entry process, dates were far out of range for reasonable program reporting. This caused datetime columns to be coerced into a nanoseconds format, when the actual precision should only be at the seconds level. To fix this issue, some assumptions were made about what the correct date range should be, and can now be programmatically fixed in the next data update.