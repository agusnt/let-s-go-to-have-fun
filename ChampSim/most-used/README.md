# Most-used-one

This directory contains a bunch of scripts that are the most used

## Scripts

### populate.sh

```bash
#
# Drop a database and populate a database with all folder of a subfolder
#
# @Parameters:
#   1 -> database json file 
#   2 -> directory with the simulation outputs (this directory has to have
#   the following structure: $2/folder(s)/sim_outputs)
#
# @Author: Navarro Torres, Agustin
#
```

#### DB json file

```json
{
    "connect": "# URL to connect",
    "db": "# Databse name",
    "collection": "# Collection name",
    "base": "# Base binary name",
    "base_llc": "# Base for memory intensive in LLC name"
}
```

### speedup_bar_geomean.py

```python
'''
Generate graph and data with the geomean speedup

Parameters:
    1 : database file configuration
    2 : graph file configuration
    3 : google sheet configuration

@Author: Navarro Torres, Agustin
'''
```

#### DB file configuration

```json
{
    "connect": "#url to connect the databse",
    "db": "#database name",
    "collection": "#collection name"
}
```

#### Graph file json

```json
{
    "colors": "# path to the colors files",
    "translate": {
        # Dictionary to tranlsate the binary name to tag in the graph
        "key": "value"
    },
    "order": [""] # Order field of the gen_fig.py script
}
```

#### Google Sheet json

```json
{
    "name": "# Name of the google sheet to update"
}
```
