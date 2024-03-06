#!/bin/bash
#
# Get queues info (speedup memory intensive)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> RQ, WQ, PQ, PTWQ
#   $3 -> cache level (L1I, L1D, L2C, LLC, DTLB, STLB)
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
    $GET_INFO $1 queues $2 $3 Y $BASE_LLC
}

###############################################################################
# Main
###############################################################################

# Test correctness
fn_correctness $1

# Print
if [[ $CSV == "Y" ]]; then fn_csv fn_data $1 $3 $2
else fn_cli fn_data $1 $3 $2; fi
