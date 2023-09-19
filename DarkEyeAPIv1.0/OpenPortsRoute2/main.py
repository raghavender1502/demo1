from getports_services import ops
from protocol import protocol_dict
from nmaptable import nmaptable
from MainInfraStructureServices import dnslookup
import requests
from netaddr import *
from ipwhois import IPWhois
from dotenv import load_dotenv  
import os
import time
import ipaddress
import numpy as np
from datetime import datetime
import sys
import pymongo
import time
from ipwhois import IPWhois
from shodan import Shodan


nmaplist = nmaptable()
load_dotenv()
shodanKey = os.getenv("ENV2_SHODAN_API")
shodanApi = Shodan(shodanKey)
apikey_ipinfo = os.getenv("ENV2_ipinfoToken")
workerProcess = os.getenv("ENV2_CountOfWorkerProcess")
MongoDBURL = os.getenv("ENV2_MongoDBURL")
MongoDBName = os.getenv("ENV2_MongoDBOpenPorts")
CollectionName = os.getenv("ENV2_OpenPortsCollection")
articleURL = os.getenv("ENV2_ARTICLEURL")
myclient = pymongo.MongoClient(MongoDBURL)
mydb = myclient[MongoDBName]
collection = mydb[CollectionName]


def get_geolocation(ip):
    try:
        geolocation ={}
        r = requests.get("https://ipinfo.io/"+ip+"?token="+apikey_ipinfo)    # 50,000 requests/month
        r = r.json()
        geolocation["city"] = r["city"]
        geolocation["country"]= r["country"]
        geolocation["location"]=r["loc"]
        geolocation["postalcode"]= r["postal"]
        geolocation["region"]=r["region"]
        geolocation["timezone"]=r["timezone"]
    except:
        pass  
    return geolocation 


