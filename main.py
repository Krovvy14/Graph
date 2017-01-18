###########################################################
#main.py												  #
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

	if args.write_file:
		pcap_dir = "/tmp/pcap"
		csv_dir = "/tmp/csv"
		pcap_files = []
		csv_files = []

		if not os.path.exists(pcap_dir):
			os.mkdir(pcap_dir)
		if not os.path.exists(csv_dir):
			os.mkdir(csv_dir)

		try:
			tshark_process = Process(target=tshark.traffic_capture, args=(pcap_dir,))
			server_process = Process(target=server.server, args=(csv_dir,))	
			server_process.start()
			tshark_process.start()

			while 1:
				time.sleep(30)
				for pcap in os.listdir(pcap_dir):
					print "pcap filename: %s" % pcap
					if not pcap in pcap_files:
						pcap_files.append(pcap)
						print "File being processed: %s" % pcap_dir + '/' + pcap
						csv_process = Process(target=pcap2csv.parser, args=(pcap_dir + '/' + pcap,))
						csv_process.start()
						csv_process.join()
				for csv in os.listdir(csv_dir):
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

	elif args.read_file:
		try:
			csv_dir = '/tmp/csv'

			if not os.path.exists(csv_dir):
				os.mkdir(csv_dir)

			server_process = Process(target=server.server, args=(csv_dir,))
			server_process.start()

			for pcap_file in os.listdir(args.readfile):
				infile = args.readfile + '/' + pcap_file
				pcap2csv.parser(infile)
				ingester.create_databse(pcap_file + '.csv')

			server_process.join()
		except KeyboardInterrupt:
			print "Keyboard interrupt detected"
	

if __name__ == '__main__':
	main()

