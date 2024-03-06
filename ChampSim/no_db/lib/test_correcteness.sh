#!/bin/bash

#
# Return the simulations that does not finish correctly
# 
# Parameters:
#   $1 -> directory with the scripts
#
source lib/set_var.sh

error=0
is_right=$(cat $1 | grep "DRAM Statistics" | wc -l)

if [[ $is_right -eq 0 ]]; then
    >&2 echo $1
    error=1
fi

exit $error
