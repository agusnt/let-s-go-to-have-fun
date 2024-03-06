#!/usr/bin/python3

'''
Convert the mean or geomean of a csv file (produce by champsim scripts) to 
a json that can be used to generate graphs

Args:
    1 -> the information of the columns to parse
    2: -> CSV files to parse
'''

import sys
import json

f = open(sys.argv[1])
order = json.load(f)
f.close()

white_edge_color = ['black', 'navy', 'blue']
dic = {}
json_t = []
for dx, ff in enumerate(sys.argv[2:]):
    with open(ff) as f:
        raw = f.read().split('\n')
        for idx, i in enumerate(raw[0].split(',')): dic[idx] = i
    
        foo = ''
        for i in reversed(raw): 
            bar = i.split(',')
            if bar[0] == 'GEOMEAN' or bar[0] == 'MEAN':
                foo = bar
                break

        for idx, i in enumerate(foo):
            if dic[idx] not in order: continue
            c = order[dic[idx]] 

            # Select the color of edge to match the color of the bar
            ec = 'black'
            if c in white_edge_color: ec = 'white'

            json_t.append({'y': float(i), 'x': dx, 'value': dic[idx], 'color': c, 'marker': '', 'edge_color': ec})

with open('data.dat', 'w') as f:
    json.dump(json_t, f)
