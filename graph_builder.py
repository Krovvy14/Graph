import sys
from collections import defaultdict
from igraph import *
import parser
import os


def build_graph(data, outfile):
    if not os.path.exists('/tmp/network_graph'):
        os.mkdir("/tmp/network_graph")
    try:
        node_index = 0  # index value use for creating nodes
        edge_index = 0  # index value used for creating edges

        g = Graph()  # create new graph object
        g.vs['ip'] = []  # define the node attribute
        g.es['protocol'] = []  # define the edge attribute defining protocol of comms

        # for loop that takes in parsed results and creates
        # vertices only parses the first 2 keys.
        for ip in data['src_ip']:
            if not ip in g.vs['ip']:
                g.add_vertex()
                g.vs[node_index]['ip'] = ip
                node_index += 1
            else:
                continue

        for ip in data['dest_ip']:
            if not ip in g.vs['ip']:
                g.add_vertex()
                g.vs[node_index]['ip'] = ip
                node_index += 1
            else:
                continue

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
            "NONE": "gray"
        }

        # create the iGraph layout controls
        layout = g.layout("circle")
        g.es['color'] = [color_dict[protocol] for protocol in g.es['protocol']]
        g.vs['label'] = g.vs['ip']
        g.vs['label_dist'] = 1
        g.vs['label_size'] = 10

        # Each of theses statements places the graph in an appropriate
        # /tmp/network_graph folder based on the name of the outfile created.
        if "file_transfer" in outfile:
            if not os.path.exists("/tmp/network_graph/file_transfer_log"):
                os.mkdir("/tmp/network_graph/file_transfer")
            plot(g, os.path.join('/tmp/network_graph/file_transfer', "%s.png" % outfile), layout=layout, margin=50)
        elif "red_team" in outfile:
            if not os.path.exists("/tmp/network_graph/red_team"):
                os.mkdir("/tmp/network_graph/red_team")
            plot(g, os.path.join('/tmp/network_graph/red_team', "%s.png" % outfile), layout=layout, margin=50)
        elif "scorebot" in outfile:
            if not os.path.exists("/tmp/network_graph/scorebot"):
                os.mkdir("/tmp/network_graph/scorebot")
            plot(g, os.path.join('/tmp/network_graph/scorebot', "%s.png" % outfile), layout=layout, margin=50)
        else:
            if not os.path.exists("/tmp/network_graph/complete_view"):
                os.mkdir("/tmp/network_graph/complete_view")
            plot(g, os.path.join('/tmp/network_graph/complete_view', "%s.png" % outfile), layout=layout, margin=50)
    except KeyError:
        pass
