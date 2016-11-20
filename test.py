import os
import sys
from scapy.all import *
# function that parses out everthing except src > dest/protocol
# Returns dictionary object with parsed data


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
        print protocol

def file_transfer(pcap):
    transfer ={}
    with open('file_transfer.txt', 'w+') as outfile:
        for pkt in pcap:
            if int(pkt[IP].len) > 1125:
                outfile.write("src_ip: %s" % pkt[IP].src)
                outfile.write("dest_ip: %s" % pkt[IP].dst)
                outfile.write("pkt_len: %i" % pkt[IP].len)
                outfile.write("payload: %s" % pkt[Raw].load)

                transfer.setdefault('src_ip', []).append(pkt[IP].src)
                transfer.setdefault('dest_ip', []).append(pkt[IP].dst)
                transfer.setdefault('protocol', []).append(pkt[IP].protocol_replace(proto))

    return transfer

def parse_line(testfile):
    result = {}  # dictionary that will hold src/dest ip addr's
    pkt_len = 0
    i = 0

    # basic error checking
    if not os.path.exists(testfile):
        print 'Error, cannot load file'
        sys.exit(1)
    else:
        p = rdpcap(testfile)
        # sessions = p.sessions()

        for packet in p:
            print protocol_replace(packet[IP].proto)
            '''
            try:
                i += 1
                #print "[*]packet length: %i" % packet[IP].len
                pkt_len += packet[IP].len
            except IndexError:
                print "out of range"
        avg_pkt_len = pkt_len / i
        for pkt in p:
            try:
                if pkt[IP].len > avg_pkt_len:
                    pkt.show()
                    #pkt[Raw].load

                else:
                    continue
            exceptnano IndexError:
                print "out of range"
                # split = session.split()
                # result.setdefault('src_ip', []).append(split[1])
                # result.setdefault('dest_ip', []).append(split[3])
                # result.setdefault('protocol', []).append(split[0])

    return result
    '''

def ip_generate():
    GOOD_IP = []

    for i in range(0, 256):
        GOOD_IP.append('192.168.1.'+str(i))

    print GOOD_IP

ip_generate()
#parse_line('blackhole.pcap')
