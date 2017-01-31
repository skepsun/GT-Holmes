#!/usr/local/bin/python

import xlrd
from xlrd import XLRDError

def readExcel(excel_file_name):
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

    # Convert the sheet to csv file
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

if __name__ == '__main__':
    # The script would output the raw data line by line,
    # and each of the attributes would be separated by '\t'
    # also the name of the attributes would be omitted.

    import sys

    excel_file_name = sys.argv[1]
    tag             = sys.argv[2] # Tag for labeling the data streaming
    attr_list, data = readExcel(excel_file_name)

    # Write the file to std output
    for row in data:
        row.append(tag)
        print '\t'.join(row)