def process(IPList, ip_domain_List, scan_id, domain):
    final_ops_list = []
    foo_443 = 0
    foo_vulnlist = 0 
    vulnerable_ports =   [7, 19, 20, 21, 22, 23, 25, 37, 53, 69, 79, 80,
                                110, 111, 135, 137, 138, 139, 445, 161, 512,
                                513, 514, 1433, 1434, 1723, 3389, 8080, 3306, 
                                3050, 5432, 3351, 1583, 7210, 1521, 1830, 8529, 
                                7000, 7001, 9042, 5984, 9200, 9300, 27017, 27018, 
                                27019, 28017, 7473, 7474, 6379, 8087, 8098, 28015, 
                                29015, 7574, 8983 ]
    count = 0
    moreInfo = []
    for ip in IPList:
        try:
            count += 1
            finddoc_for_count = collection.find_one({"domain": domain, "scan.id": scan_id, "statusCode": 202})
            updatedoc_for_count = {"$set":{"response.progress": str(count)+" / "+str(len(IPList))}}
            collection.update_one(finddoc_for_count,updatedoc_for_count)
            res = shodanApi.host(ip)
            if len(res["data"])>0:
                time.sleep(2)
                #print("INFO: Ports Open on "+ip+" :" + str(res["ports"]))
                portsList = []
                for j in ip_domain_List:
                    if j["IP"] == ip:
                        ip_host = j["domain"]
                threatsPorts = []
                for items in res["data"]:
                    try:
                        port = items["port"]
                        threatsPorts.append(port)
                        if port == None:
                            port = ""
                    except:
                        port = ""

                    try:
                        service = items["_shodan"]["module"]
                        if service == None:
                            service = ""
                    except:
                        service = ""

                    try:
                        protocol = items["transport"]
                        if protocol == None:
                            protocol = ""
                    except:
                        protocol = ""

                    portsPayload = {
                        "port": port,
                        "service": service,
                        "protocol": protocol
                    }
                    portsList.append(portsPayload)

                threatsPorts = list(set(threatsPorts))
                moreInfo.append("Port(s) "+str(threatsPorts)[1:-1]+ " open on "+ip_host) 

                try:
                    network_name = res["isp"]
                    if network_name == None:
                        network_name = ""
                except:
                    network_name = ""

                try:
                    obj = IPWhois(ip)
                    ret = obj.lookup_whois()
                    ipAddressesRange = ret["nets"][0]["range"]
                except:
                    ipAddressesRange = ""


                try:
                    country = res["country_code"]
                    if country == None:
                        country = ""
                except:
                    country = ""

                try:
                    lastUpdateDate = res["last_update"].replace("T"," ")
                    if lastUpdateDate == None:
                        lastUpdateDate = ""
                except:
                    lastUpdateDate = ""

                try:
                    city = res["city"]
                    if city == None:
                        city = ""
                except:
                    city = ""

                try:
                    location = str(res["latitude"]) + ", " + str(res["longitude"])
                    if location == None:
                        location = ""
                except:
                    location = ""

                try:
                    postalcode = items["location"]["area_code"]
                    if postalcode == None:
                        postalcode = ""
                except:
                    postalcode = ""

                try:
                    region = items["location"]["region_code"]
                    if region == None:
                        region = ""
                except:
                    region = ""

                payload = {
                    "IPv4" : res["ip_str"],
                    "hostName": ip_host,
                    "openport" : portsList,
                    "subnet" : {
                        "network_name" : network_name,
                        "ipAddressesRange": ipAddressesRange,
                        "country" : country,
                        "lastUpdateDate" : lastUpdateDate,
                        },
                    "geo_ipinfo" : {
                        "city" : city,
                        "country" : country,
                        "location" : location,
                        "postalcode" : postalcode,
                        "region" : region,
                        "timezone": ""
                    }
                }
                openPorts = res["ports"]
                for op in openPorts:
                    if op == 443 or op == 8443:
                        foo_443 =+1
                    elif op in vulnerable_ports:
                        foo_vulnlist =+ 1 
                if foo_443 == 0 and foo_vulnlist == 0:
                    assetconfigcheck = {"testName":"Open Ports & Services","status":"Ok", "description": "No vulnerable port from the list of most vulnerable ports are found to be open", "moreInfo": moreInfo}
                elif foo_443 >0 and foo_vulnlist == 0:
                    assetconfigcheck = {"testName":"Open Ports & Services","status":"Ok", "description": "HTTPS port is open which might be the Product Infrastructure requirement.", "moreInfo": moreInfo}
                elif foo_443 >0 and foo_vulnlist >0:
                    assetconfigcheck = {"testName":"Open Ports & Services","status":"Warning", "description": "There are open ports on the target server from the list of most vulnerable ports that we maintain. Also there are HTTPS ports that are open might be the Product Infrastructure requirement. Refer to the Article: " + articleURL + " for details on Vulnerable Ports.", "moreInfo": moreInfo}
                elif foo_443 ==0 and foo_vulnlist >0:             
                    assetconfigcheck = {"testName":"Open Ports & Services","status":"Warning", "description": "There are open ports on the target server from the list of most vulnerable ports that we maintain. Refer to the Article: " + articleURL + " for details on Vulnerable Ports.", "moreInfo": moreInfo}
        
                finddoc = collection.find_one({"domain": domain, "scan.id": scan_id, "statusCode": 202})
                updatedoc = {"$push":{"response.response":payload},
                             "$set":{"response.threats":assetconfigcheck}}
                
                collection.update_one(finddoc,updatedoc)
                final_ops_list.append(payload)
        except Exception as e:
            time.sleep(1)
            #print(f"DEBUG: Skipped IP {ip}  Reason:",e)
            pass
    return final_ops_list


def splitter(ipList_final, NUM_WORKERS):
    list_list_ip = []
    splittedList = np.array_split(ipList_final,NUM_WORKERS)
    for i in splittedList:
        list_list_ip.append(list(i))
        
    return list_list_ip


def completeResponse(ips, ip_domain_List, scan_id, domain):
    final_payload = False
    process(ips,ip_domain_List, scan_id, domain)
    final_payload = True

    #print("INFO: Scan completed for domain:", domain)
    return final_payload


