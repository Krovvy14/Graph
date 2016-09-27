import subprocess
'''
Starts a tshark pacet capture and saves it to a file
that is passed as a functional parameter.  At the moment
it captures 150 packets. That is what looks the most
"clean" in my current graph building module.
'''
def tshark(filename):
	tshark_out = open(filename, "wb")
	subprocess.Popen(['tshark', '-i', '1', '-c', '150'],\
	stdout=tshark_out)
	
