import os
import sys
from scapy.all import *

# function that parses out everthing except src > dest/protocol
# Returns dictionary object with parsed data

#scapy returns the IP protocol #. This just does
#a num to string coversion.
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

#iterates over entire pcap file and returns dictionary
#of important info for graph
def complete_view(testfile):
    result = {}	  # dictionary that will hold src/dest ip addr's
    # basic error checking
    if not os.path.exists(testfile):
        print 'Error, cannot load file'
        sys.exit(1)
    else:
        p = rdpcap(testfile)
        for pkt in p:
            src_ip = pkt[IP].src
            dest_ip = pkt[IP].dst
            protocol = pkt[IP].proto
            result.setdefault('src_ip', []).append(src_ip)
            result.setdefault('dest_ip', []).append(dest_ip)
            result.setdefault('protocol', []).append(protocol_replace(protocol))

	return result

#any pkt with a data > .75*MTU is likely indicative
#of a file transfer and should be investigated further
def file_transfer(testfile):
    result ={}
    if not os.path.exists("./file_transfer_log"):
        os.mkdir("./file_transfer_log")
    if not os.path.exists(testfile):
        print 'Error, cannot load file'
        sys.exit(1)
    else:
        p = rdpcap(testfile)
        sys.stdout = open(os.path.join('./file_transfer_log', '%s_file_transfer.txt' % testfile[:-5]), 'w+')
        for pkt in p:
            if int(pkt[IP].len) > 1125:
                print pkt.show()
                result.setdefault('src_ip', []).append(pkt[IP].src)
                result.setdefault('dest_ip', []).append(pkt[IP].dst)
                result.setdefault('protocol', []).append(protocol_replace(pkt[IP].proto))

    return result
