#!/usr/bin/env python3

'''
Generate and xlsx from csv files generated with bash scripts (../../bash/ChampSim)

Arguments:
  @1   -> Output workbook
  @2:n -> all inputs with information

@Author: Navarro-Torres, Agustin 
@Email: agusnavarro11@gmail.com

'''

import sys
import numpy as np
import xlsxwriter as xlsx

def parse_file(fname):
    '''
    Parse CSV file and get the final data

    Parameters:
        @1 : filename
    '''

    dic        = {}
    dx_to_name = {}

    with open(fname) as f:
        # Read file
        raw = f.read().split('\n')

        for i in raw:
            i = i.split(',')

            parse_names = False
            parse_data  = False

            if i[0] == 'Benchmark': parse_names = True
            elif i[0] == 'GEOMEAN' or i[0] == 'MEAN' or i[0] == 'SUM': parse_data = True

            for iidx, ii in enumerate(i):
                if parse_names: dx_to_name[iidx] = ii
                if parse_data:  dic[dx_to_name[iidx]] = ii

    del dic['Benchmark'] # Remove benchmark key
    return dic

def gen_xlsx(fname, name, data, columns_padding=3):
    '''
    '''
    if gen_xlsx.init != True:
        # Create a workbook
        gen_xlsx.workbook = xlsx.Workbook(fname)
        gen_xlsx.worksheet = gen_xlsx.workbook.add_worksheet()
        gen_xlsx.init = True # We only generate the workbook at the beginning

        # Formats
        gen_xlsx.bold_center = gen_xlsx.workbook.add_format({'bold': True, 
            'border': 1, 'align': 'center'})
        gen_xlsx.italic_center = gen_xlsx.workbook.add_format({'italic': True, 
            'border': 1, 'align': 'center'})
        gen_xlsx.italic_center_middle = gen_xlsx.workbook.add_format({
            'italic': True, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        gen_xlsx.format_float = gen_xlsx.workbook.add_format({
            'num_format': '#,###0.000', 'border': 1})
        gen_xlsx.format_percent = gen_xlsx.workbook.add_format({
            'num_format': '##,##00.00%', 'border': 1})

        # Another interesting objects
        gen_xlsx.row = 0
        gen_xlsx.table = np.empty([256, 256], dtype=object)
        gen_xlsx.end_merge = {}

        # First row
        for idx, i in enumerate(data):
            gen_xlsx.worksheet.write(gen_xlsx.row, columns_padding+idx, i, 
                                     gen_xlsx.bold_center)
            # Save in our table
            gen_xlsx.table[gen_xlsx.row][columns_padding+idx] = i

    gen_xlsx.row += 1 # Increase actual row

    padding_f_col = columns_padding-len(name)
    for idx, i in enumerate(name):
        # if wfirstcolumn and idx == 0: continue # We already write the first column
        gen_xlsx.worksheet.write(gen_xlsx.row, idx+padding_f_col, i, gen_xlsx.italic_center)
        gen_xlsx.table[gen_xlsx.row][idx] = i # Save in our table

    if (padding_f_col > 0):
        # We save the first merge
        gen_xlsx.end_merge[(gen_xlsx.row, 0)] =\
            (gen_xlsx.row, 0, gen_xlsx.row, padding_f_col, name[0], 
             gen_xlsx.italic_center_middle)

    # Do we need to merge upper columns?
    for i in range(0, len(name)):
        merge_level = 0
        for ii in reversed(range(0, gen_xlsx.row)):
            if gen_xlsx.table[gen_xlsx.row][i] == gen_xlsx.table[ii][i] and\
                gen_xlsx.table[gen_xlsx.row][i] and gen_xlsx.table[ii][i]:
                # The upper cell must be merge
                merge_level += 1;
            else: break # The upper cell must not be merge

        if merge_level > 0:
            # Max row to merge
            max_row = padding_f_col if i == 0 else i+padding_f_col

            # We save the merge, we will always save the biggest merge
            gen_xlsx.end_merge[(gen_xlsx.row-merge_level, i)] =\
                    (gen_xlsx.row-merge_level, i, gen_xlsx.row, 
                     max_row, name[i], gen_xlsx.italic_center_middle)

            # Avoid multiple merge over the same cells
            if i == 0 and (gen_xlsx.row, 0) in gen_xlsx.end_merge: 
                del gen_xlsx.end_merge[(gen_xlsx.row, 0)]
        
    # Write Data
    for idx, i in enumerate(data):
        if data[i][-1] != '%':
            gen_xlsx.worksheet.write(gen_xlsx.row, columns_padding+idx, 
                float(data[i]), gen_xlsx.format_float)
            # Save in our tabl
            gen_xlsx.table[gen_xlsx.row][columns_padding+idx] = data[i]
        else:
            if ''.join(data[i][0:3]) == "nan":
                gen_xlsx.worksheet.write(gen_xlsx.row, columns_padding+idx, '')
                # Save in our table
                gen_xlsx.table[gen_xlsx.row][columns_padding+idx] = None
            else:
                bar = float(''.join(data[i][:-1])) / 100
                gen_xlsx.worksheet.write(gen_xlsx.row, columns_padding+idx, bar, 
                    gen_xlsx.format_percent)
                # Save in our tabl
                gen_xlsx.table[gen_xlsx.row][columns_padding+idx] = str(bar) 


    return gen_xlsx.workbook 

if __name__ == "__main__":

    workbook = None 
    gen_xlsx.init = False
    # Read data files
    for i in sys.argv[2:]:
        name = i.split('.')[0].split('-')
        workbook = gen_xlsx(sys.argv[1], name, parse_file(i))

    for i in gen_xlsx.end_merge:
        aux = gen_xlsx.end_merge[i]
        # We change the latest format
        gen_xlsx.worksheet.merge_range(aux[0], aux[1], aux[2], aux[3], aux[4],
           aux[5])

    workbook.close()
