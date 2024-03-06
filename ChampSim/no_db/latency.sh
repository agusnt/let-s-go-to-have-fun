#!/bin/bash
#
# Get average miss latency (Memory Intensive)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> Cache level (L1I, L1D, L2C, LLC, DTLB, STLB)
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
    # $1 -> path to the directory
    $GET_INFO $1 latency $2 Y $BASE_LLC
}

###############################################################################
# Main
###############################################################################
#
# Test correctness
fn_correctness $1

# Print
if [[ $CSV == "Y" ]]; then fn_csv fn_data $1 $2
else fn_cli fn_data $1 $2; fi
