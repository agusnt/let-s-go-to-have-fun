#!/bin/bash
#
# This script call the script that made the graph
#
# @Author: Navarro Torres, Agustín
#

DIR=../../../../python
ACT=$(pwd)

source $DIR/env/bin/activate

cd $DIR/Figures

./gen_fig.py $ACT/tmp.json $1

mv $1 $ACT

cd $ACT

