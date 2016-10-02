import pcap_parser
import graph_builder
import tshark
import time
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w ', '--write ', help="Name of the new PCAP file to be created",\
                        action="store", dest="write_file")
    parser.add_argument('-r ', '--read ', help="Reads a pcap file and build a visual"\
                        "representation of it", action="store", dest="read_file")
    args = parser.parse_args()

    if args.write_file:
        tshark.new_capture(args.write_file)
        time.sleep(15)  # temporary solution, need to implement threading
        graph_builder.build_graph(pcap_parser.parse_line(args.write_file))
    elif args.read_file:
        graph_builder.build_graph(pcap_parser.parse_line(args.read_file))

if __name__ == '__main__':
    main()
