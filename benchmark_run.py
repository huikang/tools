#!/usr/bin/python

import sys
import socket
import subprocess

# configurable perf stats
perf_stat_sets=[ ["dTLB-load-misses", "dTLB-loads", "L1-dcache-loads",
                  "L1-dcache-load-misses", "L1-dcache-prefetch-misses"],   # 0
                 ["LLC-load-misses", "LLC-loads"],                         # 1 
                 ["LLC-prefetch-misses", "LLC-prefetches"]                 # 2
               ]
perf_stat_selected = 0
huge_tlb=False

# hadoop configurables
class hadoop_cmd:
    def __init__(self):
        self.directory = "/root/research/workloads/hadoop-2.4.1"


class parsec_cmd:
    # ssh 127.0.0.1 "cd research/workloads/parsec-3.0/bin; 
    #    ./parsecmgmt -a run -i simsmall -c gcc-hooks -n 2 -p canneal "

    def __init__(self):

        #configurable parameters
        self.directory = " /root/research/workloads/parsec-3.0/bin "
        # self.directory = " /home/hkang/research/workloads/parsec-3.0/bin "
        self.input_size = "native"

        # put -p at the end of the option
        self.options = " -a run " + " -i " + self.input_size + " -c gcc-hooks -n 1 -p "
        self.name = ""

class benchmark:

    def __init__(self):
        self.perf_stat = False            # enable perf stat
        self.ip =  ""                 # remote ip
        self.cnf = ""                 # benchmark name file
        self.cmd = ""                 # benchmark command

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def execute_perf_stat():
    print "execute perf stat"
    print "profiled stats"
    #print len(perf_stat_sets)
    #print perf_stat_sets
    
    perf_stat_events = perf_stat_sets[0]
    print perf_stat_events

    cmd = "perf stat -a "
    for event in perf_stat_events:
        cmd += " -e " + event

    cmd += " sleep 1000 "
    print cmd

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    # output = process.communicate()[0]
    # exitCode = process.returncode

    #if (exitCode == 0):
    #    return output
    #else:
    #    raise ProcessException(command, exitCode, output)

    return process



def usage(myname):
    print myname, "usage:"
    print "  -c [parsec|mysql|hadoop] \tbenchmark configure file"
    print "  -r [IP]                  \tIP address of remote machine"
    print "  -perf                    \tEnable perf stat"
    print "  -h                       \thelp info"

def process_cmd(argv, cxt):
    i = 1;
    str_len = len(argv)

    rc = False
    if (str_len == 1):
        return rc

    while i != str_len:
        print "  ", i
        cmd_element = argv[i]
        print " ", cmd_element
        if cmd_element == "-r":
            print "  next should be ip"
            if (i+1) == str_len:
                return 0
            else:
                ip_addr = argv[i+1]
                if validate_ip(ip_addr) == False:
                    return 0
                else:
                    print "\t\tvalid ip: ", ip_addr
                    cxt.ip = ip_addr
            i = i + 1
        elif cmd_element == "-c":
            print "  next should be benchmark cnf"
            if (i+1) == str_len:
                return 0
            else:
                print "  benchmark name", argv[i+1]
                cxt.cnf = argv[i+1]
            i = i + 1
        elif cmd_element == "-perf":
            cxt.perf_stat = True
        elif cmd_element == "-h":
            return False   
        else:
            return 0

        i += 1
    rc = True
    print "Process all argements"
    return rc;

# Run the parsec command and start perf if necessary
def execute_cmd(cxt):

    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    process = subprocess.Popen(cxt.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()

        if nextline.find("Entering ROI") >= 0:
            print "[LOG] Enter ROI, start perf"
            if cxt.perf_stat == False:
                print "perf stat disabled"
            else:
                print "[LOG] start the perf process"
                #perf_process = execute_perf_stat()

        if nextline.find("Leaving ROI") >= 0:
            if cxt.perf_stat == True:
                print "Kill the perf stat process"
                # perf_output = perf_process.communicate[0]
                #perf_process.terminate()
                #print perf_process.stdout
                

        if nextline == '' and process.poll() != None:
            print "no more line"
            break

        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    print "--------------------------------------------------------"

    if (exitCode == 0):
        return output
    else:
        raise ProcessException(command, exitCode, output)

def run_parsec(cxt):
    print "Run parsec file"

    filename = "parsec.cnf"
    # open parsec file
    f = open(filename, 'r+')

    parseccmd = parsec_cmd()
    for name in f:
        print name

        perf_cmd = " "

        hugetlb_cmd = ""

        cmd = ""

        if huge_tlb ==True:
            hugetlb_cmd = " hugectl  --heap  "

        if cxt.perf_stat == True:
            perf_cmd = " perf stat "
            for event in perf_stat_sets[perf_stat_selected]:
                perf_cmd += " -e " + event + " "

        if cxt.ip =="":
            cmd = " cd " + parseccmd.directory + " ; "
            cmd += perf_cmd + hugetlb_cmd + \
                "./parsecmgmt " + parseccmd.options + name + "  "
        else:
            cmd = "ssh " + cxt.ip + " \"  cd " + parseccmd.directory \
                + "; ./parsecmgmt " + parseccmd.options + name + " \" "
        print cmd
        cxt.cmd = cmd
    
        # output = subprocess.check_output(cmd, shell=True)
        # print output

        # Run the command and start perf when entring ROI
        execute_cmd(cxt)

    f.close()

def run_hadoop(cxt):

    hadoopcmd = hadoop_cmd()    

    perf_cmd = " "

    hugetlb_cmd = ""

    cmd = ""

    if huge_tlb ==True:
        hugetlb_cmd = " hugectl  --heap  "

    if cxt.perf_stat == True:
        perf_cmd = " perf stat "
        for event in perf_stat_sets[perf_stat_selected]:
            perf_cmd += " -e " + event + " "

    if cxt.ip =="":
        cmd = " cd " + hadoopcmd.directory + " ; time "
        cmd += perf_cmd + hugetlb_cmd + \
            " ./bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.4.1.jar terasort /tera_sort/input_4G /tera_sort/output_4G_1  "
        cxt.cmd = cmd    
        print cxt.cmd
        execute_cmd(cxt)


        cmd = " cd " + hadoopcmd.directory + " ; time "
        cmd += perf_cmd + hugetlb_cmd + \
            " ./bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.4.1.jar terasort /tera_sort/input_4G /tera_sort/output_4G_2  "
        cxt.cmd = cmd    
        print cxt.cmd
        execute_cmd(cxt)

    else:
        cmd = "ssh " + cxt.ip + " \"  cd " + parseccmd.directory \
                + "; ./parsecmgmt " + parseccmd.options + name + " \" "
    print cmd




def main(argv=None):

    # Main benchamrk context 
    cxt = benchmark()

    # Set the command lines
    rc = process_cmd(sys.argv, cxt)
    if (rc == 0):
        usage(sys.argv[0])
    else:
        print "[INFO]\t Use", cxt.cnf, "on", cxt.ip, " perf_stat", cxt.perf_stat

    if (cxt.cnf != "parsec") and (cxt.cnf != "hadoop"):
        print "[ERROR]\t Invalid benchmark name file"
        return

    if (cxt.ip == ""):
        print "No IP"

    if (cxt.cnf == "parsec"):
        run_parsec(cxt)
    elif (cxt.cnf == "hadoop"):
        run_hadoop(cxt);

if __name__ == '__main__':
    main()
