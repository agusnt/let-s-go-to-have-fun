#!/bin/bash
#
# Get energy (Memory Intensive Traces)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> Energy levels, e.g: L1D L2C LLC DRAM
#

###############################################################################
# Variables
###############################################################################
source $(dirname "$0")/common.sh

###############################################################################
# Functions
###############################################################################
fn_data()
{
    foo="$3"
    for i in ${@:4}; do foo=$(echo "$foo"_"$i"); done
    $GET_INFO $1 energy $foo $ENERGY_FILE Y $BASE_LLC
}

###############################################################################
# Main
###############################################################################

# Test correctness
fn_correctness $1

# Print
if [[ $CSV == "Y" ]]; then fn_csv fn_data $1 ${@:1}
else fn_cli fn_data $1 ${@:1}; fi
