#!/bin/python3
'''
Generate graph and data with the MPKI in all levels

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
from pprint import pprint as ppt
from pymongo import MongoClient

__dir_script = os.path.dirname(os.path.realpath(__file__))
levels = ['L1D', 'L2C', 'LLC']

def get_from_db(db):
    '''
    Connect to the mongo database and return the speedup interesting data

    Generate:
        1 : workload name
        2 : dictionary (key -> binary name), with the geometric mean of all 
            benchmark MPKI
        3 : dictionary (key -> binary name), with the geometric mean of all 
            memory intensive benchmark MPKI
        4 : dictionary (key -> benchmark name) of dictionary (key -> binary name)
            of all MPKI benchmarks
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
        for ii in collection.find({'workload': i}, {'is_mem_int', 'name', 
                                                    'L1D.MPKI.DEMAND', 
                                                    'L2C.MPKI.DEMAND',
                                                    'LLC.MPKI.DEMAND', 'binary'}):

            bin = ii['binary']
            if bin not in all: 
                all[bin] = {'L1D': [], 'L2C': [], 'LLC': []}
                memInt[bin] = {'L1D': [], 'L2C': [], 'LLC': []}
            if ii['name'] not in bench: 
                bench[ii['name']] = {}

            # Add the data
            bench[ii['name']][ii['binary']] = {
                'is_mem_int': ii['is_mem_int'],
                'L1D': ii['L1D']['MPKI']['DEMAND'],
                'L2C': ii['L2C']['MPKI']['DEMAND'],
                'LLC': ii['LLC']['MPKI']['DEMAND'],
            }
            all[bin]['L1D'].append(ii['L1D']['MPKI']['DEMAND'])
            all[bin]['L2C'].append(ii['L2C']['MPKI']['DEMAND'])
            all[bin]['LLC'].append(ii['LLC']['MPKI']['DEMAND'])
            if ii['is_mem_int']: 
                memInt[bin]['L1D'].append(ii['L1D']['MPKI']['DEMAND'])
                memInt[bin]['L2C'].append(ii['L2C']['MPKI']['DEMAND'])
                memInt[bin]['LLC'].append(ii['LLC']['MPKI']['DEMAND'])

        # Get the geomean
        for ii in all:
            for iii in all[ii]:
                all[ii][iii] = np.mean(all[ii][iii])
                memInt[ii][iii] = np.mean(memInt[ii][iii])
        yield i, all, memInt, bench

    client.close() # Close the connection with mongo

def gen_dat_for_graph(data, info):
    '''
    Generate data file for the graph

    Parameter:
        data : information with the data to print
        info : dictionary with the information for the json

    Return:
        max  : Y-axis min and maximum value
        axis : X-axis ticks
        lg   : elements to show in the legend
    '''
    colors    = json.load(open(info['colors']))
    translate = info['translate']
    summary   = True if 'summary' in info and info['summary'] else False
    dat       = {}

    def append_data(x, y, v, c, ec, m):
        # Function to individual data
        return { 'x': x, 'y': y, 'value': v, 'color': c, 'edge_color': ec, 'marker': m }

    dx = 0
    all = {}

    max_y = {}
    axis_x = []
    
    lg = []
    
    # Generate data
    for i in data:
        axis_x.append(i)
        for ii in data[i]:
            if ii not in translate: continue
            for iii in data[i][ii]:
                name = translate[ii]
                if iii not in all: all[iii] = {}
                if ii not in all: all[iii][ii] = []
                if iii not in dat: dat[iii] = []

                # Set max values
                if iii not in max_y: max_y[iii] = 0
                if data[i][ii][iii] > max_y[iii]: max_y[iii] = data[i][ii][iii]

                dat[iii].append(append_data(dx, data[i][ii][iii], name, colors[name]['color'], 
                                       colors[name]['edge_color'], colors[name]['mark']))
                all[iii][ii].append(data[i][ii][iii])

                if name not in lg: lg.append(name) # Legend
        dx += 1
    
    # Append the geomean value
    if summary:
        for i in all:
            name = translate[i]
            for ii in all[i]:
                dat[i].append(append_data(dx, all[i][ii], name, colors[name]['color'], 
                                   colors[name]['edge_color'], colors[name]['marker']))
    # Write into the file
    for i in dat: json.dump(dat[i], open('data_{}.dat'.format(i), 'w+'))
    return max_y, axis_x, lg

