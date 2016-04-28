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

import os
import json
import requests
import sys

tp_ps = [] 

if __name__ == "__main__":
	try: 
		src_host = sys.argv[1]
		dst_host = sys.argv[2]
	except:
		print "Input error"

	try:
		url1 = "http://"+ src_host +"/esmond/perfsonar/archive/?format=json"
		data = requests.get(url1,timeout=10)
	except:
		print "Request error"

	if data is None:
		print "Data is empty"
	else:
		try:
			data0 = data.json()
		except:
			print "Json error"

	if len(data0) == 0:
		print "Record is empty"

	for k in data0:	#each throughput test in ps node
		if k['tool-name'][0:11] == 'bwctl/iperf' and k['destination'] == dst_host:
			try:
				url2 = 'http://' + src_host + k['uri'] + 'throughput/base?format=json'
				
				tp_ps0 = requests.get(url2, timeout=10)
			except:
				continue

			if tp_ps0 is None:
				continue
			else:
				try:
					tp_ps = tp_ps0.json()
					#print tp_ps
				except:
					continue

			if len(tp_ps) == 0:
				continue
			else: 	
				tp_record = []
				for i in range(0,len(tp_ps)):
					tp_record.append(int(tp_ps[i]['val']))
				tp_record.sort()
				print tp_record
				number = len(tp_record)/5
				tp_threshold = sum(int(tp_record[j]) for j in range(0,number))/number
				print tp_threshold
				sys.exit(1)
                                
		
