#!/bin/bash
#
# Get demand cache MPKI (Memory Intensive traces)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> cache level: (L1I, L1D, L2C, LLC, DTLB, STLB)
#   $3 -> mpki, apki, hpki, pfki
#   $4 -> element (e.g.: LOAD_RFO_PREFETCH)
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
    $GET_INFO $1 $2 $3 $4 Y $BASE_LLC
}

###############################################################################
# Main
###############################################################################

# Test correctness
fn_correctness $1

# Print
if [[ $CSV == "Y" ]]; then fn_csv fn_data $1 $3 $2 $4
else fn_cli fn_data $1 $3 $2 $4; fi
