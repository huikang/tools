"""
   Author: Hui Kang (hkang@cs.sunysb.edu)

   This script convert the output of xentop to csv format.
   The only support command now for xentop is
            xentop -b [-d delay]

   Usages: ./xentop2csv.py <input file>
           The output will be several ./domainname.csv files
"""

#! /usr/bin/python

import csv
import sys
import os
import random
import optparse as _o
import curses as _c

options, args = None, None

TRUE=1
FALSE=0

def setup_cmdline_parse():
    parser = _o.OptionParser()
    parser.add_option("-i", "--inputfile", dest="input_f_name",\
        action = "store", default="", help = " input xentop file")

    return parser

def open_file(file_name, mode):
    """ Open a file """
    try:
        the_file = open(file_name, mode)
    except(IOError), e:
        print "[Error] Unable to open the file ", file_name, e, "\n"
        sys.exit()
    else:
        return the_file

def print_usage():
    print "Usages: ./xentop2csv.py <input file>"

def get_vm_names(input_f_name):
    vm_names = []
    fields = []

    infile = open_file(input_f_name, "r")

    #skip the first line
    line_one=0
    for line in infile:
        if (line_one >= 1):
            #print line
            if ( line.find("NAME") >= 0 and line.find("STATE") >= 0 ):
                break
            list_in_line = line.split(None)
            vm_names.append(list_in_line[0])
        else:
            list_in_line = line.split(None)
            for item in list_in_line:
                fields.append(item)
        line_one += 1

    infile.close()
    return vm_names, fields

def calc_diff(current, last):
    diff = ""
    last_update = -1
    if last >= 0:
        tmp = current
        diff = str(int(current) - last)
        last_update = int(tmp)
    else:
        last_update = int(current)
        diff = str(0)
    
    return diff, last_update

def convert2csv(input_f_name, vm_names, fields):
    infile = open_file(input_f_name, "r")
    outfiles = []

    # Do not cumulate for these attributes
    NETTX = 0
    NETRX = 0
    VBD_RD = 0
    VBD_WR = 0
    last_nettx = -1
    last_netrx = -1
    last_vbd_rd = -1
    last_vbd_wr = -1
    
    for index in range (0, len(fields)):
        if (fields[index] == "NETTX(k)"):
            NETTX=index
        if (fields[index] == "NETRX(k)"):
            NETRX=index
        if (fields[index] == "VBD_RD"):
            VBD_RD=index
        if (fields[index] == "VBD_WR"):
            VBD_WR=index

    for vm in vm_names:
        out_f_name = vm + ".csv"
        outfile = open_file(out_f_name, "w")
        outfiles.append(outfile)
    
    # write the fields for first line
    for files in outfiles:
        line = ""
        for item in fields:
            line += item + ","
        line += "\n"
        files.write(line)

    for vm in vm_names:
        infile.seek(0)
        last_nettx = -1
        last_netrx = -1
        last_vbd_rd = -1
        last_vbd_wr = -1
        for line in infile:
            list_in_line = line.split(None)
            if (line.find(vm) >= 0):
                index = vm_names.index(list_in_line[0])
                csvline = ""
                for j in range (0, len(list_in_line)):
                    if j == NETTX:
                        (list_in_line[j], last_nettx) = \
                        calc_diff(list_in_line[j], last_nettx)
                    if j == NETRX:
                        (list_in_line[j], last_netrx) = \
                        calc_diff(list_in_line[j], last_netrx)
                    if j == VBD_RD:
                        (list_in_line[j], last_vbd_rd) = \
                        calc_diff(list_in_line[j], last_vbd_rd)
                    if j == VBD_WR:
                        (list_in_line[j], last_vbd_wr) = \
                        calc_diff(list_in_line[j], last_vbd_wr)

                    csvline += list_in_line[j] + ","

                csvline += "\n"
                #print csvline
                outfiles[index].write(csvline)
        
    for files in outfiles:
        files.close()

def main():
    global options
    global args
    

    print "Convert xentop into csv format..."
    parser = setup_cmdline_parse()
    (options, args) = parser.parse_args()
    
    if (options.input_f_name ==""):
        print_usage()
        sys.exit(1)
    
    input_f_name = options.input_f_name
    output_f_name = input_f_name + ".csv"
    # output_f = open(output_f_name, "w")
    print "Output file name: " + output_f_name

    (vm_names, fields) = get_vm_names(input_f_name)
    print vm_names
    print fields
    vm_names.remove("Domain-0")

    convert2csv(input_f_name, vm_names, fields)

if __name__=="__main__":
    main()
