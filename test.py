#!/usr/bin/python

import sys
import socket
import subprocess

def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            print "no more line"
            break

        

        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise ProcessException(command, exitCode, output)


def execute_perf(command):
    f = open('perf_results', 'w')

    process = subprocess.Popen(command, shell=True, stdout=f, stderr=f)

    #sys.stdout.flush()
    #sys.stderr.flush()

    #output = process.communicate()[0]
    #exitCode = process.returncode

    return process

    if (exitCode == 0):
        return output
    else:
        raise ProcessException(command, exitCode, output)

def main():
    process=execute_perf("perf stat -a  -e   dTLB-load-misses sleep 200 > output")
    print "start Perf stat"
    # process.kill()
    #execute(" cd /root/research/workloads/parsec-3.0/bin ; ./parsecmgmt  -a run -i simlarge -c gcc-hooks -n 2 -p canneal; cd -")



if __name__ == '__main__':
    main()
