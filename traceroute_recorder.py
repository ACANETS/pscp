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

ma = []
traceroute_test = {}

f = open('ma_list','r')
ma = json.load(f)
f.close()

for name in ma:
	try:	
		data = requests.get(name+ "?format=json")
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
	traceroute_test[node] = []
	for k in data0:
		try:
			test = k['tool-name'][0:15]
		except:
			 continue
		if k['tool-name'][0:15] == 'bwctl/tracepath':
			traceroute_test[node].append('http://' + k['input-source'] + k['uri'] + 'pacet-trace/base?format=json')
	f = open('ma_record','w+')
	json.dump(traceroute_test,f)
	f.close() 	
