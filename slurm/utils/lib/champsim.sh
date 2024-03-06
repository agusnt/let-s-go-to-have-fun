#!/bin/bash
#
# Common functions for champsims
#
# Author: Navarro-Torres, Agustín
# Date: 02/02/2024
#
#

add_bench() {
    # Only run XK jobs at the same time to not saturate slurm
    while true; do
        if [[ "$(sqnum | head -n1 | tr -s ' ' | cut -d' ' -f2)" == "PENDING" ]]; then
            val=$(sqnum | grep ant_uz | tr -s ' ' | cut -d' ' -f3)
            if [[ $val -lt $MAX ]]; then break; fi
            echo "Waiting (1h) number of pending jobs $val"
            sleep 1h
        else
            break
        fi
    done
        
    if [ -z $DEADLINE ]; then
        sbatch --output=/dev/null --error=/dev/null --wrap="$1"
    else
        # Deadline mode
        sbatch --output=/dev/null --error=/dev/null --qos=deadlines --wrap="$1"
    fi
}
