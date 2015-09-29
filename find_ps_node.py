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

from sets import Set
import json
import socket
import random

#find the perfsonar nodes in the range of rng around the given node pr_node
#it uses the BFS algorithm
def find_pr_node_in_range(graph={}, pr_node="", rng=0):
	pr_node_in_range = {}
	if graph.get(pr_node) != None:
		visited = []
		to_visit = []
		to_visit.append(pr_node)
		for i in range(1, rng+1):
			pr_node_in_range[i] = []
			count = len(to_visit)
			for j in range(count):
				adj_nodes = graph[to_visit[0]]["adjacent"]
				visited.append(to_visit[0])
				to_visit.pop(0)
				for k in range(len(adj_nodes)):
					if adj_nodes[k] not in visited and adj_nodes[k] not in to_visit:
						to_visit.append(adj_nodes[k])
			for j in range(len(to_visit)):
				if graph[to_visit[j]]["type"] == "P":
					pr_node_in_range[i].append(to_visit[j])
		
	return pr_node_in_range
	
#find the perfsonar nodes in the range of 'rng' around the given node 'pr_node' with a tolerance 'tol'
#it uses the BFS algorithm	
#in order to delete the possilbe repeated nodes, it uses set to do so
def appro_find_pr_node_in_range(graph={}, pr_node="", rng=1, tol=32):
	appro_pr_node_in_range = []
	IPs = graph.keys()
	appro_IPs = []
	bin_pr_node = ''.join([bin(int(x)+256)[3:] for x in pr_node.split('.')])
	for ip in IPs:
		if ":" in ip or graph[ip]["type"] == "P":
			continue
		bin_ip = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
		if bin_pr_node[0:tol-1] == bin_ip[0:tol-1]:
			appro_IPs.append(ip)
			
	for prn in appro_IPs:
		appro_pr_node_in_range.append( find_pr_node_in_range(graph, prn, rng) )
		
	empty_dic = {}
	for i in range(0, rng+1):
		empty_dic[i] = []
		
	if graph[pr_node]["type"] == "P":
		empty_dic[0].append(pr_node)
	
	for i in range(len(appro_pr_node_in_range)):
		for j in range(1, rng+1):
			set1 = set(appro_pr_node_in_range[i][j])
			set2 = set(empty_dic[j])
			set3 = set1 | set2
			empty_dic[j] = list(set3)
	if rng == 1:
		return empty_dic
	elif rng > 1:
		for i in range(2, rng+1):
			set2 = set(empty_dic[i])
			for j in range(i-1, 0, -1):
				set1 = set(empty_dic[j])
				set2 = set2 - set1
			empty_dic[i] = list(set2)
		return empty_dic
		
#build a new path consisting of the nearest perfsonar nodes for each router on the 'trace_path' based upon the graph info
def build_pr_path(graph={}, trace_path = [], rng=1, tol=32):
	new_path = []
	new_path.append(trace_path[0])
	random.seed()
	for i in range(1, len(trace_path)-1): #no start and end
		info = appro_find_pr_node_in_range(graph, trace_path[i], rng, tol)
		flag = 0
		for j in range(0, rng+1):
			if len(info[j]) == 0:
				continue
			else:
				new_path.append(info[j][random.randint(0, len(info[j])-1)])
				flag = 1
				break
		if flag == 0:
			new_path.append("None")
	new_path.append(trace_path[len(trace_path)-1])	
	return new_path

#kind of overloading of the function build_pr_path,
#it uses the dataset95 to generate the graph and then calls the build_pr_path
#this function is used for our test	
def find_pr_path(trace_path = [], rng=1, tol=32):
	file_name = "dataset95"
	g = build_graph_from_file(file_name)
	new_path = build_pr_path(g, trace_path, rng, tol)
	return new_path
