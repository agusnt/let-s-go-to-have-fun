#!/bin/bash
#
# Populate the database.
#
# This script thinks that you already have in the directory a db.json file
# with all the information need by by_trace.py (search in the python/Champsim 
# folder) to connect to the database
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agustin.navarro@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> JSON with the extra information
#

###############################################################################
# Variables
###############################################################################
source $(dirname "$0")/lib/test_correcteness.sh
tst_champsim $1

# $1 -> path to the directory
$(dirname "$0")/get_info.py $1 db db.json $2
