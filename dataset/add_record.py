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

import json
import sys

file_name = sys.argv[1]

f = open(file_name,'r')
a = json.load(f)
g = open('datatotal','r')
b = json.load(g)

for i in a:
	if i not in b:
		b.append(i)
c = b

f.close()
g.close()
print len(c)

h = open('datatotal','w')
json.dump(c,h)
h.close()
