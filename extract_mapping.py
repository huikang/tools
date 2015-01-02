#!/usr/bin/python                                                                                                      

import sys
import subprocess

def usage():
    print "Usage: ./extrat_mapping.py <input file> <output file>\n"
    print "Extract the gva to hpa mapping in the input file."
    print "The input lines:  mapping: gva ffff88007b44a570, spte 8000000621bad263"
    print "The output lines: 7fa882912000,59f13f"


def extract_line(line=""):

    extracted_line = ""
    gva = ""
    hpa = ""
    spte = ""
    if (line.find("mapping") >= 0):
        print line
        
        # extract gva
        index_start = line.find("gva") + 4
        # print "start " + str(index_start)

        index_end = line.find(",", index_start)
        # print "end   " + str(index_end)
        # print line[index_start]
        # print line[index_end]
        # print line[index_start:index_end]
        gva = line[index_start:index_end]
        print "gva: " + gva


        # extract hpa
        index_start = line.find("spte", index_end) + 5
        # print "start " + str(index_start)

        index_end = line.find("\n", index_start) - 3
        # print "end   " + str(index_end)

        # print line[index_start]
        # print line[index_end]
        # print line[index_start:index_end]
        hpa = line[index_start:index_end]
        print "hpa: " + hpa

        extracted_line = gva + "," + hpa
    
    print extracted_line
    return extracted_line
    
def main(argv=None):

    if (len(sys.argv) != 3):
        usage()
        sys.exit()

    i_filename = sys.argv[1]
    o_filename = sys.argv[2]

    print "Input file: ", i_filename
    print "Output file:", o_filename

    # read each line of the input file
    in_file = open(i_filename, 'r')
    output_file = open(o_filename, 'w')

    for line in in_file:
        output_line = extract_line(line) + "\n"
        print output_line
        output_file.write(output_line)

if __name__ == '__main__':
    main()
