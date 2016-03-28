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


# This script is used for filtering the bad url from ma_list and keep the good url

import os
import json
import sys
import re
from query_diy import get_service_locator

ma = get_service_locator("service-type=ma") #return all the MA hostnames
f = open('ma_list','w+')
json.dump(ma,f)
f.close

filtered_ma = []
count = 1.0
bar_length = 100


for i in ma:
	ping0 = os.popen('ping -c 3 ' + i[7:len(i)-25]).read()   #Use ping tool to check the network connection
	print ping0
	ping_value = re.findall(r'time=(\d+\.\d+)\sms',ping0)
	if len(ping_value) != 0:
		filtered_ma.append(i)
	print filtered_ma

	# Print a progress bar
	percentage = (count/len(ma))*100
	hashes = '#' * int(percentage)
	spaces = ' ' * (bar_length - len(hashes))
	print "\n"
	print str(int(percentage)) + "% [" + hashes + spaces + "]"
	print "\n"
	count = count + 1.0

# Write the filter result to a new file 
fp = open('filtered_ma_list', 'w+')
json.dump(filtered_ma,fp)
fp.close() 
	
