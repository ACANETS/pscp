#PerfSONAR Control Plane (pscp)

Our control plane is used to start a test between two perfSONAR hosts, monitor the throughput performance and locate the source of network issues when problem happens.

1. control_plane.py is the code for online measurement test controls.

   To start the control plane, use "python control_plane.py [source_host_name] [destination_host_name]".

1.1. find_ps_node.py is one module of our control plane.

     After obtaining the traceroute of a problematic path, 
     this module is used to find the nearest perfSONAR node 
     for each target router on the path by looking up the graph 
     we built offline.

     graph_example.py is a small example of this module.

1.2. issue_locator.py is another module of our control plane.

                A-----C--X--D-----E-----F-----I-----H-----G-----B

     After replacing the routers with their nearest perfSONAR nodes, 
     this module is used to start throughput tests from both end nodes(A, B) 
     to each other nodes to find the long-clean path (B-D, RTT>20ms), 
     and locate the source (C-D) of network issue .

2. build_graph.py is the code for offline Measurement Archive (MA) data processing.

2.1. query_diy.py 
    
     This module is used to return a list of MA hosts from perfSONAR lookup service directory.

2.2. traceroute_collector.py

     This module can build a traceroute dataset by retrieving the traceroute tests records 
     in hosts' MAs by using perfSONAR client REST interface.

     dataset95 is a small dataset we built from 95 chosen MA hosts in central and eastern regions of US.

graphviz_example.py is used for visualizing the traceroute graph. It needs corresponding Python library.


    

   
                        
