import sys
from collections import defaultdict
from igraph import *
import parser
import os


def build_graph(data, outfile):
    if not os.path.exists('/tmp/network_graph'):
        os.mkdir("/tmp/network_graph")
    node_index = 0  # index value use for creating nodes
    edge_index = 0  # index value used for creating edges

    g = Graph()  # create new graph object
    g.vs['ip'] = []  # define the node attribute
    g.es['protocol'] = []  # define the edge attribute defining protocol of comms

    # for loop that takes in parsed results and creates
    # vertices only parses the first 2 keys.
    # **Should probably clean this up**
    for ip in data['src_ip']:
        try:
            if not ip in g.vs['ip']:
                g.add_vertex()
                g.vs[node_index]['ip'] = ip
                node_index += 1
            else:
                continue
        except KeyError:
            pass

    for ip in data['dest_ip']:
        try:
            if not ip in g.vs['ip']:
                g.add_vertex()
                g.vs[node_index]['ip'] = ip
                node_index += 1
            else:
                continue
        except KeyError:
            pass

    src = data['src_ip']
    dest = data['dest_ip']
    protocol = data['protocol']

    # search for the src/dest node in iGraph and draw
    # the edge between them once the edge is created,
    # add a label to it based on the protocol
    for src, dest, protocol in zip(src, dest, protocol):
        src_vertex = g.vs.find(ip=str(src))
        dest_vertex = g.vs.find(ip=str(dest))
        g.add_edges([(src_vertex.index, dest_vertex.index)])
        g.es[edge_index]['protocol'] = protocol
        edge_index += 1

    # graph visual style information
    color_dict = {
        "TCP": "blue",
        "ICMP": "green",
        "IGMP": "yellow",
        "IPv4": "deep pink",
        "IPv6": "dark orange",
        "RDP": "goldenrod",
        "UDP": "red",
        "NONE": "grey"
    }

    layout = g.layout("fr")
    g.es['color'] = [color_dict[protocol] for protocol in g.es['protocol']]
    g.vs['label'] = g.vs['ip']
    g.vs['label_dist'] = 1
    g.vs['label_size'] = 10
    plot(g, os.path.join('/tmp/network_graph', "%s.png" % outfile), layout=layout, margin=50)
