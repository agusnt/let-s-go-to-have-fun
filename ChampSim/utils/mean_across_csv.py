#!/usr/bin/python3

'''
Calculate the mean or geomeana of one csv with different suites

Args:
    1 -> file with the different suites
    2 -> 0: Geomean, 1: Mean
'''

import sys
import numpy as np
from scipy.stats import gmean

op = sys.argv[2] # 0 -> geomean, 1 -> mean
data = []
with open(sys.argv[1]) as f:
    raw = f.read().split('\n')
    print(raw[0])
    for i in raw:
        foo = i.split(',')
        if len(foo) == 1: continue
        if foo[0] == 'GEOMEAN': 
            op = 0
            continue
        elif foo[0] == 'MEAN': 
            op = 1
            continue
        elif foo[0] == 'Benchmark': continue
        for iidx, ii in enumerate(foo[1:]):
            if len(data) <= iidx: data.append([])
            if ii == ' ': continue
            data[iidx].append(float(ii))

string = ''
if op == 0: string = 'GEOMEAN'
elif op == 1: string = 'MEAN'

for i in data:
    if len(i) == 0: string = '{}, '.format(string)
    elif op == 0: string = '{},{}'.format(string, gmean(i))
    elif op == 1: string = '{},{}'.format(string, np.mean(i))

print(string)
