###################################################
#Copyright © 2015 by ACANETS. All rights reserved.#
###################################################

from graph import *
from graphviz import *
from subprocess import call
import os
"""
#provide the name of the file which contains all the tracepaths
#build the graph upon the file
file_name = "new_dataset"
g = build_graph_from_file_IP(file_name)

#debug and print the graph
print g
print "\n\n\n"


#use graphvz to generate the pdf file
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
"""
#call(["sfdp", "-x", "-Goverlap=prism", "-Tpng", "traceroute.gv",  ">", "traceroute.png"])
#call(["sfdp -x -Goverlap=prism -Tpng traceroute.gv  > traceroute.png"])
os.system("sfdp -x -Goverlap=prism -Tpng traceroute.gv  > traceroute.png")
