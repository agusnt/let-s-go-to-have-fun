#!/bin/bash
#
# Util champsim for 1 core simulations functions
#
# Author: Navarro-Torres, Agustín
# Date: 02/02/2024
#

source $(dirname "$0")/lib/champsim.sh # Load the libs

f_s () {
    ITER=0
    BENCH_ITER=""
    # Wrap all the benchmarks
    for i in $BIN/*; do
        binary=$(echo $i | rev | cut -d'/' -f1 | rev)
        for ii in $1/*.{gz,xz}; do
            name=$(echo $ii | rev | cut -d'/' -f1 | rev)
            [[ "$ii" =~ [\*]+ ]] && continue 
    
            if [[ ! -z $INT ]] && [[ ! ${INT[@]} =~ $(echo $name | cut -d'.' -f1) ]]; then
                # Check if the trace is in the list for running
                continue
            fi
    
            if [[ "$2" == "cvp" ]]; then
                folder=""
                [[ "$name" =~ "compute_fp" ]] && folder=$2"_compute_fp"
                [[ "$name" =~ "compute_int" ]] && folder=$2"_compute_int"
                [[ "$name" =~ "crypto" ]] && folder=$2"_crypto"
                [[ "$name" =~ "srv" ]] && folder=$2"_srv"
                mkdir -p $OUT/$folder >/dev/null 2>&1
                bench="$(pwd)/$i -w 25000000 -i 75000000 $ii > $OUT/$folder/$binary---$name.out 2>&1"
            else
                bench="$(pwd)/$i -w 25000000 -i 75000000 $ii > $OUT/$2/$binary---$name.out 2>&1"
                mkdir -p $OUT/$2 >/dev/null 2>&1
            fi
            if [[ -z $BATCH ]]; then
                add_bench "$bench"
            else
                if [[ "$ITER" -ge "$BATCH" ]]; then
                    add_bench "$BENCH_ITER"    
                    ITER=0
                    BENCH_ITER=0
                else
                    ITER=$(($ITER + 1))
                    BENCH_ITER="$bench;$BENCH_ITER"
                fi
            fi
        done
    done
}

f() {
    f_s $MAIN_TRACES/champsim-spec17/ spec
    f_s $MAIN_TRACES/champsim-ML-DPC/ChampSimTraces/gap/ gap 
    f_s $MAIN_TRACES/champsim-CVP-IISWC23 cvp
}
