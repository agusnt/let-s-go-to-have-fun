#!/bin/bash
#
# Drop a database and populate a database with all folder of a subfolder
#
# @Parameters:
#   1 -> database file
#   2 -> directory with the simulation outputs (this directory has to have
#   the following structure: $2/folder(s)/sim_outputs)
#
# @Author: Navarro Torres, Agustin
#

if [[ $# -ne 2 ]]; then
    echo "The arguments are: db file and directory"
    exit 1
fi

# Drop the database if exists
$(dirname $0)/../utils/drop_db.py $1

# Populate database
for i in $2/*; do
    name=$(echo $i | rev | cut -d'/' -f1 | rev)
    $(dirname $0)/../pop_db.sh $i $name
done
