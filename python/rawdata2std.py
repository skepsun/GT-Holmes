#!/usr/local/bin/python
import re
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
        # Try to encode the value to utf-8,
        # If failed, the value might be numbers
        try:
            row = [ x.encode('utf-8') for x in dict_ws.row_values(i) ]
        except Exception:
            row = dict_ws.row_values(i)
        # Replace the return characters with '\1'
        row = [ '\1'.join(str(x).strip().split('\n')) for x in row ]
        # Check is there the separator '\t' existed in the string. if existed, replace it with the space. 
        row = [ ' '.join(x.strip().split('\t')) for x in row ]
        data.append(row)
    
    return data[0], data[1:]

def ReadListExcel(excel_file_name):

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
        tag = raw_col.pop(0)
        # - Split the phrases by the delimiter '/'
        col = []
        for raw_word in raw_col:
            if '/' in str(raw_word):
                # exp: raw_word  = 'Back/Rear Door'
                #      items     = ['Back/Rear', 'Door']
                #      options   = ['Back/Rear']
                #      -> items  = ['Door']
                #      raw_words = ['Back Door', 'Rear Door']
                items          = str(raw_word).split()
                options        = []
                opt_item_index = 0
                # Get options (which contains delimiter '/') and its index
                for i in range(len(items)):
                    if '/' in items[i]:
                        options        = items[i].split('/')
                        opt_item_index = i
                # Generate new raw words with all the options
                raw_words = []     
                for opt in options:
                    items[opt_item_index] = opt
                    raw_words.append(' '.join(items))
                col += raw_words     
            else:
                col.append(str(raw_word))
        # - Remove the content in the brackets
        # - Replace the uppercases with lowercases
        col = [ 
            re.sub('\(.*?\)','', word).lower()
            for word in col
        ]
        # - Replace the ' ' with '_'
        col = [
            '_'.join('_'.join(word.split()).split('-'))
            for word in col
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
