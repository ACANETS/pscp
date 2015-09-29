import os
import json
import requests
import sys
from query_diy import get_service_locator

ma  = get_service_locator("service-type=ma")
print ma

tracepath_ps = [] #index for all nodes

counter = 0
for name in ma:  #each perfsonar node
	try:
		data = requests.get(name +"?format=json")
	except requests.exceptions.ConnectionError as e:
		print e
		continue

	if data is None:
		continue
	else:
		try:
			data0 = data.json()
		except:
			continue

	if len(data0) == 0:
		continue

	for k in data0:	#each traceroute test in ps node
		try:
			test = k['tool-name'][0:15]
		except: 
			continue
		if k['tool-name'][0:15] == 'bwctl/tracepath':
			try:
				trace_ps0 = requests.get('http://' + k['input-source'] + k['uri'] + 'packet-trace/base?format=json')
			except requests.exceptions.ConnectionError as e:
				print e
				continue

			if trace_ps0 is None:
				continue
			else:
				try:
					trace_ps = trace_ps0.json()
				except:
					continue

			if len(trace_ps) == 0:
				continue
			else: 	
				try:
					test = trace_ps[0]['val']
				except:
					continue
                                print trace_ps[0]
				ip_addr = []    #traceroute ip addr
				for i in trace_ps[0]['val']:
					ip_addr.append(i['ip'])
				ip_addr.insert(0,name[7:len(name)-25])
				ip_addr = sorted(set(ip_addr),key=ip_addr.index)
				print "################################################"
				print ip_addr
				print "################################################"
				tracepath_ps.append(ip_addr)
				print tracepath_ps
				print "################################################"

	counter = counter + 1
	if (counter%50) == 0:
		f = open('/home/chen/Documents/code/data'+ str(counter) ,'w+')
		json.dump(tracepath_ps,f)
		f.close()
