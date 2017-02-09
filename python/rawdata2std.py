#!/usr/local/bin/python

import sys
import json
import xlrd
from xlrd import XLRDError

def ReadTabelExcel(excel_file_name):
    '''
    Read Excel

    Read data from local excel file.
    Return the list of attributes and raw data.

    Param:
    * excel_file_name: the path of the file
    '''

    # Open excel file
    wb=xlrd.open_workbook(filename=excel_file_name, on_demand=True)
    # The validation of the file
    nsheets = wb.nsheets
    if nsheets < 1:
        print >> sys.stderr, "Invalid excel file, there is %s sheets in excel file, less then 2." % wb.nsheets
        exit(1)

    # Read the size of the first sheet
    dict_ws = wb.sheet_by_index(0)
    nrows = dict_ws.nrows
    ncols = dict_ws.ncols

    # Convert the data to list
    data = []
    for i in range(nrows):
        # Replace the return characters with '\1'
        row = map(
            lambda x: '\1'.join(str(x).strip().split('\n')), 
            dict_ws.row_values(i)
        )
        # Check is there the separator '\t' existed in the string. if existed, replace it with the space. 
        row = map(
            lambda x: ' '.join(x.strip().split('\t')),
            row
        )
        data.append(row)
    
    return data[0], data[1:]

def ReadListExcel(excel_file_name):

    def inspect_char(c):
        if c.isalpha():
            return c.lower()
        else:
            return ''

    # Open excel file
    wb=xlrd.open_workbook(filename=excel_file_name, on_demand=True)
    # The validation of the file
    nsheets = wb.nsheets
    if nsheets < 1:
        print >> sys.stderr, "Invalid excel file, there is %s sheets in excel file, less then 2." % wb.nsheets
        exit(1)

    # Read the size of the first sheet
    dict_ws = wb.sheet_by_index(0)
    nrows = dict_ws.nrows
    ncols = dict_ws.ncols

    # Convert the data into dict
    data = {}
    for i in range(ncols):
        raw_col = dict_ws.col_values(i)
        # Get the tag name of the col
        tag     = raw_col.pop(0)
        # Inspect every character in the each of the raw words
        col = [
            reduce(
                lambda new_word, c: new_word + inspect_char(c), 
                str(raw_word),
                ''
            ) 
            for raw_word in raw_col
        ]
        # Remove the duplicate and empty element in the col list
        data[tag] = list(set(filter(None, col)))
    
    return data
    


if __name__ == '__main__':

    excel_file_name = sys.argv[1]
    mode            = sys.argv[2] # Processing mode
    tag             = sys.argv[3] # Tag for labeling the data streaming
    
    if mode == 'table':
        # The script would output the raw data line by line,
        # and each of the attributes would be separated by '\t'
        # also the name of the attributes would be omitted.
        attr_list, data = ReadTabelExcel(excel_file_name)
        # Write the file to std output
        for row in data:
            if tag != '-1':
                row.append(tag)
            print '\t'.join(row)
    elif mode == 'list':
        data = ReadListExcel(excel_file_name)
        print json.dumps(data, indent=4)
