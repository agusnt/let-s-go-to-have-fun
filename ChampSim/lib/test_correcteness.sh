#!/bin/bash

#
# Return the simulations that does not finish correctly
# 
# Parameters:
#   $1 -> directory with the scripts
#

tst_champsim()
{
    if [[ "$(grep -LR "LLC TOTAL" $1 | wc -l)" != 0 ]]; then
        echo "Error"
        exit 1
    fi
}

