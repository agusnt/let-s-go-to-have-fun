# Utils

A bunch of script to make my life easier

## Files

### google_sheet_update.py
```python
'''
This script just update a google sheet

The google sheet has to have as a editor the specific user

https://docs.gspread.org/en/latest/oauth2.html

Args:
    1 : Name of google sheet
    2 : Name of the csv
    3 : if exists, the pre name of the csv
'''
```

### mean_across_csv.py

```python
'''
Calculate the mean or geomeana of one csv with different suites

Args:
    1 -> file with the different suites
    2 -> 0: Geomean, 1: Mean
'''
```
### to_xlsx.py

Parse CSV files and generate an xlsx

```Python
'''
Generate and xlsx from csv files generated with bash scripts (../../bash/ChampSim)

Arguments:
  @1   -> Output workbook
  @2:n -> all inputs with information

@Author: Navarro-Torres, Agustin 
@Email: agusnavarro11@gmail.com
'''
```

### drop_db.py

```python
'''
Drop the collection of the given database

Arguments:
    @1 -> JSON with the database information

@Author: Navarro-Torres, Agustin 
@Email: agustin.navarro@um.es, agusnavarro11@gmail.com
'''
```
