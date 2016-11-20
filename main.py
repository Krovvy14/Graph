import pcap_parser
import graph_builder
import tshark
import time
import argparse
import thread
import subprocess
import os
import glob

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w ', '--write ', help="Name of the new PCAP file to be created",\
                        action="store", dest="write_file")
    parser.add_argument('-r ', '--read ', help="Reads a pcap file and build a visual"\
                        " representation of it", action="store", dest="read_file")
    args = parser.parse_args()

    if args.write_file:
        #thread.start_new_thread(tshark.tshark,(args.write_file, ))
        tshark.tshark(args.write_file)
        time.sleep(60)   #temporary solution, need to implement threading
        graph_builder.build_graph(pcap_parser.complete_view(args.write_file), '%s_complete_view' % args.write_file[:-5])
        graph_builder.build_graph(pcap_parser.file_transfer(args.write_file), '%s_file_transfer' % args.write_file[:-5])
    elif args.read_file:
        for pcap_file in glob.glob(os.path.join(args.read_file, '*.pcap')):
            graph_builder.build_graph(pcap_parser.complete_view(pcap_file), '%s_complete_view' % args.read_file[:-5])
            graph_builder.build_graph(pcap_parser.file_transfer(pcap_file), '%s_file_transfer' % args.read_file[:-5])

if __name__ == '__main__':
    main()
