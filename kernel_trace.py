#!/usr/bin/python                                                                                                      

import sys
import subprocess

def usage():
    print "./kernel_trace.py [cmd]\n"
    print "cmd: "
    print "\treset \tclear /var/log/messages and /sys/kernel/debug/tracing/trace"
    print "\tstart \tstart trace and kvm dbg log"
    print "\tstop  \tstop trace and kvm dbg log"
    print "\tsave  \tsave /var/log/messages and trace to /tmp with a suffix"

def main(argv=None):

    if (len(sys.argv) < 2):
        usage()
        sys.exit()

    cmd_str = sys.argv[1]

    cmd = ""
    if (cmd_str == "reset"):
        print "[INFO] reset kernel trace and log\n"

        # reset kernel log message
        cmd = "echo 0 > /var/log/messages"
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cmd = "echo N > /sys/module/kvm/parameters/dbg"
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # reset kernel trace
        cmd = "echo 0 > /sys/kernel/debug/tracing/trace"
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cmd = "echo 0 > /sys/kernel/debug/tracing/tracing_on"
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    elif (cmd_str == "start"):
        print "[INFO]  start\n"

        # start kernel log message
        cmd = "echo Y > /sys/module/kvm/parameters/dbg"
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # start kernel trace
        cmd = "echo 1 > /sys/kernel/debug/tracing/tracing_on"
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    elif (cmd_str == "stop"):
        print "[INFO]  stop kernel trace and kvm dbg messsage\n"

        # stop kernel log message
        cmd = "echo N > /sys/module/kvm/parameters/dbg"
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        # stop kernel trace
        cmd = "echo 0 > /sys/kernel/debug/tracing/tracing_on"
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    elif (cmd_str == "save"):
        print "[INFO]  save trace and log files to /tmp/\n"

        if (len(sys.argv) < 3):
            print "Please proivde a suffix number"
            print "e.g., ./kernel_trace.py save  001"
            sys.exit()

        append = sys.argv[2]
        filename = "/tmp/trace_" + append
        print "[INFO]  save trace as", filename

        # copy trace file
        cmd = "cp /sys/kernel/debug/tracing/trace " + filename
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # copy kernel log message
        filename = "/tmp/messages_" + append
        cmd = "cp /var/log/messages  " + filename
        print cmd
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    else:
        usage()
        sys.exit()


if __name__ == '__main__':
    main()
