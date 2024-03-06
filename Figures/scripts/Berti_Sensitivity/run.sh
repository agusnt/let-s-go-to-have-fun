#!/bin/bash
#
# Generate the necessary data for a berti sensitivity heat-map. After it 
# generates a heat-map
#
# @param $1 : data from ChampSim it must include a no-prefetch data version and 
# the format of the files must be named as follow: L1D_$CONF_L2C_$CONF
#

# Variables
DIR='../../../../'
ACT=$(pwd)

# # Clean previous pdf
# rm *.pdf >/dev/null 2>&1
#
# mkdir -p csv/spec > /dev/null 2>&1
#
# # Activate env python
# source $DIR/python/env/bin/activate
#
# # Generate csv
# export BASE='no'
# export BASE_LLC='no'
# export CSV='Y'
# export TEST='N'
#
# cd $DIR/bash/ChampSim
#
# # Generate the csv with the information
# ./speedup.sh $1 > $ACT/csv/spec/speedup.csv
# ./accuracy.sh $1 L1D Y > $ACT/csv/spec/l1d_accuracy.csv
# ./accuracy.sh $1 L2C Y > $ACT/csv/spec/l2c_accuracy.csv
# ./pki.sh $1 L1D mpki LOAD_WRITE > $ACT/csv/spec/l1d_mpki.csv
# ./pki.sh $1 L2C mpki LOAD_WRITE_RFO > $ACT/csv/spec/l2c_mpki.csv
# ./pki.sh $1 L1D pfki > $ACT/csv/spec/l1d_pfki.csv
# ./pki.sh $1 L2C pfki > $ACT/csv/spec/l2c_pfki.csv
#
# cd $ACT

# Generate graphs
./lib/gen_pdf.py

# Remove temporal files
rm tmp.json l1d_accuracy.json l1d_mpki.json speedup.json > /dev/null 2>&1

aux=""
for i in *.pdf; do aux="$aux $i"; done

pdfunite $aux output

rm *.pdf

mv output output.pdf
