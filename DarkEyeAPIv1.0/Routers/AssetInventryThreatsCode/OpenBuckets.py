from textwrap import indent
import tldextract
import os
import json
import requests

from pathlib import Path
from dotenv import load_dotenv

# GET API KEY
load_dotenv()

key = os.getenv("openbuckets_key")



def open_buckets(domain):
    buckets = []
    ext = tldextract.extract(domain)
    
    keywords = ext.domain

    par = {"access_token": key, "keywords": keywords}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    
    try:
        response = requests.get(
            "https://buckets.grayhatwarfare.com/api/v1/buckets/0/12", params=par, timeout=4, headers=headers)
        gwf_api = response.json()
        

        if gwf_api["buckets_count"] > 0:
            try:
                for bucket in gwf_api["buckets"]:
                    
                    Domain = str(domain)
                    try:
                        ID = bucket["id"]
                    except:
                        ID = "NA"
                    
                    try:
                        Bucket = bucket["bucket"]
                    except:
                        Bucket = "NA"
                    
                    try:
                        FileCount = bucket["fileCount"]
                    except:
                        FileCount = "NA"
                    

                    try:
                        Type = bucket["type"]
                    except:
                        Type = "NA"
                    

                    
                    buckets.append(bucket)
                    

            except:
                pass
            payload = {
                "Domain": domain,
                "Buckets_Count": gwf_api["buckets_count"],
                "Buckets": buckets
            }
            

            for bucket in buckets:
                if bucket["fileCount"] > 0:
                    result = {
                        "Status": "Warning", "Description": "Bucket contains some files which could be sensitive", "moreInfo":"Open cloud storages pose a threat and they may contain secrets like passwords, critical data, etc. which can be scanned through scripts and other tools."}
                    payload.update(result)

            return payload
        else:
            payload = {"Domain": domain,
                       "Buckets_Count": 0,
                       "Buckets": "No buckets found"}
            
            return payload
    except:
        payload = {"Domain": domain,
                       "Buckets_Count": 0,
                       "Buckets": "No buckets found"}
        return payload

