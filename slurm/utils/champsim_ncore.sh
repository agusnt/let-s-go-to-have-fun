#!/bin/bash
#
# Util champsim for 1 core simulations functions
#
# The f function receive as parameters:
#   1 : the folder where the mixes are
#
# Author: Navarro-Torres, Agustín
# Date: 02/02/2024
#

source $(dirname "$0")/lib/champsim.sh # Load the libs

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
        sbatch --output=/dev/null --error=/dev/null --qos=deadlines --wrap="$1"
    fi
}

f () {
ITER=0
BENCH_ITER=""
# Wrap all the benchmarks
for i in $BIN/*; do
    binary=$(echo $i | rev | cut -d'/' -f1 | rev)
    bench="$(pwd)/$i -w 50000000 -i 200000000"
    out_s="> $OUT/$binary---"
    mkdir -p $OUT/ > /dev/null 2>&1

    for file in $1/*; do
        traces=""
        while IFS= read -r line
        do
            traces="$traces$(find ${TRACES[*]} -name "$line.*") "
        done < "$file"

        # Add benchmark
        add_bench "$bench $traces $out_s$(echo $file | rev | cut -d'/' -f1 | rev).out 2>&1"
    done
done
}
