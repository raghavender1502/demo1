import re
import requests
import argparse
#from .ns_functions import get_IP, get_IPv4, get_IPv6, check_NS_response, check_IP_status, check_A_records, check_AAAA_records, check_TCP_connection
from .validation_functions import test_ns_records
import dns.resolver
from dotenv import load_dotenv
import os


############# function to get the NS records ################
def get_ns_from_dnsresolver(target):
    answers = dns.resolver.resolve(target,'NS')
    Ns=[]
    for server in answers:
        data=server.to_text()
        try:
            if data[-1]==".":
                data=data[:-1]
        except:
            data=data
        Ns.append(data)
    return Ns

def get_ns_records(target):
    load_dotenv()
    apikey = os.getenv("HackerTargetAPIKEY")
    if len(apikey) == 0:
            
        r = requests.get("https://api.hackertarget.com/dnslookup/?q={}".format(target))
            
    else:
            
        r = requests.get("https://api.hackertarget.com/dnslookup/?q={}&apikey={}".format(target,apikey))
    p = r.text
    spli = p.split("\n")
    try:
        NS = [s for s in spli if s.startswith("NS :")]
        NS = [j[5:].strip(".") for j in NS]
        if len(NS)==0:
            NS=get_ns_from_dnsresolver(target)
        return NS
    except:
        pass


def get_test_results(target):
    ns_data = {
        "domain": target,
        "detailedResponse": {
            "NS-records": [],
            "testResults": []
        }}

    ############### getting the ns records ##################
    ns_records = get_ns_records(target)
    
    
    for record in ns_records:
        
        data = {record: {}}



    ################# getting the results of the name servers ##################
    A_records, AAAA_records, NS_response, IP_status, TCP_connection = test_ns_records(
        ns_data["detailedResponse"]['NS-records'],ns_records)
    ns_data["detailedResponse"]["testResults"].append(A_records)
    ns_data["detailedResponse"]["testResults"].append(AAAA_records)
    ns_data["detailedResponse"]["testResults"].append(NS_response)
    ns_data["detailedResponse"]["testResults"].append(IP_status)
    ns_data["detailedResponse"]["testResults"].append(TCP_connection)

    
    ns_data_new={}
    ns_arry=[]
    ns_data_new['domain']=ns_data['domain']
    ns_data_new["detailedResponse"]={"testResults":ns_data["detailedResponse"]["testResults"]}
    try:
        for k in ns_data["detailedResponse"]['NS-records']:
            temp={}
            temp["NsRecordName"]=list(k.keys())[0]
            temp.update(list(k.values())[0])
            ns_arry.append(temp)
    except:
        ns_arry=[]
    ns_data_new["detailedResponse"]['NS-records']=ns_arry

    return ns_data_new

