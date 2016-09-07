'''
Conversion program for smart meter data (KFM5KAIFA-METER)
Input:      raw data - Output: .csv data
Author:     Daan Wielens (Bosch TT-WB/ECT1-Dev, dwi4dev)
Version:    1.1 (2016-09-06)
'''

import sys
import json
import os

if len(sys.argv) != 3:
    print('\nSmart meter data -> CSV conversion tool')
    print('Usage:')
    print('    Single file: python smart_raw.py -f input_file')
    print('    All files in folder: python smart_raw -d directory')
    print('Output CSV files are stored in the same folder as the input\n')
    sys.exit()

def CreateCSV(fname):
    # Create csv file
    global f
    f = open(fname + '.csv','w')

    # Load parser data
    with open('parser.json') as json_data:
        global parser
        parser = json.load(json_data)

    # Generate file header
    global nColumns
    nColumns = len(parser['parser'])
    for i in range(0,nColumns-1):
        f.write(parser['parser'][i]['colname'] + ',')
    f.write(parser['parser'][nColumns-1]['colname'] + '\n')

def Allocate():
    lst = [None] * nColumns
    for i in range(0,nColumns):
        lst[i] = parser['parser'][i]['colname']
    global data
    data = dict.fromkeys(lst)

def WriteData():
    # Fill all empty values - easier for MATLAB later on
    for k in data:
        if data[k] == None:
            data[k] = 0

    for l in range(0,len(parser['parser'])-1):
        f.write(str(data[parser['parser'][l]['colname']]) + ',')
    f.write(str(data[parser['parser'][len(parser['parser'])-1]['colname']]) + '\n')

def ParseData(input_file):
    g = open(input_file)
    begin_found = 0
    for line in g:
        if begin_found == 0:
            if '/' in line:
                Allocate()
                begin_found = 1
        elif '!' in line:
            # Write all collected data in the dictionary data to the csv file
            WriteData()
        elif '/' in line:
            # Clear the dictionary data
            Allocate()
        else:
            for j in range(0,len(parser['parser'])):
                if parser['parser'][j]['prefix'] in line:
                    if (parser['parser'][j]['colname'] != 'Begin') and (parser['parser'][j]['colname'] != 'End'):
                        # Remove prefix data
                        line_data = line.replace(parser['parser'][j]['prefix'],'')
                        # Remove suffix data
                        line_data = line_data.replace(parser['parser'][j]['suffix'],'')
                        # Gas data needs to be splitted extra due to the datetime that also is in the line
                        if parser['parser'][j]['colname'] == 'Gas (hourly) (m3)':
                            line_data = line_data.split(')(')[1]
                        # Remove enters (\r\n) and leading zeros
                        line_data = line_data.replace('\r\n','').lstrip('0')
                        # If data only contained zeros, set the (now) empty value to zero
                        if line_data == '':
                            line_data = '0'
                        # If data was 0.something, put that one zero back
                        if line_data[0] == '.':
                            line_data = '0' + line_data
                        data[parser['parser'][j]['colname']] = line_data


if sys.argv[1] == '-f':
    input_file = sys.argv[2]
    fname = input_file.split('/')[-1].split('.')[0] # Filename only, without extension
    dname = input_file.split('/')[:-1]
    dname = ''.join(dname)
    CreateCSV(input_file)
    ParseData(input_file)

if sys.argv[1] == '-d':
    input_dir = sys.argv[2]
    file_list = os.listdir(input_dir)
    if input_dir[-1] != '/':
        input_dir = input_dir + '/'

    for file_name in file_list:
        print('Parsing: ' + file_name)
        try:
            CreateCSV(input_dir + file_name)
            ParseData(input_dir + file_name)
            print('Parsing succeeded.')
        except Exception:
            os.remove(input_dir + file_name + '.csv')
            print('Parsing failed. Not a valid file.')
