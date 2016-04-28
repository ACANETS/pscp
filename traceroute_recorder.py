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


# This file is used to record the bwctl/traceroute test uri in MAs and put all the records into a file

import os
import json
import requests
import sys
import time



f = open('filtered_ma_list','r')
ma = json.load(f)
print ma
f.close()

count = 1.0
bar_length = 100
timestamp = int(time.time())
traceroute_test = {}

for name in ma:
	percentage = (count/len(ma))*100
    	hashes = '#' * int(percentage)
    	spaces = ' ' * (bar_length - len(hashes))
    	count = count + 1.0
    	print str(int(percentage)) + "% [" + hashes +spaces + "]"
    	print "\n"
        
	try:	
		data = requests.get(name+ "?format=json",timeout=10)
	except:
		continue
	if data is None:
		continue
	else:
		try:
			data0 = data.json()
		except:
			continue
	if len(data0) == 0:
		continue
	node = name[7:len(name)-25]
	traceroute_test[node] = {}
	traceroute_test[node]['uri'] = []
	for k in data0:
		try:
			test = k['tool-name'][0:15]
		except:
			 continue
		if k['tool-name'][0:15] == 'bwctl/tracepath':			
			record = 'http://' + name[7:-25] + k['uri'] + 'pacet-trace/base?format=json'
			#record['ts'] = k['event-types'][0]['time-updated']
			traceroute_test[node]['uri'].append(record)
	print traceroute_test
	print "\n"

	f = open('ma_record_'+ str(timestamp),'w+')
	json.dump(traceroute_test,f)
	f.close() 	
