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

#### 4.3 ma_record_[timestamp]

It is a dataset contains all the traceroute tests uris.

##### 4.4 dataset

It is a dataset contains the details of all the traceroute tests.

##### 4.5 dataset95 

It is a small dataset we queried from 95 chosen MA hosts in central and eastern regions of US. 













