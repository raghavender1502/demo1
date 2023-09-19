import requests
from dotenv import load_dotenv
import os
import ast
import socket
#import pydnsbl
from ipwhois import IPWhois
import dns.resolver
#import logging
#from datetime import datetime
#current_datetime = datetime.now()
#str_current_datetime = str(current_datetime)
#filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
#logging.basicConfig(filename=filename1 + 'reversemxLogs.log', level=logging.DEBUG, 
#                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
#logger=logging.getLogger(__name__)

load_dotenv()
APIKey=os.getenv("WhoisAPI")
apikey_ipinfo = os.getenv("ipinfoTokenRNS")
limit_viewdns = os.getenv("Limit_Viewdns")
viewdns_apikey = os.getenv("ViewdnsAPI") 
limit_viewdns = ast.literal_eval(limit_viewdns)

def GetNameServerHackerTarget(domain):
    load_dotenv()
    apikey = os.getenv("HackerTargetAPIKEY")
    try:
        ns_list = []
        if len(apikey) == 0:
            
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}".format(domain))
            
        else:
            
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}&apikey={}".format(domain,apikey))
        p = r.text
        #print(p)
        # print("**************************************************************")
        spli = p.split("\n")
        try:
            NS = [s for s in spli if s.startswith("NS :")]
            NS = [j[5:-1] for j in NS]
        except:
            print("Unable to get Name Server records from HackerTarget")
            pass


        return NS    
    except:
        return []    

# def Base_Domain_Provider_Check(domain_name):
#     """
#     Takes the domain name and returns the blacklisted or not and detected by list by using 
#     the pydnsbl package. 
#     Parameters:
#         domain_name: The domain name to check blacklisted or not.
#     Returns:
#         dbl_val: Status of that domain name (blacklisted or not).
#         dbl_det: List of the domain providers where this domain name is blacklisted.
#     """
#     dbl_val=False
#     dbl_det=[]
#     try:
#         domain_checker=pydnsbl.DNSBLDomainChecker()
#         result = domain_checker.check(domain_name)
#         dbl_val = result.blacklisted

#         #Creating the list domain providers who detected that given domain is blacklisted. 
#         dbl_det = list(result.detected_by.keys())
#     except Exception as err:
#         #logger.error(err)

#         print(err)
#     return dbl_val, dbl_det

def getGeolocation(ip):

    try:
        geolocation ={}
        r = requests.get("https://ipinfo.io/"+ip+"?token="+apikey_ipinfo)    # 50,000 requests/month
        r = r.json()
        #print(r)
        geolocation["city"] = r["city"]
        geolocation["country"]= r["country"]
        geolocation["location"]=r["loc"]
        geolocation["postalcode"]= r["postal"]
        geolocation["region"]=r["region"]
        geolocation["timezone"]=r["timezone"]
    except:
        pass  
    return geolocation         

def CallReverseNSAPI(NS):
    filtered_data=[]
    mydict = []
    other_domains_ips=[]
    try:
        url = "https://reverse-ns.whoisxmlapi.com/api/v1?apiKey="+APIKey+"&ns="+NS
        #print(url)
        resp=requests.get(url)
        #print(resp)
        external_source = "WhoisXML API"
        if resp.status_code != 200:
            
            url = "https://api.viewdns.info/reversens/?ns="+NS+"&apikey="+viewdns_apikey+"&output=json"
            resp=requests.get(url)
            external_source = "WhoisXML API"
            data = resp.json()['response']['domains'][:limit_viewdns]

            
        else:               
            

            data = resp.json()['result']
            domain_list = []
            for i in data:
                domain_list.append(i['name'])
            data = domain_list        
        for i in data:
            try:
                    
                other_domain = i



                        
                domain_ip = socket.gethostbyname(other_domain)
#                 blacklistCheck, blacklistList = Base_Domain_Provider_Check(otherDomain)
#                 if blacklistCheck == True:
#                     blacklisted = "Warning"
#                     bl_description = otherDomain + " resolving to the Mail Server " + MX + " has been blacklisted by " + str(blacklistList)[1:-1]
#                 else:
#                     blacklisted = "Ok"
#                     bl_description = otherDomain + " not found in Blacklist."

                geoinfo = getGeolocation(domain_ip)
                obj = IPWhois(domain_ip)
                ret = obj.lookup_whois()
                payload = {
                    "OtherDomain":other_domain,
                    "IPv4": domain_ip,
                    "geo_ipinfo":geoinfo,
                    "subnet_ipinfo":{
                        "network_name": ret["nets"][0]["name"],
                        "ipAddressesRange": ret["nets"][0]["range"],
                        "country": geoinfo["country"],
                        "lastUpdateDate": ret["nets"][0]["updated"]
                    },
                    #"blacklist_status" :blacklisted,
                    #"description": bl_description,
                }
                mydict.append(payload)
            except Exception as e:
                print(e)
        return mydict,external_source
    except Exception as e:
        print(e)
        filtered_data=[]
    return filtered_data,external_source

def ReverseNs(domain):
    data_dict={}
    data_list=[]
    try:
        ns_list = GetNameServerHackerTarget(domain)
        print("NS Records from HT: ",ns_list)
        if len(ns_list)==0:
            
            
           
            ns_list=[]
            ns_dns = dns.resolver.resolve(domain, 'NS')
                
            for rdata in ns_dns:
                ns_list.append(rdata.to_text())
            print("NS Records from DNS Resolver: ",ns_list)
  
    
            

        
    except Exception as e:
        print(e)
        ns_list=[]

    

    for NS in ns_list:
        temp_dict={}
        filtered_data,external_source=CallReverseNSAPI(NS)
        temp_dict={"Ns":NS,"OtherDomains":filtered_data}
        data_list.append(temp_dict)
    data_dict={"Domain":domain,"TestResult":data_list, "extSource":external_source}
    return data_dict



    
