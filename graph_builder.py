import sys
from collections import defaultdict
from igraph import *
import parser

def build_graph(data):
	node_index =0 #index value use for creating nodes
	edge_index = 0 #index value used for creating edges
	g = Graph() #create new graph object
	g.vs['ip'] = [] #define the node attribute
	g.es['protocol'] = [] #define the edge attribute defining protocol of comms
	parsed_results = data #variable to hold the dict returned by parse_line
		
	#for loop that takes in parsed results and creates 
	#vertices only parses the first 2 keys.
	#**Should probably clean this up**
	for ip in parsed_results['src_ip']:
		if not ip in g.vs['ip']:				
			g.add_vertex()
			g.vs[node_index]['ip'] = ip
			node_index += 1
		else:
			continue
			
	for ip in parsed_results['dest_ip']:
		if not ip in g.vs['ip']:				
			g.add_vertex()
			g.vs[node_index]['ip'] = ip
			node_index += 1
		else:
			continue
	'''
	for key in parsed_results:
		for value in parsed_results[key]:
			if not value in g.vs['ip']:				
				g.add_vertex()
				g.vs[i]['ip']=value
				i+=1
			else:
				continue '''
	'''For ease of use I put the source/destination IP's
	into an array while drawing the edges between nodes.'''
	src = parsed_results['src_ip']
	dest = parsed_results['dest_ip']
	protocol = parsed_results['protocol']
	
	#search for the src/dest node in iGraph and draw 
	#the edge between them once the edge is created,
	# add a label to it based on the protocol
	for src, dest, protocol in zip(src, dest, protocol):
		src_vertex = g.vs.find(ip=str(src))
		dest_vertex = g.vs.find(ip=str(dest))
		g.add_edges([(src_vertex.index, dest_vertex.index)])
		g.es[edge_index]['protocol'] = protocol
		edge_index += 1
	
	#graph visual style information
	color_dict = {"TCP": "blue", "TLSv1.2": "green", "DNS": "yellow", \
	"NTP": "deep pink", "HTTP": "dark orange", "ARP": "goldenrod"}
	layout = g.layout("fr")
	g.es['color'] = [color_dict[protocol] for protocol in g.es['protocol']]
	g.vs['label'] = g.vs['ip']
	g.vs['label_dist'] = 1
	g.vs['label_size'] = 10
	plot(g, "fr_graph_output.pdf", layout = layout, margin = 50)
		
