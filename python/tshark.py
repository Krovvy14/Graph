#######################################################
#tshark.py											  #
#######################################################
import os
import subprocess

def traffic_capture(out_directory):

	if not os.path.exists(out_directory):
		os.mkdir(out_directory)

	os.chdir(out_directory)
	process = subprocess.call(['tshark', '-i', '1', '-b', 'filesize:1000', '-b','files:10000', '-w', 'capture'])

