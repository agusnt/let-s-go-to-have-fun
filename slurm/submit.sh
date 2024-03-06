#!/bin/bash
#
# Author: Navarro-Torres, Agustín
# Date: 11/11/2022
#
# Submit jobs into slurm
#
# Parameters:
#   $1 : Bin folder
#   $2 : Memory intensive files
#   $3 : Utils to load
#   $4 : Output folder
#   $5- : Extra arguments for the utils
#

if [ "$#" -lt 4 ]; then echo "I need at least two arguments"; exit; fi

source .env

# Set global vars config
OUT=$OUT$4
DIR=$(dirname "$0") # Actual dir
BIN=$1 # Binary dir
MAX=10000 # Maximum jobs in slurm at the same time

# Sub traces folder
TRACES=(
    $MAIN_TRACES/champsim-spec17/ 
    $MAIN_TRACES/champsim-ML-DPC/ChampSimTraces/gap/
    $MAIN_TRACES/champsim-CVP-IISWC23
)

source $2 # import the memory intensive traces
source $3 # Import the utils to load

f ${@:5} # Call the function tu run the jobs
