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
import re

# Start a new bwctl test
def bwctl_test(src_host,dst_host):
	try:
		throughput0 = os.popen('bwctl -s ' + src_host + ' -c ' + dst_host + ' -t 20 -f b').read()
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
