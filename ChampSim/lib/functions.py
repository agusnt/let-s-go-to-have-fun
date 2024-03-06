#!/usr/bin/env python3

'''
Functions to use in parse

@Author: Navarro-Torres, Agustin
@Email: agusnt@unizar.es, agusnavarro11@gmail.com
'''

# Round limits constants
ROUND_SPEEDUP = 4 
MACRO_ROUND_SPEEDUP = ".{}f".format(ROUND_SPEEDUP)
LEADING_ZEROS_AUX = ROUND_SPEEDUP + 4
LEADING_ZEROS = LEADING_ZEROS_AUX

# CSV Separator
SEPARATOR = ","

import sys
import random
import numpy as np
from scipy.stats import gmean

# Random for the all
RND = str(random.random())

##############################################################################
# Format functions
##############################################################################
def get_head(dic):
    '''
    Return the head string

    Parameter:
        dic : dictionary from parse_dir function
    '''
    head = "Benchmark{}".format(SEPARATOR)
    for ii in sorted(dic):
        # Binary
        head = "{}{}{}".format(head, ii, SEPARATOR) 
    return head

def get_name(long_name):
    '''
    Format the name of the trace

    Parameter:
        long_name : full name of the trace (last /)
    '''
    spec = False
    try:
        int(long_name.split('.')[0])
        spec = True
    except:
        pass

    name = []

    for i in long_name.split('.'):
        if i == "champsimtrace" or i == "trace":
            break

        if spec and len(i.split('-')) > 1:
            i = "{}-{}".format("".join(i[:3]), i.split('-')[-1])
        name.append(i)
    return ".".join(name)

def get_last_line(end, end_values, per=False):
    '''
    Format the last line

    Parameter:
        end : what kind of average use? (MEAN, GEOMEAN)
        end_values : values to calculate the average
        per : show percentage
    '''
    def format(foo, per):
        if not foo: return foo
        if per: return f"{foo:{MACRO_ROUND_SPEEDUP}}%"
        else: return f"{foo:{MACRO_ROUND_SPEEDUP}}"

    last_line = end
    for i in sorted(end_values):
        if i == RND: continue

        if (RND in end_values and len(end_values[RND][i]) != end_values[i]): 
            end_values[i] = end_values[RND][i]

        if end == "GEOMEAN":
            foo = gmean(end_values[i])
            bar = format(foo, per)
            last_line = "{}{}{}".format(last_line, SEPARATOR, bar)
        elif end == "MEAN":
            foo = np.mean(end_values[i]) if len(end_values[i]) != 0 else np.nan 
            bar = format(foo, per)
            last_line = "{}{}{}".format(last_line, SEPARATOR, bar)
        elif end == "SUM":
            foo = np.sum(end_values[i]) 
            bar = format(foo, per)
            last_line = "{}{}{}".format(last_line, SEPARATOR, bar)
    return last_line

##############################################################################
# Auxiliary functions
##############################################################################
def eprint(*args, **kwargs): 
    print(*args, file=sys.stderr, **kwargs)

def values_to_string(end_values, lines, value, name, dx_end_values):
    '''
    Move values to string and end_values string

    Parameters:
        end_values : dictionary to add value
        lines : dictionary of strings
        value : value to add into end_values and lines
        lines : key of lines
        dx_end_values : index of end_values
    '''
    if value: end_values[dx_end_values].append(value)

    if name not in lines: lines[name] = "{}".format(name)

    bar = f"{value:{MACRO_ROUND_SPEEDUP}}" if value else " "
    lines[name] = "{}{}{}".format(lines[name], SEPARATOR, bar)

def values_to_string_per(end_values, lines, value, name, dx_end_values):
    '''
    Move values to string and end_values string

    Parameters:
        end_values : dictionary to add value
        lines : dictionary of strings
        value : value to add into end_values and lines
        lines : key of lines
        dx_end_values : index of end_values
    '''
    if value: end_values[dx_end_values].append(value)

    if name not in lines: lines[name] = "{}".format(name)

    bar = f"{value:{MACRO_ROUND_SPEEDUP}}%" if value else " "
    lines[name] = "{}{}{}".format(lines[name], SEPARATOR, bar)
