#!/usr/bin/env python3
'''
Generate a bar graph for speedup

@param $1 : json with the characteristics of the graph
@param $2 : output file (pdf)
@param $3 : file with the raw champsim data 
'''

import os
import sys
import json
from pprint import pprint as ppt

BASH_DIR = '../../../bash/ChampSim'
FIG_SCRIPT = '../gen_fig.py'

def set_os_env():
    '''
    Set environmental variables for the scripts
    '''
    os.environ['BASE'] = 'no'
    os.environ['BASE_LLC'] = 'no'
    os.environ['CSV'] = 'Y'
    os.environ['TEST'] = 'N'

def parse_data(data, color):
    '''
    Parse data from the script

    @param : data to parse

    @return : json to write into a file
    '''
    json_data = []
    x_label = []

    data = data.split('\n')

    names = data[0].split(',')
    for idx, i in enumerate(data[1:-2]):
        raw = i.split(',')

        x_label.append(raw[0])

        for iidx, ii in enumerate(raw[1:]):
            if names[iidx+1] not in color: continue

            json_data.append({
                'x': idx, 
                'y': float(ii),
                'value': names[iidx+1],
                'color': color[names[iidx+1]]
            })

    return json_data, x_label

if __name__ == '__main__':
    set_os_env() # Set vars for the simulation
    actual_path = os.getcwd() # Save working directory

    # Load configuration of the graph
    config_graph = json.load(open(sys.argv[1]))
    # Get legend - color
    color = {i['label']: i['color'] for i in config_graph['graphs'][0]['legend'][0]['elems']}

    os.chdir(BASH_DIR) # Move to the script folder
    data = os.popen('./speedup.sh {}'.format(sys.argv[3])).read() # Get speedup
    os.chdir(actual_path) # Move to this script directory

    data, x_label = parse_data(data, color) # Parse fijle with the data
    json.dump(data, open('data.json', 'w+')) # Write data

    # Save new temporal graph configuration
    config_graph['graphs'][0]['axis']['x']['ticks_label'] = x_label
    config_graph['graphs'][0]['axis']['x']['ticks'] = [i for i in range(0, len(x_label))]
    json.dump(config_graph, open('tmp.json', 'w+'))

    # Call the graph scripts
    os.popen('{} tmp.json {}'.format(FIG_SCRIPT, sys.argv[2])).read()

    # Remove temporal file
    os.remove('tmp.json') 
    os.remove('data.json')
