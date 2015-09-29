###################################################
#Copyright (c) 2015 by ACANETS. All rights reserved.#
###################################################

import os
import json
import sys
import re

def locator(ps_trace,tp_value):
    	test_throughput1 = []
    	test_throughput2 = []
    
   	 #Start from A
    	for i in range(1,len(ps_trace)-1): 
            	tp0 = os.popen('bwctl -s ' + ps_trace[0] + ' -c ' + ps_trace[i] + ' -t 20').read()
	       	print tp0
		tp1 = re.findall(r'(\d+)\sbits',tp0)
		if len(tp1) != 0:
	     		test_throughput1.append(tp1[0])
		else:
            		test_throughput1.append('0')
    	test_throughput1.append(tp_value)
	print "Results from " + ps_trace[0] + " is:"
	print test_throughput1
	print "\n"
      
    	#Start from B
    	for i in range(1,len(ps_trace)-1):
           	tp2 = os.popen('bwctl -s ' + ps_trace[len(ps_trace)-1] + ' -c ' + ps_trace[i] + ' -t 20').read()
	       	print tp2
		tp3 = re.findall(r'(\d+)\sbits',tp2)
		if len(tp3) != 0:     	
			test_throughput2.insert(0,tp3[0])
		else:
            		test_throughput2.insert(0,'0')
    	test_throughput2.insert(0,tp_value) 	
	print "Results from " + ps_trace[-1] + " is:"
	print test_throughput2
	print "\n"
 
    	for i in range(0,len(test_throughput1)-1):
            	if int(test_throughput1[i]) > 1000000000 and int(test_throughput1[i+1]) < 100000000:
          		print "The problem path is from " + ps_trace[i+1] + " to  " + ps_trace[i+2]
    	for i in range(1,len(test_throughput2))[::-1]:
            	if int(test_throughput2[i]) > 1000000000 and int(test_throughput2[i-1]) < 100000000:
            		print "The problem path is from " + ps_trace[i-1] + " to  " + ps_trace[i-2] 
    
    
