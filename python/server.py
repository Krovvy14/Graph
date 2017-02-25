#! /usr/bin/python
import subprocess
import os


def server(directory, port):
    port = port
    os.chdir(directory)
    print "Starting server in %s" % os.getcwd() 
    subprocess.call(['python','-m','SimpleHTTPServer', _port])

