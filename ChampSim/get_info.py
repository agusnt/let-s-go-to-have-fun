#!/usr/bin/env python3

'''
Parse ChampSim outputs to csv

Enviaromental Vars:
    OLD_CHAMPSIM if has value it means tha you are using and older version of
    champsim, and some of the stats maybe will not work

Arguments:
  @1 -> directory to parse
  @2 -> What to get from this information, see options in comment below

@Author: Navarro-Torres, Agustin 
@Email: agusnt@unizar.es, agusnavarro11@gmail.com

Options to get information:
  - speedup: speedup of all benchmarks
       @3 -> Base elements
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - mpki: demand mpki X cache level
       @3 -> level of cache
       @4 -> event for mpki (LOAD) with underline
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - apki: demand apki X cache level
       @3 -> level of cache
       @4 -> event for mpki (LOAD) with underline
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - hpki: demand hpki X cache level
       @3 -> level of cache
       @4 -> event for mpki (LOAD) with underline
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - pfki: prefetch per kilo instruction
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - queues: full every one thousand access for queues
       @3 -> queue type (RQ, WQ, PQ, PTWQ) 
       @4 -> level of cache
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - accuracy: prefetch accuracy X cache level
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - accuracy_late: prefetch accuracy including late X cache level
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - latency: get average latency
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - branch_accuracy: get branch accuracy
       @3 -> Y for memory intensive, N for normal
       @4 -> Memory intensive base
  - branch_mpki: get branch MPKI 
       @3 -> Y for memory intensive, N for normal
       @4 -> Memory intensive base
  - branch_mpki: get average ROB occupancy at branch miss prediction
       @3 -> Y for memory intensive, N for normal
       @4 -> Memory intensive base
  - energy: get energy values (miliJules)
       @3 -> memory levels, separated by _ (e.g.: L1D_L2C_LLC_DRAM)
       @4 -> energy file
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - rel_energy: get relative energy
       @3 -> memory levels, separated by _ (e.g.: L1D_L2C_LLC_DRAM)
       @4 -> energy file
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - db: add everything into the database
       @3 -> JSON with the information
       @4 -> JSON with the extra information to add (json file)
'''

import os
import sys
import json 
import copy


import lib.parse
from lib.functions import *

from pymongo import MongoClient
from pprint import pprint as ppt


# Other constants
LLC_MEM_INT = 1

# Min prefetch (Minimun of prefetch to calculate accuracy)
MIN_PREF = 0

ENERGY_FILE = ''

##############################################################################
# Get data functions
##############################################################################
def do_speedup(binary, base): return [binary[i]["IPC"] / base[i]["IPC"] for i in binary]

def do_pki(first, second): 
    if second == 0: return 0
    return first / (second/1000)

def do_mem_intensive(miss, instr): return do_pki(miss, instr) > LLC_MEM_INT 

def do_is_mem_intensive(base_llc):
    '''
    Return true if the trace is intensive
    
    Parameter:
        base_llc : data to calculate memory intensive benchmark
    '''
    if (len(base_llc) > 1): return True
    miss = base_llc[0]["LLC"]["LOAD"]["MISS"]
    instr = base_llc[0]["instructions"]
    return do_mem_intensive(miss, instr)

def do_is_mem_intensive_cond(base_llc, dic):
    '''
    Return true if the trace is intensive
    
    Parameter:
        base_llc : base to calculate memory intensive benchmark
        dic : data to calculate memory intensive benchmark
    '''
    return not base_llc or do_is_mem_intensive(dic)

def do_sum(dic, event, events):
    '''
    Calculate the total events of demand access

    Paramters:
        dic : dictionary with the values
    '''
    total = 0

    if event: 
        for i in events: 
            if i in dic and event in dic[i]: total += dic[i][event]
    else: 
        for i in events: 
            if i in dic: total += dic[i]

    return total

