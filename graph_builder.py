import sys
from collections import defaultdict
from igraph import *
import parser

#creates all of the nodes and returns a graph object
def make_node(data):
	node_index =0 #index value use for creating nodes
	g = Graph() #create graph object
	g.vs['ip'] = [] #define the node attribute
	src = data['src_ip']
	dest = data['dest_ip']
	#for loop that takes in parsed results and creates 
	#vertices
	for ip in src:
		if not ip in g.vs['ip']:				
			g.add_vertex()
			g.vs[node_index]['ip'] = ip
			node_index += 1
	for ip in dest:
		if not ip in g.vs['ip']:				
			g.add_vertex()
			g.vs[node_index]['ip'] = ip
			node_index += 1
			
	return g

#takes in parsed data set and graph object
#returns completed graph with edges
def build_edges(data, graph):
	edge_index = 0
	src = data['src_ip']
	dest = data['dest_ip']
	protocol = data['protocol']
	
	for src, dest, protocol in zip(src, dest, protocol):
		src_vertex = graph.vs.find(ip=str(src))
		dest_vertex = graph.vs.find(ip=str(dest))
		graph.add_edges([(src_vertex.index, dest_vertex.index)])
		graph.es[edge_index]['protocol'] = protocol
		edge_index += 1
		
	return graph

def build_graph(data):
	#test make node function
	g = make_node(data)	
	build_edges(data, g)

	#graph visual style information
	color_dict = {"TCP": "blue", "TLSv1.2": "green", "DNS": "yellow", \
	"NTP": "deep pink", "HTTP": "dark orange", "ARP": "goldenrod"}
	layout = g.layout("kk")
	g.es['color'] = [color_dict[protocol] for protocol in g.es['protocol']]
	g.vs['label'] = g.vs['ip']
	g.vs['label_dist'] = 1
	g.vs['label_size'] = 10
	plot(g, "kk_graph_output.pdf", layout = layout, margin = 50)
