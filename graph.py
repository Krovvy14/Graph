from igraph import *
import os
import sys

file = '/home/batman/Documents/MastersProject/packetCapture.txt'
"""
def file_len(file):
    len=0
    if not os.path.exists(file):
        print 'Error, cannot find file!'
        sys.exit(1)
    else:
        with open(file,'r') as src_file:
            for line in src_file:
                len+=1
    return len
"""    
def build_graph():
    g = Graph([(0,2),(2,3),(3,4),(1,3),(2,4),(3,1)])
    g.vs["src_ip"] = ["1.1.1.1","1.1.1.2","1.1.1.3","1.1.1.4","1.1.1.5"]
    layout = g.layout("kamada_kawai")
    g.vs["label"] = g.vs["src_ip"]
    plot(g,layout = layout)
      
    
def main():
    #print "The number of lines is: ", file_len(file)
    build_graph()
    
if __name__ == '__main__':
	main()
    
