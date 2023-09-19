import socket
import re
import json
import requests
import dns.resolver
import shodan
import os
from dotenv import load_dotenv
import socket
import time

def dnslookup( target):  
    load_dotenv()

    apikey = os.getenv("HackerTargetAPIKEY")

    try:    
        subdomain = "www"
        url =f"http://{subdomain}.{target}"
        hostIP = socket.gethostbyname(target)
        payload = [
                    {
                    "Domain Name": target,
                    "IPv4": hostIP,
                    "Kind": "web"
                    },
                    {
                    "Domain Name": url[7:],
                    "IPv4": hostIP,
                    "Kind": "www.web"
                    }] 

    except:
        payload = []
        
    
    try:
        arecordsarry=[]
        if len(apikey) == 0:
            req = requests.get(
                "https://api.hackertarget.com/hostsearch/?q="+str(target))
        else:
            req = requests.get(
                "https://api.hackertarget.com/hostsearch/?q="+str(target)+"&apikey="+apikey) 
        req = req.text	
        sp = re.split(',|\n',req)
        itr = iter(sp)
        res_dicts = dict(zip(itr,itr))
        for k in res_dicts:
            arecordsarry.append({"Domain Name":k,
                                 "IPv4":res_dicts[k],
                                 "Kind": "A"
                                 })
    except:
        arecordsarry = []
    mx_list = []
    mx_preference = "" 
    mx_ipv4 = ""
    mx_ipv6 = ""
    mx_ttl = ""
    
    try:
        MX=[]
        for x_mx in dns.resolver.resolve(target, 'MX'): 
            x_mx = x_mx.to_text()
            MX.append(x_mx)
        for mx in MX:
            try:
                mx_preference = mx[:2]
            except:
                mx_preference = ""    
            try:
                mx_ipv4 = socket.gethostbyname(mx[3:])
            except:
                mx_ipv4 = ""
            try:    
                mx_ipv6 = dns.resolver.resolve(mx[3:], "AAAA")
                mx_ipv6= str(mx_ipv6[0])
            except:
                mx_ipv6 = ""
            try:
                mx_ttl = dns.resolver.resolve(mx[3:]).rrset.ttl
            except:
                mx_ttl = ""
            mx_payload = {
                "Preference": mx_preference,
                "Domain Name": mx[3:],
                "IPv4": mx_ipv4,  
                "IPv6": mx_ipv6,
                "TTL": mx_ttl,
                "Kind":"MX" 
            }
            
            mx_list.append(mx_payload) 
    except:
        mx_list = []
    try:
        NS=[]
        for x_ns in dns.resolver.resolve(target, 'NS'): 
            x_ns = x_ns.to_text()
            NS.append(x_ns)
        ns_list =[]    
        for ns in NS:
            try:
                ns_ipv4 = socket.gethostbyname(ns)
            except:
                ns_ipv4 = ""
            try:                        
                ns_ipv6 = dns.resolver.resolve(ns, "AAAA")
                ns_ipv6= str(ns_ipv6[0])
            except:
                ns_ipv6 = ""
            try:    
                ns_ttl = dns.resolver.resolve(ns).rrset.ttl
            except:
                ns_ttl = ""
            ns_payload = {
                "Domain Name": ns,
                "IPv4": ns_ipv4,  
                "IPv6": ns_ipv6,
                "TTL": ns_ttl,
                "Kind": "NS"
            }
            ns_list.append(ns_payload)
    except:
        ns_list = []
    try:
        SOA=[]
        for x_soa in dns.resolver.resolve(target, 'SOA'): 
            x_soa = x_soa.to_text()
            SOA.append(x_soa)
        
        soa_payload = {
            "Primary name server": SOA[0].split()[0],
            "Hostmaster (e-mail)": SOA[0].split()[1],
            "Serial": SOA[0].split()[2],
            "Refresh": SOA[0].split()[3],
            "Retry": SOA[0].split()[4],
            "Expire": SOA[0].split()[5],
            "Minimum TTL": SOA[0].split()[6],              
        }

    except:
        soa_payload = {}    
    
    try:
        TXT=[]
        for x_txt in dns.resolver.resolve(target, 'TXT'): 
            x_txt = x_txt.to_text()
            TXT.append(x_txt)
    except:
        TXT=[]
    full_payload={
        "Domain": target,
        "Sub domains":payload, # 2 
        "A Records": arecordsarry, # 4 
        "MX Records": mx_list, #2
        "NS Records": ns_list, #2
        "SOA Records": soa_payload,
        "TXT Records": TXT,
    }

    return full_payload
        
