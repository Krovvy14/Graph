###########################################
#pcap2csv.py							  #
###########################################
#! /usr/bin/python
import os
import subprocess
import time

def parser(infile):
    infile_split = infile.split('/')
    file = infile_split[-1].split('.')[0]
    print "converting file: %s" % file

    start_time = time.time()
    print "Start time: %s" % start_time

    with open(os.getcwd() + '/csv/' + file + ".csv", 'w+') as outfile:
        subprocess.call(['tshark','-r','%s' % infile,'-T','fields','-e','frame.number',\
        '-e','eth.src','-e','ip.src','-e','eth.dst','-e','ip.dst','-e','_ws.col.Protocol',\
        '-e','_ws.col.Info','-e','data','-e','frame.len','-E','header=y','-E','separator=|'], stdout=outfile)

    end_time = time.time()
    print "End time: %s" % end_time
    run_time = ((end_time - start_time)/60)
    print "Run time: %s minutes" % str(run_time)


