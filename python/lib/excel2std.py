#!/usr/local/bin/python

import xlrd
from xlrd import XLRDError

def readExcel(excel_file_name):
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
            lambda x: '\1'.join(str(x).split('\n')), 
            dict_ws.row_values(i)
        )
        # Check is there the separator '\t' existed in the string. if existed, replace it with the space. 
        row = map(
            lambda x: ' '.join(x.split('\t')),
            row
        )
        data.append(row)
    
    return data[0], data[1:]

if __name__ == '__main__':
    import sys

    excel_file_name = sys.argv[1]
    attr_list, data = readExcel(excel_file_name)

    # Write the file to std output
    for row in data:
        print '\t'.join(row)
