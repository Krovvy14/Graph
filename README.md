# Graph
Dependencies: neo4j, tshark, sigma.js (follow install guidelines)

Prerequisites: The neo4j database must be up and running before this program is run.

This project can be run in two modes: read or write

Read mode: The project reads all pcap files files pointed to by the path provided on the command line. Those pcap files are then converted into a semi-colon separated value and ingested into a neo4j database over an http connection.

e.g. python main.py -r /path/to/pcap/files

Write mode: The project will start a tshark process and begin collecting network traffic. All pcap file will be written to a pcap directory within the directory the program is started from. If a /pcap directory does not already exist one will be created. These pcap files are than automatically converted to a csv(in reality it is a '|' separated list) and ingested in the same fashion as the read mode above.

e.g. python main.py -w

TODO: Web application front end
