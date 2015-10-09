###########################################################################
# Copyright 2015 by ACANETS Lab at University of Massachusetts Lowell     #
#                                                                         #
# Licensed under the Apache License, Version 2.0 (the "License");         #
# you may not use this file except in compliance with the License.        #
# You may obtain a copy of the License at                                 #
#                                                                         #
#    http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                         #
# Unless required by applicable law or agreed to in writing, software     #
# distributed under the License is distributed on an "AS IS" BASIS,       #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.#
# See the License for the specific language governing permissions and     #
# limitations under the License.                                          #
###########################################################################

# perfsonar control plane

import os
import json
import sys
import re
import time
import datetime
from find_ps_node import *
from issue_locator import locator

SLEEP_TIME = 60  	 #run a throughput test every 60 seconds
RNG = 3          	 #the distance betweeb ps node and target router
TOL = 24         	 #subnet range
TP_THRESHOLD = 100000000 # Set the threshold to define the problematic path

print_info =  "Please follow this formate to start the program:\n\tcontrol_plane.py [source_host_name] [destination_host_name]\n\n\tsource_host_name: The host name or IP address where the test starts from\n\tdestination_host_name: The host name or IP addree where the test ends to\n"

# Start a new bwctl test
def bwctl_test(src_host,dst_host):
	try:
		throughput0 = os.popen('bwctl -s ' + src_host + ' -c ' + dst_host + ' -t 20').read()
		print throughput0
		throughput = re.findall(r'(\d+)\sbits',throughput0)
		return throughput[0]
	except:
		return 0

# Start a traceroute test
def trace_test(src_host, dst_host):
	while 1:
		trace0 = os.popen('bwtraceroute -s ' + src_host + ' -c ' + dst_host).read()
		print trace0
		trace = re.findall(r'\((\d+\.\d+\.\d+\.\d+)\)',trace0)
		if len(trace) != 0:
			break
	del trace[0]
	trace.insert(0,src_host)
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
	print "PSCP starts..."
	print "\n"

    	# Start monitoring
	while 1:
		tp_value = bwctl_test(src_host,dst_host)       # Check the throughput performance using bwctl tool
        	print "The throughput is: " + str(tp_value) + " bits/s"
        	print "\n"

        	if int(tp_value) < TP_THRESHOLD: 

			print "The path has a problem!!!!\n"

                	start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            		print "Troubleshooting starts at " + start_time 
			
			trace = trace_test(src_host,dst_host)         # Obtian the traceroute info using bwtraceroute tool
            		print "###########################################################"
            		print "The traceroute is:"
            		print trace
			print "###########################################################"
          	  	ps_trace = find_pr_path(trace,RNG,TOL)		# Find nearest ps nodes for target routers
           		print "The traceroute after replacing is:"
			print ps_trace
			print "###########################################################"
 			print "\n"

	            	location = locator(ps_trace,tp_value)		# Locate the problematic source(s)
			
			end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			print "Troubleshooting ends at " + end_time
               		sys.exit(0) 
		else:	
			time.sleep(SLEEP_TIME)




