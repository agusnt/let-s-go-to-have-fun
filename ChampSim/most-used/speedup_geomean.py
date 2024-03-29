#!/bin/python3
'''
Generate graph and data with the geomean speedup

Parameters:
    1 : database file configuration
    2 : graph file configuration
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
from scipy.stats import gmean
from pprint import pprint as ppt
from pymongo import MongoClient

__dir_script = os.path.dirname(os.path.realpath(__file__))

def get_from_db(db):
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

    # Get the workloads
    ret = collection.aggregate([{'$group': {'_id': {'workload': '$workload'}}}])
    workloads = [i['_id']['workload'] for i in ret]

    for i in workloads:
        all = {}
        memInt = {}
        bench = {}
        for ii in collection.find({'workload': i}, {'is_mem_int', 'name', 'speedup', 'binary'}):
            bin = ii['binary']
            if bin not in all: 
                all[bin] = []
                memInt[bin] = []
            if ii['name'] not in bench: bench[ii['name']] = {}

            # Add the data
            bench[ii['name']][ii['binary']] = (ii['is_mem_int'], ii['speedup'])
            all[bin].append(ii['speedup'])
            if ii['is_mem_int']: memInt[bin].append(ii['speedup'])

        # Get the geomean
        for ii in all:
            all[ii] = gmean(all[ii])
            memInt[ii] = gmean(memInt[ii])
        yield i, all, memInt, bench

    client.close() # Close the connection with mongo

def gen_dat_for_graph(data, info):
    '''
    Generate data file for the graph

    Parameter:
        data : information with the data to print
        info : dictionary with the information for the json

    Return:
        (min, max) : Y-axis min and maximum value
        axis       : X-axis ticks
        lg         : elements to show in the legend
    '''
    colors    = json.load(open(info['colors']))
    translate = info['translate']
    summary   = True if 'summary' in info and info['summary'] else False
    dat       = []

    def append_data(x, y, v, c, ec, m):
        # Function to individual data
        return { 'x': x, 'y': y, 'value': v, 'color': c, 'edge_color': ec, 'marker': m }

    dx = 0
    all = {}

    min_y = {}
    max_y = {}
    axis_x = []
    
    lg = []
    
    # Generate data
    for i in sorted(data):
        axis_x.append(i)
        for ii in sorted(data[i]):
            if ii not in translate: continue
            if ii not in all: all[ii] = []
            name = translate[ii]

            # Set min and max values
            if ii not in min_y: min_y[ii] = data[i][ii]
            elif data[i][ii] < min_y[ii]: min_y[ii] = data[i][ii]
            if ii not in max_y: max_y[ii] = data[i][ii]
            elif data[i][ii] > max_y[ii]: max_y[ii] = data[i][ii]

            dat.append(append_data(dx, data[i][ii], name, colors[name]['color'], 
                                   colors[name]['edge_color'], colors[name]['mark']))
            all[ii].append(data[i][ii])

            if name not in lg: lg.append(name) # Legend
        dx += 1
    
    # Append the geomean value
    if summary:
        for i in all:
            name = translate[i]
            dat.append(append_data(dx, all[i], name, colors[name]['color'], 
                                   colors[name]['edge_color'], colors[name]['marker']))
    # Write into the file
    json.dump(dat, open('data.dat', 'w+'))
    return (min_y, max_y), axis_x, lg

def gen_graph(info, y, x, lg, outf):
    '''
    Generate data file for the graph

    Parameter:
        info : dictionary with the information for the json
        y    : (min, max) values for the Y-axis
        x    : xticks for the graph
        lg   : values to write in the legend
        outf : output figure name
    '''
    factor = 10 ** 2
    template = json.load(open('{}/template/speedup.json'.format(__dir_script)))
    # Get axis X values (with 5 steps)
    max = 0
    min = sys.maxsize
    for i in y[0]:
        if info['translate'][i] not in info['order']: continue
        if y[0][i] > max: max = y[0][i]
        if y[1][i] < min: min = y[1][i]
    max  = math.ceil(max * factor) / factor
    min  = math.floor(min * factor) / factor
    step = 0.05
    if min > 0.95: min = 0.95
    if max < 1.05: max = 1.05
    xticks = [round(i, 2) for i in np.arange(min, max+step/2, step)]
    mxticks = [round(i, 2) for i in np.arange(min, max+step/4, step/2)]
    if xticks[-1] > max: max = xticks[-1]

    # Y-axis
    template['graphs'][0]['axis']['y']['max'] = max
    template['graphs'][0]['axis']['y']['min'] = min
    template['graphs'][0]['axis']['y']['ticks'] = xticks 
    template['graphs'][0]['axis']['y']['minor_ticks'] = mxticks 

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

    json.dump(template, open('tmp.json', 'w+'))
    subprocess.run(['{}/../../Figures/gen_fig.py'.format(__dir_script), 'tmp.json', outf])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Need at least 2 arguments: [db file] [graph fil] [gs file]')
        sys.exit()
    if len(sys.argv) >= 4: gs = json.load(open(sys.argv[3]))
    else: gs = None

    allG = {}
    memIntG = {}
    for workload, all, memInt, toCSV in get_from_db(json.load(open(sys.argv[1]))):
        print("Getting data for: {}".format(workload))
        header = ['Benchmark', 'Is_Mem_Int']
        data = []
        allG[workload] = copy.deepcopy(all)
        memIntG[workload] = copy.deepcopy(memInt)

        # Generate header and data for the csv
        for idx, i in enumerate(sorted(toCSV)): 
            foo = [i]
            for ii in sorted(toCSV[i]):
                if idx == 0: header += [ii]
                if len(foo) < 2: foo += [toCSV[i][ii][0]]
                foo += [toCSV[i][ii][1]]
            data += [foo]

        # Adding the geomean
        foo = ['GEOMEAN_ALL', False]
        bar = ['GEOMEAN', True]
        for i in sorted(all):
            foo += [all[i]]
            bar += [memInt[i]]
        data += [foo]
        data += [bar]

        # Write the csv
        with open('speedup_{}.csv'.format(workload), 'w') as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow(header)
            csvWriter.writerows(data)

        # Update the information to Google Sheet
        if gs:
            print("Updating google sheet: {}".format(workload))
            subprocess.run(['{}/../../utils/google_sheet_update.py'.format(__dir_script), 
                            gs['name'], 'speedup_{}.csv'.format(workload)])


    # Generate the data file
    print("Gen fig")

    config = json.load(open(sys.argv[2]))
    for i in [(memIntG, 'speedup_mem_int.pdf'), (allG, 'speedup_all.pdf')]:
        y, x, lg = gen_dat_for_graph(i[0], config)
        gen_graph(config, y, x, lg, i[1])
    
    # Remove temporal files
    print("Deleting temporal files")
    os.remove('data.dat')
    os.remove('tmp.json')
