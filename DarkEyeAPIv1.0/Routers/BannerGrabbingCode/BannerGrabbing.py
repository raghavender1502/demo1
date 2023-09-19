import requests
import socket
from re import search
import ast
from dotenv import load_dotenv
import os
from .nmaptable import nmaptable


nmaplist = nmaptable()
#print(nmaplist)

def banner_grabbing(domain):

    ip=socket.gethostbyname(domain)
    try:
        load_dotenv()
        apikey = os.getenv("HackerTargetAPIKEY")
            
        if len(apikey) == 0:
        
            res = requests.get("https://api.hackertarget.com/bannerlookup/?q={}".format(ip))
            
        else:
            
            res = requests.get("https://api.hackertarget.com/bannerlookup/?q={}&apikey={}".format(ip,apikey))

        #print(res.text)
        result = ast.literal_eval(res.text)
        #print(result)
        #print(type(result))
        response=[]
        for k,v in result.items():
            if k=="ip":
                continue #skip ip key value pair

            else:

                try:
                    string = ''.join((element for element in k if not element.isdigit()))
                    name=string
                except:
                    name=""
                try:
                    #title=k
                    title=v["title"]
                except:
                    title=""
                try:
                    service=k[0:5]
                except:
                    service=""
                try:
                    server=v["server"]
                except:
                    server=""
                try:
                        key = [a for a,b in nmaplist.items() if b==name]
                        port=key[0]
                except:
                    port=""
                try:
                    apps=v["apps"]
                except:
                    apps=[]
                try:
                    version=v["version"]
                except:
                    version=""
                extra_info=""

                payload={
                    "name":name,
                    "title":title,
                    "service":service,
                    "server":server,
                    "port":port,
                    "apps":apps,
                    "version":version,
                    "extra_info":extra_info

                }
                response.append(payload)


        final_payload={
            "domain":domain,
            "extSource": "HackerTarget API",
            "ip":ip,
            "response":response
            }


        #print(final_payload)
        return final_payload



    except:
        final_payload={
            "domain":domain,
            "extSource": "HackerTarget API",
            "ip":ip,
            "response":[{
                    "name":"",
                    "title":"",
                    "service":"",
                    "server":"",
                    "port":"",
                    "apps":[],
                    "version":"",
                    "extra_info":""
                }]
            }

        #print(final_payload)
        return final_payload    
#bannger_grabbing('DOMAIN_NAME')