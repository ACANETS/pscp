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

#convert every hostname on the trace_path to ip address by using the socket
def path_to_ippath(trace_path=[]):
	for i in range(len(trace_path)):
		try:
			trace_path[i] = socket.gethostbyname(trace_path[i])
		except:
			continue
	return trace_path

#insert the trace_path into the graph
def build_graph(graph = {}, trace_path = []):
	if len(trace_path) < 2:
		return graph
		
	for i in range(0, len(trace_path)):
		if trace_path[i] != None and ":" in trace_path[i]:
			return graph
		
	for i in range(len(trace_path)):
		if trace_path[i] == None or trace_path[i] == "reply":
			continue
			
		if graph.get(trace_path[i]) == None:
			graph[trace_path[i]] = {}
			graph[trace_path[i]]["type"] = []
			graph[trace_path[i]]["adjacent"] = []	
			
		if  i == 0:
			graph[trace_path[i]]["type"] = "P"
			if trace_path[i+1] not in graph[trace_path[i]]["adjacent"] and trace_path[i+1] != None and trace_path[i+1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i+1])
			
		elif i == len(trace_path) - 1:
			graph[trace_path[i]]["type"] = "P"
			if trace_path[i-1] not in graph[trace_path[i]]["adjacent"] and trace_path[i-1] != None and trace_path[i-1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i-1])
		else:
			if graph[trace_path[i]]["type"] != "P":
				graph[trace_path[i]]["type"] = "R"
			if trace_path[i-1] not in graph[trace_path[i]]["adjacent"] and trace_path[i-1] != None and trace_path[i-1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i-1])
			if trace_path[i+1] not in graph[trace_path[i]]["adjacent"] and trace_path[i+1] != None and trace_path[i+1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i+1])
			
	return graph
	
#insert the trace_path into the graph, plus converting the hostname to ip address	
def build_graph_IP(graph = {}, trace_path = []):
	if len(trace_path) < 2:
		return graph
		
	for i in range(0, len(trace_path)):
		if trace_path[i] != None and ":" in trace_path[i]:
			return graph
	
	path_to_ippath(trace_path)
		
	for i in range(len(trace_path)):
		if trace_path[i] == None or trace_path[i] == "reply":
			continue
			
		if graph.get(trace_path[i]) == None:
			graph[trace_path[i]] = {}
			graph[trace_path[i]]["type"] = []
			graph[trace_path[i]]["adjacent"] = []	
			
		if  i == 0:
			graph[trace_path[i]]["type"] = "P"
			if trace_path[i+1] not in graph[trace_path[i]]["adjacent"] and trace_path[i+1] != None and trace_path[i+1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i+1])
			
		elif i == len(trace_path) - 1:
			graph[trace_path[i]]["type"] = "P"
			if trace_path[i-1] not in graph[trace_path[i]]["adjacent"] and trace_path[i-1] != None and trace_path[i-1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i-1])
		else:
			if graph[trace_path[i]]["type"] != "P":
				graph[trace_path[i]]["type"] = "R"
			if trace_path[i-1] not in graph[trace_path[i]]["adjacent"] and trace_path[i-1] != None and trace_path[i-1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i-1])
			if trace_path[i+1] not in graph[trace_path[i]]["adjacent"] and trace_path[i+1] != None and trace_path[i+1] != "reply":
				graph[trace_path[i]]["adjacent"].append(trace_path[i+1])
			
	return graph

#build the graph from a tracepaht file, the file format is jason in the form of [ [], [], [], ..., [] ]
def build_graph_from_file(file_name = ""):
	graph = {}
	f_handle = open(file_name, "r")
	f_json = f_handle.read()
	f_list = json.loads(f_json)
	for trace_path in f_list:
		graph = build_graph(graph, trace_path)
	
	return graph	
#build the graph from a tracepaht file, the file format is jason in the form of [ [], [], [], ..., [] ]
#plus converting the hostname to ip address	
def build_graph_from_file_IP(file_name = ""):
	graph = {}
	f_handle = open(file_name, "r")
	f_json = f_handle.read()
	f_list = json.loads(f_json)
	for trace_path in f_list:
		graph = build_graph_IP(graph, trace_path)
	
	return graph
