from graph import *

#provide the name of the file which contains all the tracepaths
#build the graph upon the file
file_name = "new_dataset"
g = build_graph_from_file(file_name)

#debug and print the graph
print g
print "\n\n\n"


#trace_path = ["pr20.uml.edu", "129.63.205.254", "172.16.4.25", "129.63.189.34", "172.16.5.1", "172.16.1.240", "69.16.3.7", "207.210.143.57", "192.5.89.18", "198.71.45.8", "198.71.45.234", "192.5.170.222", "130.202.222.81", "140.221.47.250", "140.221.68.2"]

#trace_path = ["pr20.uml.edu", "129.63.205.254", "172.16.4.25", "129.63.189.34", "172.16.5.1", "172.16.1.240", "69.16.3.7", "207.210.143.57", "192.5.89.18", "198.71.45.8", "149.165.254.185", "149.165.254.250", "149.165.225.224"]

#trace_path = ["pr20.uml.edu", "129.63.205.254", "172.16.4.25", "129.63.189.34", "172.16.5.1", "172.16.1.240", "69.16.3.7", "207.210.143.57", "192.5.89.18", "198.71.45.5", "198.71.45.228", "206.196.177.149", "129.2.0.229", "129.2.0.85", "129.2.0.213", "128.8.17.54"]

#trace_path = ["pr20.uml.edu", "129.63.205.254", "172.16.4.25", "129.63.189.34", "172.16.5.1", "172.16.1.240", "69.16.3.7", "207.210.143.57", "192.5.89.18", "198.71.45.8", "164.113.255.249", "164.113.255.46", "129.93.5.165"]

#trace_path = ["pr20.uml.edu", "129.63.205.254", "172.16.4.25", "129.63.189.34", "172.16.5.1", "172.16.1.240", "69.16.3.7", "69.16.3.249", "38.104.218.13", "154.54.3.197", "154.54.3.93", "154.54.31.125", "154.54.41.46", "154.24.22.130", "38.104.168.234", "208.65.23.1", "208.65.23.67", "208.65.23.44"]

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

new_path = find_pr_path(trace_path, rng, tol)
print new_path
print "\n\n\n"


