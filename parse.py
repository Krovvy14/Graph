import re
import os
import sys
from igraph import *

#source file. hard coded at the moment will change to cmd line arg later
file = '/path/to/tcpdump.txt'
#regex to find the src > dest of tcpdump file
line_parser = re.compile(r'(\d*\.\d*.\d*.\d*)(\.\d*) > (\d*\.\d*.\d*.\d*)(\.\d*)')

#function that parses out everthing except src > dest and creates a dict from it
def parse_line(line):
	match = line_parser.search(line) 
	if match:
		src_ip, src_port, dest_ip, dest_port = match.groups()
		return {'src_ip': src_ip, 'src_port': src_port, 'dest_ip': dest_ip, 'dest_port': dest_port}
	else:
		return None
		
def main():
	i=0 #control index
	parsed_results = [] #array to store parsing results
	g = Graph()	#create igraph graph object
	g.vs['ip']=[]	#dictionary to hold the VertexSeq attribute named
	#layout= #layout to be used for graph plot
	
	# basic error checking
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
					continue
	#for loop that takes in parsed results and creates vertices
	for result in parsed_results:
		if not result['src_ip'] in g.vs['ip']:
			g.add_vertex()
			g.vs[i]['ip']=result['src_ip']
			i+=1
		elif not result['dest_ip'] in g.vs['ip']:
			g.add_vertex()
			g.vs[i]['ip']=result['dest_ip']
			i+=1
		else:
			continue
	for con in parsed_results:
		src = con['src_ip']
		dest = con['dest_ip']
		
		src_vertex = g.vs.find(ip=str(src))
		dest_vertex = g.vs.find(ip=str(dest))
		g.add_edges([(src_vertex.index, dest_vertex.index)])
	g.vs['label'] = g.vs['ip']
	plot(g,"igraph_test.pdf",layout=g.layout('kamada_kawai'))
	
if __name__ == '__main__':
	main()