def do_energy(dic, dx_2, dx_1, levels):
    '''
    Calculate energy

    Parameters:
        dic : dictionary from parse_dir function
        dx_1, dx_2 : access index for array
        levels : cache_level
    '''

    energy = json.load(open(ENERGY_FILE))
    wb_energy = ["L2C", "LLC"] # Levels to calculate wb energy
    total = 0

    for i in levels: # Calculate energy per cache level
        if i == "DRAM":
            total += dic[dx_2][dx_1][0]["LLC"]["TOTAL"]["MISS"] * energy[i]
            continue
        # Tag energy
        tag   = dic[dx_2][dx_1][0][i]["TOTAL"]["ACCESS"] * energy[i]["TAG"]
        # Read energy
        read  = (dic[dx_2][dx_1][0][i]["TOTAL"]["HIT"] + \
                dic[dx_2][dx_1][0][i]["TOTAL"]["MISS"]) * energy[i]["READ"]
        # Write energy
        write = dic[dx_2][dx_1][0][i]["TOTAL"]["MISS"] * energy[i]["WRITE"]
        # Write back energy 
        if i in wb_energy:
            wb = (dic[dx_2][dx_1][0][i]["WRITE"]["MISS"] + \
                    dic[dx_2][dx_1][0][i]["WRITE"]["HIT"]) * energy[i]["WRITE"]
        else: wb = 0
        # Total energy
        total += (tag + read + write + wb)

    return total

def speedup(dic, base, name, lines, end_values, dx_1, dx_2, base_llc=None):
    '''
    Get speedup 

    Parameters:
        dic : dictionary from parse_dir function
        base : base for the speedup
        name : array with the names
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
    '''
    if not base_llc or do_is_mem_intensive(dic[base_llc][dx_1]):
        foo = do_speedup(dic[dx_2][dx_1], dic[base][dx_1])
        if RND not in end_values: end_values[RND] = {}
        if dx_2 not in end_values[RND]: end_values[RND][dx_2] = []
        end_values[RND][dx_2] += foo
        foo = gmean(foo) if (len(foo) > 1) else foo[0]
        values_to_string(end_values, lines, foo, name, dx_2)

    return lines, end_values

def cache_pki(dic, level, event, name, lines, end_values, dx_1, dx_2, events, base_llc=None):
    '''
    Get speedup

    Parameters:
        dic : dictionary from parse_dir function
        level : cache_level
        event : event to measure (MISS, ACCESS, HIT)
        name : array with the names
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
    '''
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        total_event = do_sum(dic[dx_2][dx_1][0][level], event, events)
        foo = do_pki(total_event, dic[dx_2][dx_1][0]["instructions"])

        values_to_string(end_values, lines, foo, name, dx_2)

    return lines, end_values

def cache_pfki(dic, level, name, lines, end_values, dx_1, dx_2, base_llc=None):
    '''
    Get speedup

    Parameters:
        dic : dictionary from parse_dir function
        level : cache_level
        name : array with the names
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
    '''
    events = ["USEFUL", "LATE", "USELESS"]
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        total_event = do_sum(dic[dx_2][dx_1][0][level]["PREFETCH"], None, events)
        foo = do_pki(total_event, dic[dx_2][dx_1][0]["instructions"])
        values_to_string(end_values, lines, foo, name, dx_2)

    return lines, end_values

def queues_pki(dic, queue, level, name, lines, end_values, dx_1, dx_2, base_llc=None):
    '''
    Get speedup

    Parameters:
        dic : dictionary from parse_dir function
        queue : queue type
        level : cache_level
        event : event to measure (MISS, ACCESS, HIT)
        name : array with the names
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
    '''
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        access_event = dic[dx_2][dx_1][0][level][queue]["ACCESS"]
        full_event = dic[dx_2][dx_1][0][level][queue]["FULL"]
        foo = do_pki(full_event, access_event)

        values_to_string(end_values, lines, foo, name, dx_2)

    return lines, end_values

def accuracy_prefetch(dic, level, name, lines, end_values, dx_1, dx_2, base_llc=None, late=False):
    '''
    Get prefetch accuracy 

    Parameters:
        dic : dictionary from parse_dir function
        level : cache_level
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
        late : include late prefetchers
    '''
    events = ["USEFUL", "LATE"] if late else ["USEFUL"]
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        total_pf = do_sum(dic[dx_2][dx_1][0][level]["PREFETCH"], None, ["USEFUL", "LATE", "USELESS"])
        pf = do_sum(dic[dx_2][dx_1][0][level]["PREFETCH"], None, events)
        foo = (pf / total_pf) * 100 if total_pf > MIN_PREF else None 

        values_to_string_per(end_values, lines, foo, name, dx_2)

    return lines, end_values

