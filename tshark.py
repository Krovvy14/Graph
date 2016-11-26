import subprocess
import os
import signal

'''
Starts a tshark pacet capture and saves it to a file
that is passed as a functional parameter.  At the moment
it captures 150 packets. That is what looks the most
"clean" in my current graph building module.
'''
def traffic_capture(out_directory):
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
    os.chdir(out_directory)
    process = subprocess.call(['tshark', '-i', '1', '-b', 'filesize:1000', '-b',
                      'files:10000', '-w', 'capture'])
    if signal.SIGINT:
        os.kill(process.pid, signal.SIGINT)
