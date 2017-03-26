###########################################################
#main.py                                                  #
###########################################################
import argparse
import os
import subprocess
import ingester
import pcap2csv
import tshark
import server
import time
from multiprocessing import Process


PCAP_DIR = os.getcwd() + "/pcap"
CSV_DIR = os.getcwd() + "/csv"
WEBAPP_DIR = os.getcwd() + "/webapp/" # find a way to get webapp to start server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w ', '--write ', help="Name of the new PCAP file to"
                        "be created. Will be stored as a csv for ingesting into"
                        " neo4j database", action="store_true", dest="write_file")
    parser.add_argument('-r ', '--read ', help="Give the absolute path to the"
                        "folder containing a pcap file(s). Reads the pcap file"
                        " and convert it to a csv. This is then ingested into"
                        "a neo4j database", action="store", dest="read_file")
    args = parser.parse_args()

    print "WEBAPP_DIR: %s" % WEBAPP_DIR
    if args.write_file:
        pcap_files = []
        csv_files = []

        if not os.path.exists(PCAP_DIR):
            os.mkdir(PCAP_DIR)
        if not os.path.exists(CSV_DIR):
            os.mkdir(CSV_DIR)


        try:
            tshark_process = Process(target=tshark.traffic_capture, args=(PCAP_DIR,))
            server_process = Process(target=server.server, args=(CSV_DIR, 8080,))   
            webapp_process = Process(target=server.server, args=(WEBAPP_DIR, 8000,))
            server_process.start()
            tshark_process.start()
            webapp_process.start()
            while 1:
                time.sleep(30)
                for pcap in os.listdir(PCAP_DIR):
                    print "pcap filename: %s" % pcap
                    if not pcap in pcap_files:
                        pcap_files.append(pcap)
                        print "File being processed: %s" % PCAP_DIR + '/' + pcap
                        csv_process = Process(target=pcap2csv.parser, args=(PCAP_DIR + '/' + pcap,))
                        csv_process.start()
                        csv_process.join()
                for csv in os.listdir(CSV_DIR):
                    print "csv filename: %s" % csv
                    if not csv in csv_files:
                        csv_files.append(csv)
                        print "File to be ingested: %s" % csv
                        ingester_process = Process(target=ingester.create_database, args=(csv,))
                        ingester_process.start()
                        ingester_process.join()
        except KeyboardInterrupt:
            print "Keyboard interrupt detected"     
            tshark_process.join()
            server_process.join()
            webapp_process.join()

    elif args.read_file:

        print "Webapp dir: %s" % WEBAPP_DIR
        try:
            if not os.path.exists(CSV_DIR):
                os.mkdir(CSV_DIR)
            
            if not os.path.exists(PCAP_DIR): 
                os.mkdir(PCAP_DIR)

            # initialize server processes for browsing and uploading to database
            server_process = Process(target=server.server, args=(CSV_DIR, 8080,))
            webapp_process = Process(target=server.server, args=(WEBAPP_DIR, 8000,))
            server_process.start()
            webapp_process.start()
            for pcap_file in os.listdir(args.read_file):
                infile = args.read_file + '/' + pcap_file
                outfile = pcap_file
                print "pcap_file to cut: %s" % infile
                subprocess.call(['editcap', '-c','10000','%s' % infile, '%s' % PCAP_DIR + '/' + pcap_file])
            for pcap_file in os.listdir(PCAP_DIR):
                infile = PCAP_DIR + '/' + pcap_file
                print "infile from main: %s" % infile
                pcap2csv.parser(infile)
                ingester.create_database(pcap_file.split('.')[0] + '.csv')

            server_process.join()

        except KeyboardInterrupt:
            print "Keyboard interrupt detected"
            webapp_process.join()   
            server_process.join()

if __name__ == '__main__':
    main()