def latency(dic, level, name, lines, end_values, dx_1, dx_2, base_llc=None):
    '''
    Get prefetch accuracy 

    Parameters:
        dic : dictionary from parse_dir function
        level : cache_level
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
    '''
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        foo = dic[dx_2][dx_1][0][level]["AVERAGE MISS LATENCY"]

        values_to_string(end_values, lines, foo, name, dx_2)

    return lines, end_values

def accuracy_branch(dic, name, lines, end_values, dx_1, dx_2, base_llc=None):
    '''
    Get branch accuracy 

    Parameters:
        dic : dictionary from parse_dir function
        level : cache_level
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
        late : include late prefetchers
    '''
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        foo = dic[dx_2][dx_1][0]['BRANCH']['Accuracy (%)']
        values_to_string_per(end_values, lines, foo, name, dx_2)

    return lines, end_values

def mpki_branch(dic, name, lines, end_values, dx_1, dx_2, base_llc=None):
    '''
    Get branch accuracy 

    Parameters:
        dic : dictionary from parse_dir function
        level : cache_level
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
        late : include late prefetchers
    '''
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        foo = dic[dx_2][dx_1][0]['BRANCH']['MPKI']
        values_to_string(end_values, lines, foo, name, dx_2)

    return lines, end_values

def rob_branch(dic, name, lines, end_values, dx_1, dx_2, base_llc=None):
    '''
    Get branch accuracy 

    Parameters:
        dic : dictionary from parse_dir function
        level : cache_level
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        base_llc : base for the selecting if the trace is memory intensive
        late : include late prefetchers
    '''
    if not base_llc or do_is_mem_intensive_cond(base_llc, dic[base_llc][dx_1]):
        foo = dic[dx_2][dx_1][0]['BRANCH']['Average ROB Occupancy at']
        values_to_string(end_values, lines, foo, name, dx_2)

    return lines, end_values

def energy(dic, name, lines, end_values, dx_1, dx_2, levels, base_llc=None):
    '''
    Get energy

    Parameters:
        dic : dictionary from parse_dir function
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        levels : cache_level
        base_llc : base for the selecting if the trace is memory intensive
    '''

    # Read energy values
    
    if not base_llc or do_is_mem_intensive(dic[base_llc][dx_1]):
        total = do_energy(dic, dx_2, dx_1, levels)
           
        # total = (total * 10**-9) # Total Energy (Julios)
        total = (total * 10**-6) # Total Energy (miliJulios)
        values_to_string(end_values, lines, total, name, dx_2)
    return lines, end_values

def rel_energy(dic, base, name, lines, end_values, dx_1, dx_2, levels, base_llc=None):
    '''
    Get relative energy

    Parameters:
        dic : dictionary from parse_dir function
        base : base for the relative
        lines : array with the lines that will be printed
        end_values : list with the speedup values
        dx_1, dx_2 : access index for array
        levels : cache_level
        base_llc : base for the selecting if the trace is memory intensive
    '''

    # Read energy values
    
    if not base_llc or do_is_mem_intensive(dic[base_llc][dx_1]):
        total_base = do_energy(dic, base, dx_1, levels)
        total = do_energy(dic, dx_2, dx_1, levels)
           
        # total = (total * 10**-9) # Total Energy (Julios)
        aux = total / total_base # Total Energy (miliJulios)
        values_to_string(end_values, lines, aux, name, dx_2)
    return lines, end_values

