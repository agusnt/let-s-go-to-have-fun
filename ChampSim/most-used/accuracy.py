#!/bin/python3
'''
Generate graph and data with the Accuracy in given level

Parameters:
    1 : database file configuration
    2 : graph file configuration (must have a 'level' field with the level: L1D, L2C, LLC)
    3 : google sheet configuration

@Author: Navarro Torres, Agustin
'''

import os
import csv
import sys
import copy
import json
import math
import subprocess
import numpy as np
from pprint import pprint as ppt
from pymongo import MongoClient

__dir_script = os.path.dirname(os.path.realpath(__file__))

# Cast objects to fix types issue with JSON
# From: https://stackoverflow.com/questions/75552548/typeerror-object-of-type-int64-is-not-json-serializable-while-trying-to-conve
def cast_type(container, from_types, to_types):
    if isinstance(container, dict):
        # cast all contents of dictionary 
        return {cast_type(k, from_types, to_types): cast_type(v, from_types, to_types) for k, v in container.items()}
    elif isinstance(container, list):
        # cast all contents of list 
        return [cast_type(item, from_types, to_types) for item in container]
    else:
        for f, t in zip(from_types, to_types):
            # if item is of a type mentioned in from_types,
            # cast it to the corresponding to_types class
            if isinstance(container, f):
                return t(container)
        # None of the above, return without casting 
        return container

def get_from_db(db, info):
    '''
    Connect to the mongo database and return the speedup interesting data

    Generate:
        1 : workload name
        2 : dictionary (key -> binary name), with the geometric mean of all 
            benchmark speedup
        3 : dictionary (key -> binary name), with the geometric mean of all 
            memory intensive benchmark speedup
        4 : dictionary (key -> benchmark name) of dictionary (key -> binary name)
            of all speedup benchmarks
    '''
    # Open the database and collection
    client = MongoClient(db['connect'])
    collection = client[db['db']][db['collection']]

    projection = {'is_mem_int', 'name', 'binary'}
    projection.add('{}.PF.ACCURACY'.format(info['level']))
    projection.add('{}.PF.ACCURACY_LATE'.format(info['level']))

    # Get the workloads
    ret = collection.aggregate([{'$group': {'_id': {'workload': '$workload'}}}])
    workloads = [i['_id']['workload'] for i in ret]

    for i in workloads:
        all = {}
        all_late = {}
        memInt = {}
        memInt_late = {}
        bench = {}
        for ii in collection.find({'workload': i}, projection):
            bin = ii['binary']
            if bin not in all: 
                all[bin] = []
                all_late[bin] = []
                memInt[bin] = []
                memInt_late[bin] = []
            if ii['name'] not in bench: bench[ii['name']] = {}

            # Add the data
            fields = [ii['{}'.format(info['level'])]['PF']['ACCURACY'], 
                      ii['{}'.format(info['level'])]['PF']['ACCURACY_LATE']]
            bench[ii['name']][ii['binary']] = [ii['is_mem_int']] + fields

            all[bin].append(fields[0])
            all_late[bin].append(fields[1])
            if ii['is_mem_int']: 
                memInt[bin].append(fields[0])
                memInt_late[bin].append(fields[1])

        # Get the geomean
        for ii in all:
            all[ii] = np.mean(all[ii])
            all_late[ii] = np.mean(all_late[ii])
            memInt[ii] = np.mean(memInt[ii])
            memInt_late[ii] = np.mean(memInt_late[ii])
        yield i, all, all_late, memInt, memInt_late, bench

    client.close() # Close the connection with mongo

def gen_dat_for_graph(data, data_late, info):
    '''
    Generate data file for the graph

    Parameter:
        data      : information with the data to print
        data_late : information with the data late to print
        info      : dictionary with the information for the json

    Return:
        (min, max) : Y-axis min and maximum value
        axis       : X-axis ticks
        lg         : elements to show in the legend
    '''
    colors    = json.load(open(info['colors']))
    translate = info['translate']
    summary   = True if 'summary' in info and info['summary'] else False
    dat       = []

    def append_data(x, y, v, c, ec, m, l):
        # Function to individual data
        return { 'x': x, 'y': y, 'value': v, 'color': c, 'edge_color': ec, 
                'marker': m, 'legend': l}

    dx = 0
    all = {}

    axis_x = []
    
    lg = []
    
    # Generate data
    for i in sorted(data):
        axis_x.append(i)
        for ii in sorted(data[i]):
            if ii not in translate: continue
            if ii not in all: all[ii] = []
            name = translate[ii]

            dat.append(append_data(dx, data_late[i][ii], name, colors[name]['color'], 
                                   colors[name]['edge_color'], '///', False))
            dat.append(append_data(dx, data[i][ii], name, colors[name]['color'], 
                                   colors[name]['edge_color'], '', True))
            all[ii].append(data[i][ii])

            if name not in lg: lg.append(name) # Legend
        dx += 1
    
    # Append the geomean value
    if summary:
        for i in all:
            name = translate[i]
            dat.append(append_data(dx, all_late[i], name, colors[name]['color'], 
                                   colors[name]['edge_color'], '///', False))
            dat.append(append_data(dx, all[i], name, colors[name]['color'], 
                                   colors[name]['edge_color'], '', True))
    # Write into the file
    json.dump(dat, open('data.dat', 'w+'))
    return axis_x, lg

