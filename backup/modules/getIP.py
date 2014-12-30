#!usr/bin/python

#----MODULE TO DISPLAY OR RETURN IP ADDRESS----

# v0.1

import subprocess
import socket
import fcntl
import struct

def findIP():
	# Find the IP address:
	ifname='eth0'
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	IPaddress=socket.inet_ntoa(fcntl.ioctl(
	                s.fileno(), 0x8915,
	                struct.pack('256s',ifname[:15])
	                )[20:24])
	IPstring = str(IPaddress)
	return IPstring

def wifiIP():
	output = subprocess.check_output("sudo hostname -I", shell=True)
	return output


def main():
	try:
		currentIP = findIP()
		print "Current IP address is %s" % currentIP
	except:
		print "Physical connection could not be found, wireless IP search returned:"
		print wifiIP()

if __name__ == "__main__":
	main()

