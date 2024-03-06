#!/bin/bash

# Set variables to run the experiments 
ENERGY_FILE=$(dirname "$0")/../config_json/energy.json
if [ -z $BASE ]; then BASE=no; fi
if [ -z $BASE_LLC ]; then BASE_LLC=no; fi
if [ -z $CSV ]; then CSV="N"; fi # Print as CSV or human readable format
if [ -z $TEST ]; then TEST="Y"; fi # Test if outputs are right
