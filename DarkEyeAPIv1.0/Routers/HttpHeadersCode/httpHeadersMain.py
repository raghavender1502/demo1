import json
import requests
import os
import re
from dotenv import load_dotenv

# get the keys
load_dotenv()
hackertargetKey = os.getenv("HackerTargetAPIKEY")
geekflareKey = os.getenv("geekflareAPIKEY")

def httpHeadersHackertarget(domain):
    if len(hackertargetKey) == 0:
        r = requests.get("https://api.hackertarget.com/httpheaders/?q={}".format(domain))
    else:
        r = requests.get("https://api.hackertarget.com/httpheaders/?q={}&apikey={}".format(domain,hackertargetKey))
    p = r.text
    spli = p.split("200 OK\n")
    sp = spli[1].split("\n")
    date = ""
    expires = ""
    cache_control = ""
    content_encoding = ""
    content_type = ""
    sts = ""
    permissions_policy = ""
    origin_trial = ""
    p3p = ""
    x_frame_options = ""
    x_xss_protection = ""
    transfer_encoding = ""
    set_cookie = ""
    server = ""
    alt_svc = ""

    for element in sp:
        if element.startswith('Date: '):
            date = element[6:]
        if element.startswith('Expires: '):
            expires = element[9:]
        if element.startswith('Cache-Control: '):
            cache_control = element[15:] 
        if element.startswith('Content-Type: '):
            content_type = element[14:]
        if element.startswith('Strict-Transport-Security: '):
            sts = element[27:]
        if element.startswith('Permissions-Policy: '):
            permissions_policy = element[20:]
        if element.startswith('Origin-Trial: '):
            origin_trial = element[14:]      
        if element.startswith('P3P: '):
            p3p = element[5: ]
        if element.startswith('Content-Encoding: '):
            content_encoding = element[18:]
        if element.startswith('Server: '):
            server = element[8:]
        if element.startswith('X-XSS-Protection: '):
            x_xss_protection = element[18:]
        if element.startswith('X-Frame-Options: '):
            x_frame_options = element[17:]
        if element.startswith('Set-Cookie: '):
            set_cookie = element[12:]      
        if element.startswith('Alt-Svc: '):
            alt_svc = element[9:]
        if element.startswith('Transfer-Encoding: '):
            transfer_encoding = element[18:]

        
    payload = {
            "Date": date,
            "Expires": expires,
            "Cache-Control": cache_control,
            "Content-Type": content_type,
            "Strict-Transport-Security": sts,
            "Permissions-Policy": permissions_policy,
            "Origin-Trial": origin_trial,
            "P3P": p3p,
            "Content-Encoding": content_encoding,
            "Server": server,
            "X-XSS-Protection": x_xss_protection,
            "X-Frame-Options": x_frame_options,
            "Set-Cookie": set_cookie,
            "Alt-Svc": alt_svc,
            "Transfer-Encoding": transfer_encoding
        }    

    final_payload = {
        "domain": domain,
        "response": payload,
        "extSource": "Hackertarget API"
    }    

    return final_payload


def httpheadersGeekflare(domain):
    

    #URL for the JSON field in the post request
    url = "https://"+str(domain)
    
    #headers in the post request.
    header={
        'x-api-key':geekflareKey,
        'Content-Type':'application/json'
    }

    json_field={
    "url":url,
    "proxyCountry":"us"

    }

    response=requests.post("https://api.geekflare.com/httpheader",headers=header,json=json_field)
    res = response.json()
    lis = res['data']
    #print(lis)
    try:
        for i in range(len(lis)):
            if res['data'][i]['name'] == "set-cookie":
                txt = res['data'][i]['value']
                x = re.findall("^SEOR=",txt)
                if x:
                    lis.pop(i)
                else:
                    pass   
            else:
                pass     
    except:
        pass                
    newlist = lis
    
    prev_value = ""
    transfer_encoding = ""
    date = ""
    expires = ""
    cache_control = ""
    content_type = ""
    sts= ""
    permissions_policy = ""
    origin_trial = ""
    p3p = ""
    server = ""
    x_xss_protection = ""
    set_cookie = ""
    alt_svc = ""
    content_encoding = ""
    x_frame_options = ""
    coopor = ""
    connection = ""
    report_to =""
    accept_ch = ""

    

    for element in newlist:

        if element["name"] == "date":
            date = element["value"]
        if element["name"] == "expires":
            expires = element["value"]
        if element["name"] == "cache-control":
            cache_control = element["value"]
        if element["name"] == "content-type":
            content_type = element["value"]
        if element["name"] == "strict-transport-security":
            sts = element["value"]
        if element["name"] == "permissions-policy":
            permissions_policy = element["value"]
        if element["name"] == "origin-trial":
            origin_trial = element["value"]
        if element["name"] == "p3p":
            p3p = element["value"]
        if element["name"] == "server":
            server = element["value"]
        if element["name"] == "x-xss-protection":
            x_xss_protection = element["value"]
        if element["name"] == "set-cookie":
            prev_value = set_cookie
            set_cookie = element["value"]
            if set_cookie != prev_value:
                prev_value = set_cookie
            
        if element["name"] == "alt-svc":
            alt_svc = element["value"]
        if element["name"] == "content-encoding":
            content_encoding = element["value"]
        if element["name"] == "x-frame-options":
            x_frame_options = element["value"]
        if element["name"] == "report-to":
            report_to = element["value"]
        if element["name"] == "accept-ch":
            accept_ch = element["value"]  
        if element["name"] == "cross-origin-opener-policy-report-only":
            coopor = element["value"]
        if element["name"] == "connection":
            connection = element["value"]                   


    payload = {
            "Date": date,
            "Expires": expires,
            "Cache-Control": cache_control,
            "Content-Type": content_type,
            "Strict-Transport-Security": sts,
            "Permissions-Policy": permissions_policy,
            "Origin-Trial": origin_trial,
            "P3P": p3p,
            "Content-Encoding": content_encoding,
            "Server": server,
            "X-XSS-Protection": x_xss_protection,
            "X-Frame-Options": x_frame_options,
            "Set-Cookie": set_cookie,
            "Alt-Svc": alt_svc,
            "Transfer-Encoding": transfer_encoding,
            "Cross-origin-opener-policy-report-only" : coopor,
            "Connection": connection,
            "report-to": report_to,
            "accept-ch": accept_ch
        }    

    final_payload = {
        "domain":domain,
        "response": payload,
        "extSource": "Geekflare API"
    }

    return final_payload


def function(domain):
    try:
        result = httpheadersGeekflare(domain)
        return result
    except Exception as e:
        print("\nWarning: Exception occured:",e)
        result = httpHeadersHackertarget(domain)
        return result    
