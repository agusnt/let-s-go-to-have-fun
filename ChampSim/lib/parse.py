#!/usr/bin/env python3

'''
Parse to easily parse all the information that result as output from ChampSim

@Author: Navarro-Torres, Agustin
@Email: agusnt@unizar.es, agusnavarro11@gmail.com

Arguments:
  @1 -> directory to parse
'''

import re
import os
import sys
from pprint import pprint as ppt

def parse_file(fname):
    # Parse an specific file of ChampSim output
    def parse_file_especific(key, line):
        # This sub function is used to parse LLC and core structures
        if key not in dic[core]:
            dic[core][key] = {}

        if ' '.join(line[1:-2]) == "AVERAGE MISS LATENCY:":
            # Get the Miss Latency
            dic[core][key]["AVERAGE MISS LATENCY"] = float(line[-2])
        else:
            # The other information can be easily get
            if line[1] not in dic[core][key]: dic[core][key][line[1]] = {}
            for iidx in range(2, len(line)-1, 2):
                dic[core][key][line[1]][line[iidx].split(':')[0]] =\
                    int(line[iidx+1])

    dic = {}
    with open(fname) as f:
        raw = f.read().split('\n')

        region_of_interest = False
        core = None

        for idx, i in enumerate(raw):
            if i == "Region of Interest Statistics":
                # Try to find the interest par of the simulation
                region_of_interest = True
            elif region_of_interest:
                # We are interested in this part of the output file
                aux = re.sub(' +', ' ', i).split(' ') 

                if aux[0] == "CPU" and aux[2] == "cumulative":
                    # This is the general information
                    core = int(aux[1])
                    dic[core] = {
                        aux[3].split(':')[0]: float(aux[4]),
                        aux[5].split(':')[0]: int(aux[6]),
                        aux[7].split(':')[0]: int(aux[8]),
                    } # Core information
                elif aux[0] == "CPU" and aux[2] == "Branch":
                    # This is general information about Branch
                    dic[core]["BRANCH"] = {
                        "{} (%)".format(aux[4].split(':')[0]): 
                            float(aux[5].split('%')[0]),
                        aux[6].split(':')[0]: float(aux[7]),
                        ' '.join(aux[8:-2]).split(':')[0]: float(aux[-1]),
                    }
                elif aux[0] == "DRAM":
                    # This is DRAM information
                    dic[core]["DRAM"] = {}

                    channel = None
                    for iidx in range(idx+1, len(raw)):
                        aux = re.sub(' +', ' ', raw[iidx]).split(' ')
                        # Get the information about the DRAM
                        if raw[iidx] == "":
                            # We end this part of the file
                            break
                        elif aux[0] == "Channel":
                            # DRAM channel number
                            channel = int(aux[1])
                            dic[core]["DRAM"][channel] = {}
                        else:
                            # Information about this DRAM channel
                            dic[core]["DRAM"][channel][aux[1]] = {}
                            
                            for iiidx in range(2, len(aux)-1, 2):
                                try:
                                    dic[core]["DRAM"][channel][aux[1]]\
                                            [aux[iiidx]] = int(aux[iiidx+1])
                                except:
                                    try:
                                        dic[core]["DRAM"][channel][aux[1]]\
                                                [aux[iiidx]] = float(aux[iiidx+1])
                                    except:
                                        dic[core]["DRAM"][channel][aux[1]]\
                                                [aux[iiidx]] = None
                elif aux[0] == "LLC":
                    # The LLC information
                    parse_file_especific("LLC", aux)
                elif ''.join(aux[0][:3]) == "cpu":
                    # Information of per core structures
                    key = aux[0].split('_')[1]
                    parse_file_especific(key, aux)
    
    return dic

def parse_file_older_champsim(fname):
    # Parse an specific file of ChampSim output (older version)
    dic = {}
    cache_keys = ['L1D', 'L2C', 'LLC', 'ITLB', 'DTLB', 'STLB']
    type_keys  = ['TOTAL', 'LOAD', 'RFO', 'TIMELY', 'PREFETCH']

    with open(fname) as f:
        raw = f.read().split('\n')

        region_of_interest = False
        core = None

        for i in raw:
            # Detect region of interest
            if i == 'Region of Interest Statistics': region_of_interest = True

            if not region_of_interest: continue

            # We are in an interesting region
            aux = re.sub(' +', ' ', i).split(' ') 
            if aux[0] == 'CPU' and aux[2] == 'cumulative': 
                core = int(aux[1])
                dic[core] = {
                        aux[3].split(':')[0]: float(aux[4]),
                        aux[5].split(':')[0]: int(aux[6]),
                        aux[7].split(':')[0]: int(aux[8]),
                    }
            elif aux[0] in cache_keys:
                if aux[0] not in dic[core]: dic[core][aux[0]] = {}
                if aux[1] not in type_keys: continue
                if aux[1] == 'PREFETCH' and aux[2] != 'REQUESTED:': continue
                if aux[1] == 'LOAD' and aux[2] == 'TRANSLATION': continue
                if aux[1] not in dic[core][aux[0]]: dic[core][aux[0]][aux[1]] = {}

                for iidx, ii in enumerate(aux):
                    try:
                        if aux[1] == 'TIMELY':
                            dic[core][aux[0]]['PREFETCH'][ii] = int(aux[iidx+2])
                        else:
                            if (ii.split(':')[0]) == '%': continue
                            dic[core][aux[0]][aux[1]][ii.split(':')[0]] = \
                            int(aux[iidx+1])
                    except: continue
    return dic

def parse_dir(fdir, older=False):
    # Parse all element of a dir, files must follow this format
    # [binary name]---[trace]

    dic = {}
    traces = []

    for i in os.listdir(fdir):
        binary = i.split('---')[0]
        trace  = i.split('---')[1]
        
        if binary not in dic:
            dic[binary] = {}
        if not older:
            dic[binary][trace] = parse_file("{}/{}".format(fdir, i))
        else:
            dic[binary][trace] = parse_file_older_champsim("{}/{}".format(fdir, i))

        if trace not in traces:
            traces.append(trace)

    return dic, traces

if __name__ == "__main__":
    # parse_dir(sys.argv[1])
    parse_file_older_champsim(sys.argv[1])
