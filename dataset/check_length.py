import json
import sys

file_name = sys.argv[1]
f = open(file_name,'r')
g = json.load(f)
print len(g)
f.close()
