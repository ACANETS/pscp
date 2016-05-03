import json
import sys

file_name = sys.argv[1]

f = open(file_name,'r')
a = json.load(f)

g = open('datatotal','r')
b = json.load(g)

for i in a:
	if i not in b:
		b.append(i)

c = b
f.close()
g.close()
print len(c)
h = open('datatotal','w')
json.dump(c,h)
f.close()
