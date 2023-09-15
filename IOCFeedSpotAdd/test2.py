import os
import json
import requests
from pathlib import Path

feedspotKey = "5xX15I8b6OoZ4uRH180cy+EZ+blnSuobGxLlSdbIF8ncD8u2lEsb/i3o6hbZyRPG4hL65JNM6ulL5OoaBfZL/OAV9uKTHunrG+YTStjIG8zcD8uwYxrp6h7e3ksJ+BbS40P45JRP6u4d5+YZ3fcX/BRFxrdnH+TpSxIS"

Headers = {
    "Authorization": feedspotKey,
    "Content-Type": "application/json; charset=utf-8"
}

def dataFolderID(folder_id):
    response = requests.get(f"https://api.feedspot.com/v1/folders/{folder_id}.json", headers=Headers).json()
    try:
        payload = {
            "folder_id": folder_id,
            "response": response
        }
        return payload
    except:
        payload = {
            "folder_id": "",
            "response": ""
        }
        return payload

folder_id = "5758880"
folder_data = dataFolderID(folder_id)

if "response" in folder_data and "feed_url" in folder_data["response"]:
    feed_url = folder_data["response"]["feed_url"]

    ioc_parser_url = "https://api.iocparser.com/url"
    ioc_parser_payload = {"url": feed_url}
    ioc_parser_headers = {'Content-Type': 'application/json'}

    ioc_parser_response = requests.post(ioc_parser_url, headers=ioc_parser_headers, json=ioc_parser_payload).json()
    
    folder_data["response"]["ioc_parser_response"] = ioc_parser_response

print(json.dumps(folder_data, indent=4))
