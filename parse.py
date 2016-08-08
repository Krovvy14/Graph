import re
import os
import sys
from igraph import *

file = '/path/to/packetCapture.txt'
line_parser = re.compile(r'(\d*\.\d*.\d*.\d*)(\.\d*) > (\d*\.\d*.\d*.\d*)(\.\d*)')

def parse_line(line):
	match = line_parser.search(line)
	if match:
		src_ip, src_port, dest_ip, dest_port = match.groups()
		return {'src_ip': src_ip, 'src_port': src_port, 'dest_ip': dest_ip, 'dest_port': dest_port}
	else:
		return None

def main():
	parsed_results = []
    
    
	if not os.path.exists(file):
		print 'Error, cannot load file'
		sys.exit(1)
	else:
		with open(file,'r') as source_file:
			for source_line in source_file:
				results = parse_line(source_line)
				if results:
					parsed_results.append(results)
				else:
					print "Unable to find results"
	for result in parsed_results:
		#print result['src_ip']
		#print result['dest_ip']
		g = Graph()
			g.vs['ip']
		#g.get_edgelist()[0:]
                    
    
        					
if __name__ == '__main__':
	main()
