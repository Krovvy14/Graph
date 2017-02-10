# Graph
Dependencies: tshark, sigma.js (follow install guidelines)

This project can be run in two modes: read or write

Read mode: The project reads all pcap files files pointed to by the path provided on the command line. Those pcap files are then converted into a semi-colon separated value and ingested into a neo4j database over an http connection.

e.g. python main.py -r /path/to/pcap/files

Write mode: The project will start a tshark process and begin collecting network traffic. All pcap file will be written to a /tmp/pcap directory that is created if it does not already exist. These pcap files are than automatically converted to a csv and ingested in the same fashion as the read mode above.

e.g. python main.py -w

TODO: Web application front end
