#!/usr/bin/python3

'''
Split the output csv into a csv by file

Arg:
    1 -> name of the original csv file
'''

import sys
import re

with open(sys.argv[1]) as f:
    raw = f.read().split('\n')
    workload_open = ''
    fo = None
    for idx, i in enumerate(raw):
        foo = i.split(',')
        if (foo[0] == 'GEOMEAN' or foo[0] == "MEAN") and fo != None:
            fo.write(i)
            continue
        elif len(foo) < 2: continue
        elif foo[0][0] == 'B': continue
        elif re.search('compute_fp_*', i) and workload_open != 'compute_fp':
            if fo != None: fo.close()
            workload_open = 'compute_fp'
            fo = open('compute_fp.csv', 'w')
            fo.write('{}\n'.format(raw[0]))
        elif re.search('compute_int_*', i) and workload_open != 'compute_int':
            if fo != None: fo.close()
            workload_open = 'compute_int'
            fo = open('compute_int.csv', 'w')
            fo.write('{}\n'.format(raw[0]))
        elif re.search('crypto*', i) and workload_open != 'crypto':
            if fo != None: fo.close()
            workload_open = 'crypto'
            fo = open('crypto.csv', 'w')
            fo.write('{}\n'.format(raw[0]))
        elif re.search('srv*', i) and workload_open != 'srv':
            if fo != None: fo.close()
            workload_open = 'srv'
            fo = open('srv.csv', 'w')
            fo.write('{}\n'.format(raw[0]))
        elif re.search('^6', i) and workload_open != 'spec':
            if fo != None: fo.close()
            workload_open = 'spec'
            fo = open('spec.csv', 'w')
            fo.write('{}\n'.format(raw[0]))
        elif foo[0][0] != 'G' and foo[0][0] != 'B' \
            and not re.search('compute_fp_*', i)\
            and not re.search('compute_int_*', i)\
            and not re.search('crypto*', i)\
            and not re.search('srv*', i)\
            and not re.search('^6', i)\
            and workload_open != 'gap':
            if fo != None: fo.close()
            workload_open = 'gap'
            fo = open('gap.csv', 'w')
            fo.write('{}\n'.format(raw[0]))
        if fo !=None: fo.write('{}\n'.format(i))
    if fo != None: fo.close()
