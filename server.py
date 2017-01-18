#! /usr/bin/python
import subprocess
import os


def server(directory):
	os.chdir(directory)
	print "Starting server in %s" % os.getcwd() 
	subprocess.call(['python','-m','SimpleHTTPServer'])

