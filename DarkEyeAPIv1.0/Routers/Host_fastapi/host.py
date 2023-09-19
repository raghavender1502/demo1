import requests
import json
import socket
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("Binaryedge_APIKEY")
# #head = {
#     "X-KEY" :  "7f27d1ee-6727-4f1b-af39-608c909bb85f"
# }
#API_KEY = "7f27d1ee-6727-4f1b-af39-608c909bb85f"
def get_Host(domain):
    """
    Details about an hostList of recent events for the specified host,
        including details of exposed ports and services.
        https://docs.binaryedge.io/api-v2/#host
        Args:
            ip: IP address (string)
        Returns:
            A dict created from the JSON returned by BinaryEdge
        Raises:
        BinaryEdgeException: if anything else than 200 is returned by BE
    """
    try:
        ip=socket.gethostbyname(domain)

        #response = requests.get("https://api.binaryedge.io/v2/query/ip/{}".format(ip),headers = head)
        response = requests.get("https://api.binaryedge.io/v2/query/ip/{}".format(ip),api_key)
        # res = response.json()
        # print(response.text)
        res1 = response.json()
        # parse x:
        # res1 = json.loads(res)
        # print(y)
        payload = {
            "domain" : domain,
            "IP" : ip,
            "results" : res1,
            "extSource":"Binaryedge API"
        } 
        # print(type(payload))
        # print(payload)
        return payload
    except Exception as e:
        print("Exception: Reason: ",e)
        payload = {
         "domain" : domain,
            "IP" : ip,
            "results" : ""
        } 
        # print(payload)
        return payload

# print(get_Host("tamu.edu"))


