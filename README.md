#PerfSONAR Control Plane (pscp)

Our control plane is used to start a test between two perfSONAR hosts, monitor the throughput performance and locate the source of network issues when problem happens.

### 1.Preparation Work: offline Measurement Archive (MA) data collecting
 
 traceroute_collector.py can build a traceroute dataset by retrieving the traceroute tests records in hosts' MAs using perfSONAR client REST interface.
 
 To start collecting traceroute data from MA hosts, use command:
 
        python traceroute_collector.py

 In this program, we collect the traceroute details from dataset "filtered_ma_list". To obtain this dataset, we use the following tools.
 
##### 1.1 ma_filter.py
 
 This script is used to check the network connection to MAs by using ping. At the end, it will return two files: ma_list and filtered_ma_list. 
 In this script, we deploy a module: query_diy.py
 
 1.1.1 query_diy.py 
 
 It is a module in this program which is used to return a list of MA hosts from perfSONAR lookup service directory.
 
### 2.Online Control Plane
 
 control_plane.py is the code for online measurement test controls. We implement the meaausrement and troubleshooting methods between two specific perfSONAR nodes.

 To start the control plane, use command:
   
     python control_plane.py [source_host_name] [destination_host_name]
     
In control_plane.py, we deploy the following three modules: bwctl_tools.py, find_ps_node.py and issue_locator.py

##### 2.1 bwctl_tool.py
 
 This module is used to start a throughput test (use bwctl tool) or a traceroute test (use bwtraceroute tool) and return the result.
 
##### 2.2 find_ps_node.py 
      
After obtaining the traceroute of a problematic path, this module is used to find the nearest perfSONAR node for each target router on the path by looking up the graph we built.

 2.2.1 build_graph.py 
 
 The objective is to build a traceroute graph for find_ps_node module when we detect the abnormalities.

 2.2.2 graph_example.py 
 
 This is a small example of replacing the IP address of target routers on a specific path with perfSONAR nodes' IP.

##### 2.3 issue_locator.py 
 
  An example of problematic path:    
  
      A-----C--X--D-----E-----F-----I-----H-----G-----B

After replacing the routers with their nearest perfSONAR nodes, this module is used to start throughput tests from both end nodes(A, B) to each other nodes to find the long-clean path (B-D, RTT>20ms), and locate the source (C-D) of network issue .

### 3.Other Tool
    
##### 3.1 traceroute_recorder.py
 
 We collect all the traceroute test URLs from MAs and write the records into a file. Later, this file will be used to update our traceroute detail dataset as well as the traceroute graph.
 
##### 3.2 graphviz_example.py 
 
 It is used for visualizing the traceroute graph. It needs graphviz Python library.

### 4.Dataset (json format)

##### 4.1 ma_list

It is a dataset contains all the MAs' hostname.

##### 4.2 filtered_ma_list

It is a dataset after we filter the "bad" MAs in ma_list.

##### 4.3 ma_record

It is a dataset contains all the traceroute test URLs.

##### 4.4 dataset

It is a dataset contains the details of all the traceroute tests.

##### 4.5 dataset95 

It is a small dataset we queried from 95 chosen MA hosts in central and eastern regions of US. 


### 5.APIs

##### 5.1 from bwctl_tool import *

string    bwctl_test(string src_host, string dst_host): start a throughput test between two perfSONAR hosts using bwctl and return the result (bit/s).

list      trace_test(string src_host, string dst_host): start a traceroute test between two perfSONAR hosts using bwtraceroute and return the result.

##### 5.2 from find_ps_node import *

list      find_pr_path(list trace,int RNG,int TOL): find nearest ps nodes for target routers in trace. RNG represents the distance between the router and the perfSONAR node in the graph. TOL represents the subnet range we use to find the router in the graph.

##### 5.3 from issue_locator import *

void      locator(list trace, list ps_trace, string tp_value): locate the problematic source(s). trace represents the original traceroute. ps_trace represents the traceroute after we replace the routers' IP with perfSONARs' IP.

##### 5.4 from build_graph import *
dict      build_graph(dict graph, list trace_path): update the 'graph' by inserting the 'trapce_path' into the 'graph', i.e. inserting the nodes and edges into the graph. 'graph' represents the current graph. 'trace_path' represents the tracepath between two hosts.

dict      build_graph_from_file(string file_name): build a graph from a file which consists of all the tracepaths. The 'file_name' represents the file that contains the tracepaths dataset. The file must be in the format of [tracepath_1, tracepath_2, tracepath_3, ......, tracepath_n]. Each 'tracepath_i' is in the format of ['ip_1', 'ip_2', 'ip_3', ......, 'ip_m'].

##### 5.5 from query_diy import *
list      get_service_locator(string qstr): return all the hostnames that provide some certain services. 'qstr' is the query string, currently this function supports qstr = "service-type=bwctl", "service-type=mp-bwctl", "service-type=owamp", "service-type=mp-owamp", "service-type=ping", "service-type=traceroute", "service-type=ndt", "service-type=npad", and "service-type=ma".