def gen_graph(info, x, lg, outf):
    '''
    Generate data file for the graph

    Parameter:
        info : dictionary with the information for the json
        x    : xticks for the graph
        lg   : values to write in the legend
        outf : output figure name
    '''
    template = json.load(open('{}/template/accuracy.json'.format(__dir_script)))

    step = 10
    xticks = [i//1 for i in np.arange(0, 101, step)]
    mxticks = [i for i in np.arange(0, 101, step/2)]

    # Y-axis
    template['graphs'][0]['axis']['y']['ticks'] = xticks 
    template['graphs'][0]['axis']['y']['minor_ticks'] = mxticks 
    template['graphs'][0]['axis']['y']['label'] =  '{} {}'.format(
        info['level'], template['graphs'][0]['axis']['y']['label']
    )

    # X-axis
    template['graphs'][0]['axis']['x']['ticks'] = [i for i in range(0, len(x))]
    template['graphs'][0]['axis']['x']['ticks_label'] = x
    template['graphs'][0]['order'] = info['order']
    template['graphs'][0]['order'] = info['order']

    # Legend
    template['graphs'][0]['legend'][0]['elems'] = lg

    # Number of columns by legend
    if 'cols' in info:
        template['graphs'][0]['legend'][0]['args']['ncol'] = info['cols']

    json.dump(cast_type(template, [np.int64, np.float64], [int, float]), open('tmp.json', 'w+'))
    subprocess.run(['{}/../../Figures/gen_fig.py'.format(__dir_script), 'tmp.json', outf])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Need at least 2 arguments: [db file] [graph fil] [gs file]')
        sys.exit()
    if len(sys.argv) >= 4: gs = json.load(open(sys.argv[3]))
    else: gs = None

    config = json.load(open(sys.argv[2]))

    allG = {}
    allG_late = {}
    memIntG = {}
    memIntG_late = {}
    for workload, all, all_late, memInt, memInt_late, toCSV in get_from_db(json.load(open(sys.argv[1])), config):
        print("Getting data for: {}".format(workload))
        header = ['Benchmark', 'Is_Mem_Int']
        data = []
        allG[workload] = copy.deepcopy(all)
        allG_late[workload] = copy.deepcopy(all_late)
        memIntG[workload] = copy.deepcopy(memInt)
        memIntG_late[workload] = copy.deepcopy(memInt_late)

        for jdx, j in enumerate(['ACCURACY', 'ACCURACY_LATE']):
            # Generate header and data for the csv
            for idx, i in enumerate(sorted(toCSV)): 
                foo = [i]
                for ii in sorted(toCSV[i]):
                    if idx == 0: header += [ii]
                    if len(foo) < 2: foo += [toCSV[i][ii][0]]
                    foo += [toCSV[i][ii][1+jdx]]
                data += [foo]

            # Adding the geomean
            foo = ['MEAN_ALL', False]
            bar = ['MEAN', True]
            for i in sorted(all):
                if j == 'ACCURACY':
                    foo += [all[i]]
                    bar += [memInt[i]]
                else:
                    foo += [all_late[i]]
                    bar += [memInt_late[i]]
            data += [foo]
            data += [bar]

            # Write the csv
            with open('{}_PF_{}_{}.csv'.format(config['level'], j, workload), 'w') as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(header)
                csvWriter.writerows(data)

            # Update the information to Google Sheet
            if gs:
                print("Updating google sheet: {}".format(workload))
                subprocess.run(['{}/../../utils/google_sheet_update.py'.format(__dir_script), 
                                gs['name'], '{}_PF_{}_{}.csv'.format(config['level'], j, workload)])

    # Generate the data file
    print("Gen fig")

    for i in [(memIntG, memIntG_late, 'accuracy_{}_mem_int.pdf'.format(config['level'])), 
              (allG, allG_late, 'accuracy_{}_all.pdf'.format(config['level']))]:
        x, lg = gen_dat_for_graph(i[0], i[1], config)
        gen_graph(config, x, lg, i[2])
    
    # Remove temporal files
    print("Deleting temporal files")
    os.remove('data.dat')
    os.remove('tmp.json')
