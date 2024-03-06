#!/bin/bash
#
# Get average ROB occupancy at branch miss prediction (Memory Intensive Traces)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
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
    $GET_INFO $1 branch_rob Y $BASE_LLC
}

###############################################################################
# Main
###############################################################################

# Test correctness
fn_correctness $1

# Print
if [[ $CSV == "Y" ]]; then fn_csv fn_data $1
else fn_cli fn_data $1; fi
