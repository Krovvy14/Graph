import os
import sys

#function that parses out everthing except src > dest/protocol 
#Returns dictionary object with parsed data
def parse_line(testfile):
	result = {}	#dictionary that will hold src/dest ip addr's
	
	# basic error checking
	if not os.path.exists(testfile):
		print 'Error, cannot load file'
		sys.exit(1)
	else:
		with open(testfile,'r') as source_file:
			#read in file; split on ' '; add src/dest to dict
			for source_line in source_file:
				results = source_line.split()
				result.setdefault('src_ip',[]).append(results[2])
				result.setdefault('dest_ip',[]).append(results[4])
				result.setdefault('protocol',[]).append(results[5])
	
	return result
