###########################################################################
# Copyright 2015 by ACANETS                                               #
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

#This file provides an example for how to visulize the traceroute graph
#Please follow https://pypi.python.org/pypi/graphviz to install the necessary packages first
from build_graph import *
from find_ps_node import *
from graphviz import *
import os

#provide the name of the file which contains all the tracepaths
#build the graph upon the file
file_name = "dataset95"
g = build_graph_from_file_IP(file_name)

#use graphvz to generate the DOT file
dot = Graph(comment='The Traceroute Graph')
dot.engine = 'sfdp'

pair_checked = {}
vers = g.keys()
total_len = len(vers)
for ver in vers:
	if g[ver]["type"] == "P":
		dot.node(ver, color = 'red')
	else:
		dot.node(ver)
for ver in vers:
	for adj in g[ver]["adjacent"]:
		if pair_checked.get(adj + "-" + ver) == None:
			dot.edge(ver, adj)
			pair_checked[ver + "-" + adj] = ""
		
		
f = open('traceroute.gv', 'w')
f.write(dot.source)

#system call the sfdp command in the graphviz package to generate the graph
os.system("sfdp -x -Goverlap=prism -Tpng traceroute.gv  > traceroute.png")
