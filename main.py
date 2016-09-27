import sys
import parser
import graph_builder
import tshark
import time

#source file. hard coded at the moment will change to cmd line arg later
#testfile = '/home/batman/Documents/MastersProject/Graph/test.pcap'	
testfile = sys.argv[1]

def main():
	tshark.tshark(testfile)
	time.sleep(15)#temporary solution, need to implement threading
	graph_builder.build_graph(parser.parse_line(testfile))
	
if __name__ == '__main__':
	main()
