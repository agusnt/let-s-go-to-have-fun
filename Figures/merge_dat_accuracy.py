#!/usr/bin/python3

'''
Get two data files of accuracy (first with lates, secondo without lates),
and put slashed as mark in the first one to gen the graph properly.

Args:
    1 -> data file of accuracy with lates
    2 -> data file of accuracy without lates
    3 -> output file
    4 -> marker of lates
'''
import sys
import json

if (len(sys.argv) < 5): mark = '//'
else: mark = sys.argv[4]

f = open(sys.argv[1])
with_late = json.load(f)
f.close()
for i in with_late: i['marker'] = mark

f = open(sys.argv[2])
without_late = json.load(f)
f.close()

with_late = with_late + without_late

with open(sys.argv[3], 'w') as f: json.dump(with_late, f)
