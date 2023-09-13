import json
import requests
import os
import re
# from dotenv import load_dotenv
#get the keys
load_dotenv()
geekflareKey = "c02ba9ce-506f-438e-90a8-dd299515e28b"
def siteUptime(domain):
    url = "https://api.geekflare.com/up"
    payload = {}
    try:

        payload = json.dumps({
        "url": domain,
        "followRedirect": True,
        "proxyCountry": "us"
        })
        headers = {
        'x-api-key': geekflareKey,
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        payload = {
            "domain": domain,
            "response": response.json(),
            "extSource": "Geekflare API"
        }
    except:
        payload = {
            "domain": domain,
            "response": "",
            "extSource": "Geekflare API"
        }    
    return payload

print(siteUptime("tamu.edu"))
