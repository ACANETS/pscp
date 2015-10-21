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


# This file is used to collect the details (routes' IP addresses) of traceroute tests

import os
import json
import requests
import sys

f  = open('filtered_ma_list','r')
ma = json.load(f)
f.close()
print ma

tracepath_ps = [] 

counter = 0
for name in ma:  # Each perfsonar node
	try:
		data = requests.get(name +"?format=json",timeout=10)
	except:
        	continue

	if data is None:       # Skip this node if its MA has no data
		continue
	else:
		try:
			data0 = data.json()
		except:
			continue

	if len(data0) == 0:
		continue

	for k in data0:	# Each traceroute test in ps node
		try:
			test = k['tool-name'][0:15]
		except: 
			continue
		if k['tool-name'][0:15] == 'bwctl/tracepath':  # Filter the test
			try:
				trace_ps0 = requests.get('http://' + k['input-source'] + k['uri'] + 'packet-trace/base?format=json',timeout=10)
			except:
				continue

			if trace_ps0 is None:
				continue
			else:
				try:
					trace_ps = trace_ps0.json()
				except:
					continue

			if len(trace_ps) == 0:
				continue
			else: 	
				try:
					test = trace_ps[0]['val']  # Jsut need one path since others are alomost the same
				except:
					continue
                                print trace_ps[0]

				ip_addr = []    
				for i in trace_ps[0]['val']:
					ip_addr.append(i['ip'])
				ip_addr.insert(0,k['input-source'])
				ip_addr = sorted(set(ip_addr),key=ip_addr.index)
				print "################################################"
				print ip_addr
				print "################################################"
				tracepath_ps.append(ip_addr)
				print tracepath_ps
				print "################################################"

	counter = counter + 1
	if (counter%50) == 0:
		f = open('data'+ str(counter) ,'w+')
		json.dump(tracepath_ps,f)
		f.close()
