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


import requests
import sys

###############################################################################
_LS_HINTS = "http://ps-west.es.net:8096/lookup/activehosts.json"
###############################################################################

def get_hosts():
    hosts = requests.get(_LS_HINTS).json().get("hosts", [])
    hosts = sorted(hosts, key=lambda v: v.get("priority", ""), reverse=True)
    for host in hosts:
        if host.get("locator", "") == "http://nsw-brwy-sls1.aarnet.net.au:8090/lookup/records/" or host.get("status", "") != "alive" or not host.get("locator", ""):
            hosts.remove(host)
    return hosts

###############################################################################    

def query(query_string, hosts):
	entry_count = 0
	records = []
	urls = [(host["locator"] + "?" + query_string) for host in hosts]
	for url in urls:
		response = requests.get(url)
		if response is None:
			continue
        	
		ls_host = response.url.split("lookup/records")[0]
		for record in response.json():
			entry_count = entry_count + 1
			if record.get("uri", "") and record.get("type", [ False ])[0]:
				record["ls-host"] = ls_host
				records.append(record)
	return records, entry_count
    
###############################################################################

def modify_str(in_str, qstr):
	ip_flag = 1
	http_flag = 1
	out_str=""
	if qstr == "service-type=bwctl":
		out_str = in_str[6:len(in_str)-5]
			
	elif qstr == "service-type=mp-bwctl":
		if str(in_str[0:5]) == 'https':
			out_str = in_str[8:len(in_str)-18]
			http_flag = 0
		elif in_str[0:5] == "http:":
			out_str = in_str[7:len(in_str)-18]
			
	elif qstr == "service-type=owamp":
		out_str = in_str[6:len(in_str)-4]
	
	elif qstr == "service-type=mp-owamp":
		if str(in_str[0:5]) == 'https':
			out_str = in_str[8:len(in_str)-18]
			http_flag = 0
		elif in_str[0:5] == "http:":
			out_str = in_str[7:len(in_str)-18]
			
	elif qstr == "service-type=ping":
		out_str = in_str
	
	elif qstr == "service-type=traceroute":
		out_str = in_str
	
	elif qstr == "service-type=ndt":
		out_str = in_str[7:len(in_str)-5]
	
	elif qstr == "service-type=npad":
		out_str = in_str[7:len(in_str)-5]

	elif qstr == "service-type=ma":
		out_str = in_str

	if qstr != "service-type=ma":
		if out_str[0] == '[' or "ipv6" in out_str or ":" in out_str:
			ip_flag = 0	
	return out_str, ip_flag, http_flag

###############################################################################
#This function is used for obtaining all the active hostnames that provide the correspondng service 
def get_service_locator(qstr):
	_ls_hosts = get_hosts()
	records_all, entry_num = query(qstr,_ls_hosts)
	service_locator = []
	for record in records_all:
		for temp_in_str in record.get("service-locator"):
			temp_out_str, ip_flag, http_flag = modify_str(temp_in_str, qstr)
			if ip_flag == 0 or http_flag==0:
				continue
			else:
				service_locator.append(temp_out_str)
				if qstr == "service-type=mp-bwctl" or qstr == "service-type=mp-owamp" or qstr == "service-type=ma":
					break
	return service_locator

#################################################################################
"""
def locator_main(sys_argv):
    qstr = "service-type=" + sys_argv
    service_locator = get_service_locator(qstr,_ls_hosts)
    sorted(service_locator)
    print "There are totally " + str(len(service_locator)) + " " + qstr + " locators, and they are: \n"
    print service_locator
"""




