from urllib import response
import requests
import socket
import re
from dotenv import load_dotenv
import os

load_dotenv()
apikey = os.getenv("HackerTargetAPIKEY")

def getDomains(domain):
    
    domain_ip = socket.gethostbyname(domain)
    if len(apikey) == 0:
        data = requests.get(
            "https://api.hackertarget.com/reverseiplookup/?q="+str(domain_ip))
    else:
        data = requests.get(
            "https://api.hackertarget.com/reverseiplookup/?q="+str(domain_ip)+"&apikey="+apikey)      
    result = data.text

    sp = re.split(',|\n', result)
    
    if sp[0]=="API count exceeded - Increase Quota with Membership":
        payload = {
            "Domain": domain,
            "Response": [],
            "extSource": "HackerTarget API",
            "Relevant Domains": [],
            "Non-relevant Domains": []
        }
        
        return payload
    if sp[0]=="No DNS A records found":
        payload = {
            "Domain": domain,
            "Response": [],
            "extSource": "HackerTarget API",
            "Relevant Domains": [],
            "Non-relevant Domains": []
        }
        return payload

    else:
            
        pattern1 = f"^[a-zA-Z0-9\-]*\.*{domain}"
        pattern2 = f"^[a-zA-Z0-9\-]*\.[a-zA-Z0-9\-]*\.{domain}"
        relevant_domains = []
        non_relevant_domains = []
        temp_arr = domain.split(".")

        for d in sp:

           
            if (re.match(pattern1, d) or re.match(pattern2, d) or temp_arr[0] in d):
                
                relevant_domains.append(d)
            else:
                
                non_relevant_domains.append(d)

        payload = {
            "Domain": domain,
            "Response": sp,
            "extSource": "HackerTarget API",
            "Relevant Domains": relevant_domains,
            "Non-relevant Domains": non_relevant_domains
        }

        if len(non_relevant_domains) > 0:
            result = {
                "Status": "Warning",
                "Description": f"{len(non_relevant_domains)} Non-relevant Domains/Sub-domains found on the same IP",
                "moreInfo":non_relevant_domains
                }
            payload.update(result)


        return payload

