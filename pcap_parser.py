
import os
import sys
from scapy.all import *


# small function to create a 'white list' of just
# TU ip's
def good_ip():
    good_ips = []

    for i in range(0, 256):
        good_ips.append('172.16.6.' + str(i))
        good_ips.append('192.168.26.' + str(i))

    return good_ips


# scapy returns the IP protocol #. This just does
# a num to string coversion.
def protocol_replace(protocol):
    if protocol == 1:
        return "ICMP"
    elif protocol == 2:
        return "IGMP"
    elif protocol == 4:
        return "IPv4"
    elif protocol == 6:
        return "TCP"
    elif protocol == 17:
        return "UDP"
    elif protocol == 27:
        return "RDP"
    elif protocol == 41:
        return "IPv6"
    else:
        return "NONE"


# iterates over entire pcap file and returns dictionary
# of important info for graph
def complete_view(testfile):
    result = {}	  # dictionary that will hold src/dest ip addr's
    # basic error checking
    if not os.path.exists(testfile):
        print 'Error, cannot load file'
        sys.exit(1)
    # reads in the pcap and creates the dictionary of src/dest ips
    # this dict is used to build the graph
    else:
        p = rdpcap(testfile)
        team_ips = good_ip()
        for pkt in p:
                try:
                    if pkt[IP].src or pkt[IP].dst in team_ips:
                        result.setdefault('src_ip', []).append(pkt[IP].src)
                        result.setdefault('dest_ip', []).append(pkt[IP].dst)
                        result.setdefault('protocol', []).append(protocol_replace(pkt[IP].proto))
                except IndexError:
                    pass
    return result


# any pkt with a data > .75*MTU is likely indicative
# of a file transfer and should be investigated further
def file_transfer(testfile):
    result = {}
    if not os.path.exists("/tmp/file_transfer_log"):
        os.mkdir("/tmp/file_transfer_log")
    if not os.path.exists(testfile):
        print 'Error, cannot load file'
        sys.exit(1)
    else:
        p = rdpcap(testfile)
        team_ips = good_ip()
        sys.stdout = open('/tmp/file_transfer_log/%s_file_transfer.txt' % testfile[:-5], 'w+')
        for pkt in p:
            try:
                if pkt[IP].src in team_ips and pkt[IP].dst not in team_ips:
                    if int(pkt[IP].len) > 1125:
                        print pkt.show()
                        result.setdefault('src_ip', []).append(pkt[IP].src)
                        result.setdefault('dest_ip', []).append(pkt[IP].dst)
                        result.setdefault('protocol', []).append(protocol_replace(pkt[IP].proto))
            except IndexError:
                continue
return result


def red_team(testfile):
    result = {}	  # dictionary that will hold src/dest ip addr's
    # basic error checking
    if not os.path.exists(testfile):
        print 'Error, cannot load file'
        sys.exit(1)
    # reads in the pcap and creates the dictionary of src/dest ips
    # this dict is used to build the graph
    else:
        p = rdpcap(testfile)
        team_ips = good_ip()
        for pkt in p:
                try:
                    if pkt[IP].src not in team_ips and pkt[IP].dst in team_ips:
                        result.setdefault('src_ip', []).append(pkt[IP].src)
                        result.setdefault('dest_ip', []).append(pkt[IP].dst)
                        result.setdefault('protocol', []).append(protocol_replace(pkt[IP].proto))
                except IndexError:
                    pass
    return result


# any pkt with a data > .75*MTU is likely indicative
# of a file transfer and should be investigated further
def scorebot(testfile):
    result = {}
    nagios = ["192.168.26.253", "172.16.6.253"]

    if not os.path.exists("/tmp/scorebot_log"):
        os.mkdir("/tmp/scorebot_log")
    if not os.path.exists(testfile):
        print 'Error, cannot load file'
        sys.exit(1)
    # reads in the pcap and creates the dictionary of src/dest ips
    # this dict is used to build the graph
    else:
        p = rdpcap(testfile)
        sys.stdout = open('/tmp/scorebot_log/%s_scorebot_traffic.txt' % testfile[:-5], 'w+')
        for pkt in p:
            try:
                if pkt[IP].src or pkt[IP].dst in nagios:
                    print pkt.show()
                    result.setdefault('src_ip', []).append(pkt[IP].src)
                    result.setdefault('dest_ip', []).append(pkt[IP].dst)
                    result.setdefault('protocol', []).append(protocol_replace(pkt[IP].proto))
            except IndexError:
                continue
    return result
