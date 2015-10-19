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

from build_graph import *
from find_ps_node import *

#provide the name of the file which contains all the tracepaths
#build the graph upon the file
file_name = "dataset95"
g = build_graph_from_file(file_name)

#debug and print the graph
print g
print "\n\n\n"


#pick the possibly problematic trace_path from the file
trace_path = ["pr20.uml.edu", "129.63.205.254", "172.16.4.25", "129.63.189.34", "172.16.5.1", "172.16.1.240", "69.16.3.7", "207.210.143.57", "192.5.89.18", "198.71.45.8", "192.170.225.5", "192.170.224.78", "192.170.227.164"]

#debug and print the trace_path
print trace_path
print "\n\n\n"


#set up the parameters and build a new path which consists of all the nearest perfsonar nodes for each router on the path
rng = 3
tol = 24
new_path = build_pr_path(g, trace_path, rng, tol)

#debug and print the new_path
print new_path
print "\n\n\n"

#find_pr_path is an extended version of build_pr_path, this function implicity uses the dataset95
new_path = find_pr_path(trace_path, rng, tol)
print new_path
print "\n\n\n"


