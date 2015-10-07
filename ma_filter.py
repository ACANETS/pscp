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
import sys
import re

f = open('ma_list','r')
ma = json.load(f)
print ma
f.close

filtered_ma = []
for i in ma:
	ping0 = os.popen('ping -c 5 ' + i[7:len(i)-25]).read()
	print ping0
	ping_value = re.findall(r'time=(\d+\.\d+)\sms',ping0)
	if len(ping_value) != 0:
		filtered_ma.append(i)
        print "################"
	print filtered_ma
        print "################"

fp = open('filtered_ma_list', 'a+')
json.dump(filtered_ma,fp)
fp.close() 
	
