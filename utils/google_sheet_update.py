#!/usr/bin/python3

'''
This script just update a google sheet

The google sheet has to have as a editor the specific user

https://docs.gspread.org/en/latest/oauth2.html

Args:
    1 : Name of google sheet
    2 : Name of the csv
    3 : if exists, the pre name of the csv
'''

import gspread as gs
import gspread_dataframe as gd
import sys
import pandas 

df = pandas.read_csv(sys.argv[2]) # Read CSV file

# Remove Unnamed
cols = [col for col in df.columns.values if 'Unnamed' not in str(col)]
df = df[cols]

sheet_name = sys.argv[2].split('/')[-1].split('.csv')[0]
if len(sys.argv) == 4: sheet_name = '{}-{}'.format(sys.argv[-1], sheet_name)

gc = gs.service_account() # Read credentials

sh = gc.open(sys.argv[1]) # Open correct sheet

try: sh.del_worksheet(sh.worksheet(sheet_name)) # try to delete worksheet if already exists
except: pass

ws = sh.add_worksheet(sheet_name, rows=df.shape[0], cols=df.shape[1]) # create new workseeth

gd.set_with_dataframe(ws, df) # upload values