def get_ipList(domain):
    IPlist = []
    response = dnslookup(domain)

    for ip_sub in response["Sub domains"]:
        IPlist.append(ip_sub["IPv4"])
        
    for ip_a in response["A Records"]:
        
        IPlist.append(ip_a["IPv4"]) 
        
    for ip_mx in response["MX Records"]:
        IPlist.append(ip_mx["IPv4"])
        
    for ip_ns in response["NS Records"]:
        IPlist.append(ip_ns["IPv4"])  

    if [] in IPlist: 
        IPlist.remove([])
    iplist = list(np.unique(IPlist))
    if "" in iplist:
        iplist.remove("")  
    ipList_sorted = sorted(iplist, key = ipaddress.IPv4Address)
    ipList_final = []               # final sorted list of public ip 

    for z in ipList_sorted:
        if (IPAddress(z).is_private()):
            continue
        else:
            ipList_final.append(z)  
    ip_domain_List = []
    for ip_sub in response["Sub domains"]:
        sub_ip = ip_sub["IPv4"]
        sub_domain = ip_sub["Domain Name"]
        subrecord = {"IP" : sub_ip,
                    "domain": sub_domain}
        ip_domain_List.append(subrecord)

    for ip_a in response["A Records"]:
        a_ip = ip_a["IPv4"]
        a_domain = ip_a["Domain Name"]
        arecord = {"IP" : a_ip,
                    "domain": a_domain}
        ip_domain_List.append(arecord)

    for ip_mx in response["MX Records"]: 
        mx_ip = ip_mx["IPv4"]
        mx_domain = ip_mx["Domain Name"]
        mxrecord = {"IP" : mx_ip,
                    "domain": mx_domain}
        ip_domain_List.append(mxrecord)   

    for ip_ns in response["NS Records"]:
        ns_ip = ip_ns["IPv4"]
        ns_domain = ip_ns["Domain Name"]
        nsrecord = {"IP" : ns_ip,
                    "domain": ns_domain}
        ip_domain_List.append(nsrecord)     
    if {} in ip_domain_List:
        ip_domain_List.remove({})                    
    return ipList_final, ip_domain_List

##########################################################################################



def get_inprogress_doc(domain, scan_id, wait_time_secs=10, sleep_interval=1):
    """Waits 10s(by default) for the inprogress doc, given the domain and scan_id. \
        If couldn't find, just returns None."""
    for i in range(wait_time_secs):
        time.sleep(sleep_interval)
        inprogress_doc =  collection.find_one({
            "domain": domain, "scan.id": scan_id, "statusCode": 202})
        if inprogress_doc != None:
            return inprogress_doc

def update_inprogress_record(domain, scan_id):
    newdata = {
        "$set": {
            "status": "completed",
            "statusCode": 200,
            "statusMessage": "Thanks for being patient, the scan is completed.",
        }
    }
    inprogress_doc = get_inprogress_doc(domain, scan_id)

    if inprogress_doc == None:
        raise Exception(
            f"update_inprogress_record(): Waited for the inprogress doc, still couldn't \
                find the record in OPEN_PORTS with scan_id: {scan_id} and \
                domain: {domain}")

    collection.update_one(inprogress_doc, newdata)      

##########################################################################################
def port_finder(domain : str, scan_id):
    t1 = time.time()
    ipList_final ,ip_domain_List  = get_ipList(domain)
    execution = False
    data = completeResponse(ipList_final, ip_domain_List, scan_id,domain)  
    if data == True:
        finddoc = collection.find_one({"domain": domain, "scan.id": scan_id, "statusCode": 202})
        updatedoc = {
                "$set":{
                    "response.domain": domain,
                    "response.extSource":"Shodan API",
                    "response.executionTime":time.time() - t1,
                    "response.timestamp":str(datetime.now()) 
                }
            }
        collection.update_one(finddoc,updatedoc)
        execution = True     
    return execution

def main(domain, scan_id):
    res = port_finder(domain, scan_id)
    if res == True:
        update_inprogress_record(domain, scan_id)
    

if __name__ == '__main__':    
    domain, scan_id = sys.argv[1], int(sys.argv[2])
    main(domain, scan_id)