def db(dic, trace, info, workload):
    '''
    Dump all information into the database. This only works for single thread
    traces.

    TODO: made it works for multi-thread simulations

    Parameters:
        dic : dictionary from parse_dir function
        trace :
        info : json with all the information to insert into the database
        workload : workload
    '''
    def try_catch_insert_dic(dic_ins, key, value):
        '''
        Try to convert a value to a float and insert it into a dictionary
        if it cant it will insert a 0.

        The value is the return line of a function

        Parameters:
            dic_ins -> dictionary to insert
            key -> key to insert into the dictionary
            value -> value to try to convert
        '''
        try: dic_ins[key] = float(value[list(value.keys())[0]].split(',')[-1].replace('%', ''))
        except: dic_ins[key] = 0
        return dic_ins

    client = MongoClient(info['connect'])
    print("Connected to DB")

    db = client[info['db']] # Connect to DB
    # Check if collection exists
    collection = db[info['collection']] # Connect to collection
    if 'del' in info and info['del'] and info['collection'] in db.list_collection_names(): 
        print("Erase collection to avoid future duplicated issues")
        collection.drop() # Remove collection that already exists

    base = info['base'] # Base calculation for the speedup

    foo = {} # This is a useless var that I need
    data = [] # Index of the data

    print("Populating DB")
    for idx, i in enumerate(sorted(trace)):
        print ("Loading {} of {}".format(idx, len(trace)), end="\r")
        name = get_name(i)

        for ii in sorted(dic):
            if ii not in foo: foo[ii] = [] 
            element = {}
            element['name'] = name
            element['workload'] = workload
            element['binary'] = ii

            # Speedup
            bar, _ = speedup(dic, base, name, {}, foo, i, ii)
            try_catch_insert_dic(element, 'speedup', bar)

            if info['multicore']: 
                data.append(copy.deepcopy(element))
                continue # TODO: Implement metrics for multicore

            # Events of cache
            events = {'DEMAND': ['LOAD', 'RFO', 'WRITE'], 'LOAD': ['LOAD'], 
                      'PREFETCH': ['PREFETCH'], 'TRANSLATION': ['TRANSLATION'],
                      'WRITE': ['WRITE'], 'RFO': ['RFO'],
                      'ALL': ['LOAD', 'RFO', 'WRITE', 'TRANSLATION', 'PREFETCH']}
            for j in ['L1D', 'L2C', 'LLC', 'ITLB', 'DTLB', 'STLB']:
                # PKI of all caches
                if j not in element: element[j] = {}
                # MISS/ACCESS/HIT
                types = {'MISS': 'MPKI', 'ACCESS': 'APKI', 'HIT': 'HPKI'}
                for jj in types:
                    element[j][types[jj]] = {} 
                    for jjj in events:
                        # All possible events
                        bar, _ = cache_pki(dic, j, jj, name, {}, foo, i, ii, events[jjj])
                        try_catch_insert_dic(element[j][types[jj]], jjj, bar)

                if 'PF' not in element[j]: element[j]['PF'] = {}
                # PFKI
                bar, _ = cache_pfki(dic, j, name, {}, foo, i, ii)
                try_catch_insert_dic(element[j]['PF'], 'PFKI', bar)
                # Accuracy
                bar, _ = accuracy_prefetch(dic, j, name, {}, foo, i, ii) 
                try_catch_insert_dic(element[j]['PF'], 'ACCURACY', bar)
                bar, _ = accuracy_prefetch(dic, j, name, {}, foo, i, ii, late=True)
                try_catch_insert_dic(element[j]['PF'], 'ACCURACY_LATE', bar)
                # Latency
                bar, _ = latency(dic, j, name, {}, foo, i, ii)
                try_catch_insert_dic(element[j], 'LATENCY', bar)
                # TODO: Queues information
            # Branch
            key = 'Branch'
            if key not in element: element[key] = {}
            # Accuracy
            bar, _ = accuracy_branch(dic, name, {}, foo, i, ii)
            try_catch_insert_dic(element[key], 'ACCURACY', bar)
            # MPKI
            bar, _ = mpki_branch(dic, name, {}, foo, i, ii)
            try_catch_insert_dic(element[key], 'MPKI', bar)
            # ROB
            bar, _ = rob_branch(dic, name, {}, foo, i, ii)
            try_catch_insert_dic(element[key], 'ROB', bar)

            # Raw data
            element['raw'] = dic[ii][i][0]

            # We want to know if this is memory intensive or not
            if 'base_llc' in info:
                if do_is_mem_intensive(dic[info['base_llc']][i]):
                    element['is_mem_int'] = True
                else: element['is_mem_int'] = False
            # Save the data to insert into the database later
            data.append(copy.deepcopy(element))

    # Inserting into the database
    collection.insert_many(data)

    print("Loaded  {} of {}".format(len(trace), len(trace)))
    client.close()

