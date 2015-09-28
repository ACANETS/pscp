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
		
#build a new path consisting of the nearest perfsonar nodes for each router on the 'trace_path'
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
	
def find_pr_path(trace_path = [], rng=1, tol=32):
	file_name = "new_dataset"
	g = build_graph_from_file(file_name)
	new_path = build_pr_path(g, trace_path, rng, tol)
	return new_path
