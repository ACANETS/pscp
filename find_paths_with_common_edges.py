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

# This function finds the other possible 'paths' that share the 'num_comm_edges' common edges with 'trace_path' in the 'graph'
# We only consider the concatenated common edges
def find_paths_with_common_edges(graph = {}, trace_path = [], num_comm_edges = 0):
	paths = {}
	if(len(trace_path) < 4) or (num_comm_edges <= 0):
		return paths		
	i = 1
	while (i+num_comm_edges) <= (len(trace_path)-2):
		start_end_set = set( [] )
		if (trace_path[i] != None) and (trace_path[i] != "reply") and (":" not in trace_path[i]) and (trace_path[i+num_comm_edges] != None) and (trace_path[i+num_comm_edges] != "reply") and (":" not in trace_path[i+num_comm_edges]):
			start_end_set = set( collect_start_end(graph[trace_path[i]]["paths"]) )
			for j in range(i+1, i+num_comm_edges+1):
				if (trace_path[j] != None) and (trace_path[j] != "reply") and (":" not in trace_path[j]):
					start_end_set &= set( collect_start_end(graph[trace_path[j]]["paths"]) )
				else:
					start_end_set = set([])
					break;
			temp = list(start_end_set)
			start_end = []
			for j in range(len(temp)):
				if (temp[j].split()[0] != trace_path[0]) and (temp[j].split()[1] != trace_path[len(trace_path)-1]):
					start_end.append(temp[j])			
			paths[trace_path[i] + "  " + trace_path[i+num_comm_edges]] = start_end
		i += 1
	return paths
	
	
def collect_start_end(paths = []):
	start_end = []
	for i in range(len(paths)):
		start_end.append(paths[i]["Start"] + "  " + paths[i]["End"])
	return start_end
	