##############################################################################
# Main
##############################################################################
if __name__ == "__main__":
    old_champ = True if 'OLD_CHAMPSIM' in os.environ else False
    base_llc = None
    percentage = False
    analyze = sys.argv[2]
    dic, trace = lib.parse.parse_dir(sys.argv[1], older=old_champ)
    
    # Stdout
    head = get_head(dic)
    last_line = ""
    lines = {}
    end_values = {} 
    end = ""

    # We dump the raw data into a database
    if sys.argv[2] == "db":
        db(dic, trace, json.load(open(sys.argv[3])), sys.argv[4])
        sys.exit(0)

    # Iterate over traces 
    for i in sorted(trace):
        # Get name of trace
        name = get_name(i)

        for ii in sorted(dic):
            # Save values for average
            if ii not in end_values: end_values[ii] = [] 

            if sys.argv[2] == "speedup":
                # Speedup
                end = "GEOMEAN"
                if sys.argv[4] == "Y": base_llc = sys.argv[5]
                speedup(dic, sys.argv[3], name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "mpki":
                events = sys.argv[4].split('_')
                end = "MEAN"
                if sys.argv[5] == "Y": base_llc = sys.argv[6]
                cache_pki(dic, sys.argv[3], 'MISS', name, lines, end_values, i, ii, events, base_llc=base_llc)
            elif sys.argv[2] == "apki":
                events = sys.argv[4].split('_')
                end = "MEAN"
                if sys.argv[5] == "Y": base_llc = sys.argv[6]
                cache_pki(dic, sys.argv[3], 'ACCESS', name, lines, end_values, i, ii, events, base_llc=base_llc)
            elif sys.argv[2] == "hpki":
                events = sys.argv[4].split('_')
                end = "MEAN"
                if sys.argv[5] == "Y": base_llc = sys.argv[6]
                cache_pki(dic, sys.argv[3], 'HIT', name, lines, end_values, i, ii, events, base_llc=base_llc)
            elif sys.argv[2] == "pfki":
                end = "MEAN"
                if sys.argv[4] == "Y": base_llc = sys.argv[5]
                cache_pfki(dic, sys.argv[3], name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "queues":
                end = "MEAN"
                if sys.argv[5] == "Y": base_llc = sys.argv[6]
                queues_pki(dic, sys.argv[4], sys.argv[3], name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "accuracy":
                percentage = True
                end = "MEAN"
                if sys.argv[4] == "Y": base_llc = sys.argv[5]
                accuracy_prefetch(dic, sys.argv[3], name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "accuracy_late":
                percentage = True
                end = "MEAN"
                if sys.argv[4] == "Y": base_llc = sys.argv[5]
                accuracy_prefetch(dic, sys.argv[3], name, lines, end_values, i, ii, base_llc=base_llc, late=True)
            elif sys.argv[2] == "latency":
                LEADING_ZEROS = LEADING_ZEROS_AUX + 2
                end = "MEAN"
                if sys.argv[4] == "Y": base_llc = sys.argv[5]
                latency(dic, sys.argv[3], name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "branch_accuracy":
                percentage = True
                end = "MEAN"
                if sys.argv[3] == "Y": base_llc = sys.argv[4]
                accuracy_branch(dic, name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "branch_mpki":
                end = "MEAN"
                if sys.argv[3] == "Y": base_llc = sys.argv[4]
                mpki_branch(dic, name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "branch_rob":
                end = "MEAN"
                if sys.argv[3] == "Y": base_llc = sys.argv[4]
                rob_branch(dic, name, lines, end_values, i, ii, base_llc=base_llc)
            elif sys.argv[2] == "energy":
                levels = sys.argv[3].split('_')
                end = "MEAN"
                ENERGY_FILE = sys.argv[4]
                if sys.argv[5] == "Y": base_llc = sys.argv[6]
                energy(dic, name, lines, end_values, i, ii, levels, base_llc=base_llc)
            elif sys.argv[2] == "rel_energy":
                levels = sys.argv[4].split('_')
                end = "GEOMEAN"
                ENERGY_FILE = sys.argv[5]
                if sys.argv[6] == "Y": base_llc = sys.argv[7]
                rel_energy(dic, sys.argv[3], name, lines, end_values, i, ii, levels, base_llc=base_llc)
            else:
                eprint("Unknown parameter")                
                sys.exit(1)
        
    # Get last_line
    last_line = get_last_line(end, end_values, per=percentage)

    # Print information
    print(head)
    for i in sorted(lines): print(lines[i])
    print(last_line)
    print(head)