def gen_graph(info, y, x, lg, outf):
    '''
    Generate data file for the graph

    Parameter:
        info : dictionary with the information for the json
        x    : xticks for the graph
        x    : (min, max) values for the Y-axis
        lg   : values to write in the legend
        outf : output figure name
    '''
    template = json.load(open('{}/template/mpki.json'.format(__dir_script)))

    for idx, i in enumerate(levels):
        max  = math.ceil(y[i])
        min  = 0
        # A maximum of 5 division in multiples of 5
        step = math.ceil(max / 4)
        while (step % 5) != 0: step += 1 # TODO this in a good way
        while (max % step) != 0: max += 1 # TODO: This in a good way

        xticks = [round(i, 2) for i in np.arange(min, max+step/2, step)]
        mxticks = [round(i, 2) for i in np.arange(min, max+step/4, step/2)]
        if xticks[-1] > max: max = xticks[-1]

        # Y-axis
        template['graphs'][idx]['axis']['y']['max'] = max
        template['graphs'][idx]['axis']['y']['min'] = min
        template['graphs'][idx]['axis']['y']['ticks'] = xticks 
        template['graphs'][idx]['axis']['y']['minor_ticks'] = mxticks 
        # Write labelpad if needed
        if len(str(y['L1D']//1)) > len(str(y[i]//1)):
            inc = 11.0 * (len(str(y['L1D']//1)) - len(str(y[i]//1)))
            template['graphs'][idx]['axis']['y']['args_txt_label'] = {'labelpad': inc}

        # X-axis
        if idx == 2:
            template['graphs'][idx]['axis']['x']['ticks_label'] = x
        else:
            template['graphs'][idx]['axis']['x']['ticks_label'] = []
        template['graphs'][idx]['axis']['x']['ticks'] = [i for i in range(0, len(x))]
        template['graphs'][idx]['order'] = info['order']
        template['graphs'][idx]['order'] = info['order']

    # Legend
    template['graphs'][0]['legend'][0]['elems'] = lg

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

        for level in levels:
            # Generate header and data for the csv
            for idx, i in enumerate(sorted(toCSV)): 
                foo = [i]
                for ii in sorted(toCSV[i]):
                    if idx == 0: header += [ii]
                    if len(foo) < 2: foo += [toCSV[i][ii]['is_mem_int']]
                    foo += [toCSV[i][ii][level]]
                data += [foo]

            # Adding the geomean
            foo = ['GEOMEAN_ALL', False]
            bar = ['GEOMEAN', True]
            for i in sorted(all):
                foo += [all[i][level]]
                bar += [memInt[i][level]]
            data += [foo]
            data += [bar]

            # Write the csv
            with open('mpki_{}_{}.csv'.format(level, workload), 'w') as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(header)
                csvWriter.writerows(data)

            # Update the information to Google Sheet
            if gs:
                print("Updating google sheet: {}".format(workload))
                subprocess.run(['{}/../../utils/google_sheet_update.py'.format(__dir_script), 
                                gs['name'], 'mpki_{}_{}.csv'.format(level, workload)])

    # Generate the data file
    print("Gen fig")
    config = json.load(open(sys.argv[2]))
    for i in [(memIntG, 'mem_mem_int.pdf'), (allG, 'mem_all.pdf')]:
        y, x, lg = gen_dat_for_graph(i[0], config)
        gen_graph(config, y, x, lg, i[1])
    
    # Remove temporal files
    print("Deleting temporal files")
    for i in levels: os.remove('data_{}.dat'.format(i))
    os.remove('tmp.json')
