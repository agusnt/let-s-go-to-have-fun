#!/bin/bash
#
# Generate random mixes from a list
#
# @Author: Navarro Torres, Agustin
# @email: agustin.navarro@um.es, agusnavarro11@gmail.com
#
# Parameters:
#   1 -> number of mixes
#   2 -> number of cores
#   3 -> file with the traces option

source $3

for i in $(seq 1 $1); do
    for j in $(seq 1 $2); do 
        size=${#BENCH[@]}
        index=$(($RANDOM % $size))
        echo ${BENCH[$index]} >> $i.mix
    done
done

