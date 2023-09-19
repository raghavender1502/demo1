import requests
from dotenv import load_dotenv
import os
import socket
import ast
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
apikey_ipinfo = os.getenv("ipinfoTokenRMX")
limit_viewdns = os.getenv("Limit_Viewdns")
apikey_viewdns = os.getenv("ViewdnsAPI")
limit_viewdns = ast.literal_eval(limit_viewdns)

def GetMailServers(domain):
    load_dotenv()
    apikey = os.getenv("HackerTargetAPIKEY")
    try:
        mx_list = []
        if len(apikey) == 0:
            
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}".format(domain))
            
        else:
            
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}&apikey={}".format(domain,apikey))
        p = r.text
        #print(p)
        # print("**************************************************************")
        spli = p.split("\n")
        try:
            MX = [s for s in spli if s.startswith("MX :")]
            MX = [j[5:] for j in MX]
        except:
            pass
        for mx in MX:
            mx_split = mx.split()
            mx_preference = mx_split[1][:-1]
            mx_list.append(mx_preference)

        return mx_list    
    except:
        return {}    

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

def GetGeoLocation(ip):

    try:
        geo_location ={}
        r = requests.get("https://ipinfo.io/"+ip+"?token="+apikey_ipinfo)    # 50,000 requests/month
        r = r.json()
        geo_location["city"] = r["city"]
        geo_location["country"]= r["country"]
        geo_location["location"]=r["loc"]
        geo_location["postalcode"]= r["postal"]
        geo_location["region"]=r["region"]
        geo_location["timezone"]=r["timezone"]
    except:
        pass  
    return geo_location         

def CallReverseMxAPI(MX):
    filtered_data=[]
    my_dict = []
    otherdomainsIPs=[]

    try:
        url = "https://reverse-mx.whoisxmlapi.com/api/v1?apiKey="+APIKey+"&mx="+MX
        #print(url)
        resp=requests.get(url)
        #print(resp)
        
        external_source = "WhoisXML API"
        if resp.status_code != 200:
            
            url = "https://api.viewdns.info/reversemx/?mx="+MX+"&apikey="+apikey_viewdns+"&output=json"
            resp=requests.get(url)
            external_source = "ViewDNS API"
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

                geoinfo = GetGeoLocation(domain_ip)
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
                my_dict.append(payload)
            except Exception as e:
                print(e)
        return my_dict,external_source
    except Exception as e:
        print(e)
        filtered_data=[]
    return filtered_data , external_source

def ReverseMx(domain):
    data_dict={}
    data_list=[]
    try:
        Mx_list = GetMailServers(domain)
        if len(Mx_list)==0:
            
            
           
            Mx_list2=[]
            mx_dns = dns.resolver.query(domain, 'MX')
                
            for rdata in mx_dns:
                Mx_list2.append(rdata.to_text())

            for i in Mx_list2:
                Mx_list.append(i.split()[1][:-1])   
    
            

        
    except:
        Mx_list=[]

    # MxList = GetMailServers(domain)
    # print(MxList)

    for MX in Mx_list:
        temp_dict={}
        filtered_data,external_source=CallReverseMxAPI(MX)
        temp_dict={"MX":MX,"OtherDomains":filtered_data}
        data_list.append(temp_dict)
    data_dict={"Domain":domain,"TestResult":data_list, "extSource":external_source}
    return data_dict







