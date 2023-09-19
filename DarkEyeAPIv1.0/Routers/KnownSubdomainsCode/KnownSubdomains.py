from .Sublist3r import subDScanner

import requests
from dotenv import load_dotenv
import os




def KnownSubdomainsChecks(domain):
    try:
        try:
            load_dotenv()
            apikey = os.getenv("HackerTargetAPIKEY")
            
            if len(apikey) == 0:
            
                response = requests.get("https://api.hackertarget.com/hostsearch/?q={}".format(domain))
                
            else:
                
                response = requests.get("https://api.hackertarget.com/hostsearch/?q={}&apikey={}".format(domain,apikey))
          
            result = response.text
            res = result.split("\n")
            subdomain_list = []
            ip_list = []
            for subdo in res:
                if subdo == "":
                    continue
                s = subdo.split(",")[0]
                ip = subdo.split(",")[1]
                subdomain_list.append(s)
                ip_list.append(ip)
            
            payload =  {
                "Domain": domain,
                "SubDomains": subdomain_list,
                "IPV4s": ip_list,
                "extSource": "HackerTarget API"
            }  
            return payload
        
        
        except:
            data = subDScanner.getsubDomains(domain)
            data["extSource"] = "sublist3r"
            return data

    except:
        
        payload =  {
                "Domain": domain,
                "SubDomains": [],
                "IPV4s": [],
                "extSource": "sublist3r"
            } 
        
        return payload




