#!/usr/bin/python3

'''
Parse csv and generate heatmap graphs for every benchmark

This graphs is compose by 5 graphs: L1D / L2C accuracy, L1D / L2C MPKI, 
L2C PFKI and speedup

@Author : Agustín Navarro Torres
'''

import os
import sys
import json
import subprocess
import numpy as np
from pprint import pprint as ppt

def read_file(fname):
    # Read one file
    trans = {}
    dic   = {}

    with open(fname) as f:
        raw = f.read().split('\n')[:-2]
        for idx, i in enumerate(raw):
            aux = i.split(',')
            if idx == 0: trans = {iidx: ii for iidx, ii in enumerate(aux[:-1])}
            else:
                for iidx, ii in enumerate(aux[:-1]):
                    if iidx == 0: dic[ii] = {}
                    else: 
                        if len(ii) == 1: ii = 0
                        elif len(ii.split('%')) > 1: ii = ii.split('%')[0]
                        dic[aux[0]][trans[iidx]] = float(ii)

    return dic

def gen_json(data, ffile):
    # From data to json data
    dic = []
    for i in data:
        aux = i.split('_')
        if aux[0] != 'L1D': continue
        if data[i] == 0: data[i] = np.nan 
        dic.append({
            'x': int(aux[1]),
            'y': int(aux[3]),
            'value': data[i]
        })
    json.dump(dic, open(ffile, 'w+'))

if __name__ == '__main__':
    dic = {}
    for i in os.listdir('csv/spec'): dic[i] = read_file('csv/spec/{}'.format(i))

    keys = ['l1d_accuracy.csv', 'l2c_accuracy.csv',
            'l1d_mpki.csv', 'l2c_mpki.csv',
            'l1d_pfki.csv', 'l2c_pfki.csv',
            'speedup.csv'
            ]

    # Read basic fonfiguration
    with open('lib/heatmap.json') as f: template = json.load(f)

    for i in dic[keys[0]]: 
        for iidx, ii in enumerate(keys): 
            dx = i
            if i == 'MEAN' and i not in dic[ii]: dx = 'GEOMEAN'
            gen_json(dic[ii][dx], "{}.json".format(ii))
            # template['graphs'][iidx]['dy'] = iidx
            template['graphs'][iidx]['data'] = "{}/{}.json".format(os.getcwd(), ii)
            template['graphs'][iidx]['title'] = "{}\n{}".format(ii.split('.')[0], dx)
        # Generate json data
        json.dump(template, open('tmp.json', 'w+'))

        subprocess.run('lib/made_graph.sh {}.pdf'.format(i), shell=True) 
