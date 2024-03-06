#!/bin/bash
#
# Get prefetch accuracy (Memory Intensive Traces)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> cache level (L1I, L1D, L2C, LLC, DTLB, STLB)
#   $3 -> Y if count lates prefetch 
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
    if [[ "$3" == "Y" ]]; then
         $GET_INFO $1 accuracy_late $2 N $BASE_LLC
    else
         $GET_INFO $1 accuracy $2 N $BASE_LLC
    fi
}

###############################################################################
# Main
###############################################################################

# Test correctness
fn_correctness $1

# Print
if [[ $CSV == "Y" ]]; then fn_csv fn_data $1 $2 $3
else fn_cli fn_data $1 $2 $3; fi
