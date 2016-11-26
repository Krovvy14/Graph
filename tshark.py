import subprocess
import os



# Starts a tshark packet capture and saves it to a file
# in the location that is passed as a functional parameter.
# Currently it creates files the size of 10MB.

def traffic_capture(out_directory):
	# check if the directory given exists, if not create it.
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
    os.chdir(out_directory)
    process = subprocess.call(['tshark', '-i', '1', '-b', 'filesize:1000', '-b',
                      'files:10000', '-w', 'capture'])
