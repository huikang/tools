#!/usr/bin/python                                                                                                      

import sys
import subprocess

def usage():
    print "Usage: ./extrat_mapping.py <-m> <input file> <output file>\n"
    print "Extract the gva to hpa mapping in the input file."
    print "The input lines:  mapping: gva ffff88007b44a570, spte 8000000621bad263"
    print "The output lines: 7fa882912000,59f13f\n"

    print "-m\t\t mapping file. If not present, extract all the mappings"

class Mapping:
    def __init__(self, addr_start, addr_end, perms, offset, dev, inode,
                 pathname):
        self.addr_start = int(addr_start, 16)
        self.addr_end   = int(addr_end, 16)
        self.perms      = perms
        self.offset     = offset
        self.dev        = dev
        self.inode      = inode
        self.pathname   = pathname
        self.range      = self.addr_end - self.addr_start

    def output(self):
        print self.addr_start, self.addr_end, "(", self.range, ")", \
            self.perms, self.offset, self.dev, self.inode, self.pathname

#
# mappings:   a set of mappings
# m_filename: filename
#
def get_mappings_from_file(mappings, m_filename):

    print m_filename
    map_file = open(m_filename, 'r')

    for line in map_file:
        print line
        words = line.split();
        # get vaddress start and end
        address = words[0].split('-')
        # print address
        if len(words) == 6:
            map = Mapping(address[0], address[1], words[1], words[2], words[3],
                          words[4], words[5])
        else:
            map = Mapping(address[0], address[1], words[1], words[2], words[3],
                          words[4], "")
        # map.output()
        mappings.append(map)
        # break

    print "start, end (range), perms, offset, dev, inode, pathname"
    for map in mappings:
        map.output()

    map_file.close()


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

    if (len(sys.argv) < 3):
        usage()
        sys.exit()

    if (sys.argv[1] == "-m"):
        m_filename = sys.argv[2]
        i_filename = sys.argv[3]
        o_filename = sys.argv[4]
    else:
        i_filename = sys.argv[1]
        o_filename = sys.argv[2]

    print "Input file:\t",  i_filename
    print "Output file:\t",  o_filename
    print "mapping file:\t", m_filename

    mappings=[]
    print "mappings: ", mappings
    if m_filename == "":
        print "No mapping file"
    else:
        print "Extracting mappings"
        get_mappings_from_file(mappings, m_filename)
    sys.exit()

    # read each line of the input file
    in_file = open(i_filename, 'r')
    output_file = open(o_filename, 'w')

    for line in in_file:
        output_line = extract_line(line) + "\n"
        print output_line
        output_file.write(output_line)
    
    in_file.close()
    out_file.close()

if __name__ == '__main__':
    main()
