###################################################
#Copyright © 2015 by ACANETS. All rights reserved.#
###################################################


# perfsonar control plane


import os
import json
import sys
import re
import time
import urllib2
import requests

SLEEP_TIME = 60  #run a throughput test every 60 seconds

print_info =  "Please follow this formate to start the program\n\tcontrol_plane.py [source_host_name] [destination_host_name]\n\n\tsource_host_name: The host name or IP address where the test starts from\n\tdestination_host_name: The host name or IP addree where the test ends to\n"

#Start a new bwctl test
def bwctl_test(src_host,dst_host):
	throughput0 = os.popen('bwctl -s ' + src_host + ' -c ' + dst_host + ' -t 20').read()
	print throughput0
	throughput = re.findall(r'(\d+)\sbits',throughput0)
	print throughput
	return throughput[0]

#Start a traceroute test
def trace_test(src_host, dst_host):
	trace0 = os.popen('bwtraceroute -s ' + src_host + ' -c ' + dst_host).read()
	trace = re.findall(r'\((\d+\.\d+\.\d+\.\d+)\)',trace0)
	del trace[0]
	trace.insert(0,src_host)
	print trace0
	return trace

if __name__ == "__main__":
	try:
        	src_host = sys.argv[1]
        	dst_host = sys.argv[2]

	except:
        	print print_info
		sys.exit(0)

	if len(sys.argv) != 3:
		print print_info
		sys.exit(0)

	
	while 1:
		tp_value = bwctl_test(src_host,dst_host)
        if int(tp_value) < 200000000: #200Mbps
			print "The path has a fault!"
            trace = trace_test(src_host,dst_host)
                #find nearest ps node
                #locate the problematic source
		else:	
			time.sleep(SLEEP_TIME)

	print "The throughput is: " + tp_value + "bits/s"
	print "\n"
	print "The traceroute is:\n"
	print trace
	print "\n"

