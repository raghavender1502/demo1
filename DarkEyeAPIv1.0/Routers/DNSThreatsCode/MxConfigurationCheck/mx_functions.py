import dns.resolver
import socket
import time
from netaddr import *
import validators
import requests
import subprocess
import json
import requests
from dotenv import load_dotenv
import os


def get_IPv4(target):
    try:
        target_IP = socket.gethostbyname(target)
        ips = socket.getaddrinfo(
            target, "http", family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )
        return ips[0][-1][0]
    except:
        
        return ""


def get_IPv6(target):
    try:
        target_IP = socket.gethostbyname(target)
        ips = socket.getaddrinfo(
            target, "http", family=socket.AF_INET6, proto=socket.IPPROTO_TCP
        )
        return ips[0][-1][0]
    except:
        
        return ""


################ getting NS records ################
def get_ns_records(target):
    ns_records = []

    try:
        ns_result = dns.resolver.resolve(target, 'NS')
        for val in ns_result:
            ns_records.append(val.to_text().strip("."))
    except:
        pass

    return ns_records


################ check A record ################
def check_A_records(target):
    response_data = {
        "Status": "",
        "Description": "",
    }
    # Finding A record
    try:
        result = list(dns.resolver.resolve(target, "A"))
        if len(result) != 0:
            response_data["Status"] = "Ok"
            response_data["Description"] = f"{target} have A record"
        else:
            response_data["Status"] = "Warning"
            response_data["Description"] = f"{target} have no A record"
    except:
        print("Failed to get the A records")
        response_data["Status"] = "Failed"
        response_data["Description"] = f"Failed to get the A records for {target}"

    return response_data


############### check AAAA record ################
def check_AAAA_records(target):
    response_data = {
        "Status": "",
        "Description": "",
    }
    # Finding AAAA record
    try:
        result = list(dns.resolver.query(target, "AAAA"))

        if len(result) != 0:
            response_data["Status"] = "Ok"
            response_data["Description"] = f"{target} have AAAA record"
        else:
            response_data["Status"] = "Warning"
            response_data["Description"] = f"{target} have no AAAA record"

    except:
        print("Failed to get the AAAA records")
        response_data["Status"] = "Failed"
        response_data["Description"] = f"Failed to get the AAAA records for {target}"

    return response_data


############### check CNAME record ################
def check_CNAME_records(target):
    response_data = {
        "Status": "",
        "Description": "",
    }
    # Finding CNAME record
    try:
        result = list(dns.resolver.resolve(target, "CNAME"))
        response_data["Status"] = "Ok"

    except:
        
        response_data["Status"] = "Failed"

    return response_data


############### check if IP public or not ################
def check_IP_status(target):
    response_data = {
        "Status": "",
        "Description": "",
    }
    try:
        result = IPAddress(socket.gethostbyname(target)).is_private()
        if result == False:
            response_data["Status"] = "Ok"
            response_data["Description"] = "IP is Public"
        else:
            response_data["Status"] = "Warning"
            response_data["Description"] = "IP is not Public"
    except:
        
        pass

    return response_data


############### check if it's a valid domain or not ################
def check_domain(target):
    response_data = {
        "Status": "",
        "Description": "",
    }

    try:
        result = validators.domain(target)
        if result == True:
            response_data["Status"] = "Ok"
            response_data["Description"] = "Domain is Valid"
        else:
            response_data["Status"] = "Failed"
            response_data["Description"] = "Domain is not Valid"
    except:
        
        pass

    return response_data


############### check if it's an IP or not ################
def check_IP(target):
    response_data = {
        "Status": "",
        "Description": "",
    }
    try:
        res = socket.inet_aton(target)
        response_data["Status"] = "Ok"
        response_data["Description"] = "It's an IP"

    except socket.error:
        response_data["Status"] = "Failed"
        response_data["Description"] = "It's not an IP"

    return response_data


############### check duplicate MX records ################
def check_duplicate_MX_records(mx_records):
    response_data = {
        "TestName":"No duplicate MX records",
        "Status": "",
        "Description": "",
        "moreInfo":[{"MX Records":i} for i in mx_records]
    }
    ipv4_arr = [get_IPv4(x) for x in mx_records if (get_IPv4(x) != "")]
    ipv6_arr = [get_IPv6(x) for x in mx_records if (get_IPv6(x) != "")]
    

    if(len(ipv4_arr) != 0):
        result = list(filter(lambda x: ipv4_arr.count(x) > 1,
                      ipv4_arr))
        
        if len(result) == 0:
            response_data["Status"] = "Ok"
            response_data["Description"] = "No duplicate records. It is recommended that MX records point to different IPs."
            response_data["moreInfo"] = [{"MX Records":i} for i in mx_records]
        else:
            response_data["Status"] = "Warning"
            response_data["Description"] = "Found Mail Servers resolving to the same IPv4 address. It is recommended that MX records point to different IPs."
            response_data["moreInfo"] = [{"MX Records":i} for i in mx_records]
            #    str(", ".join([socket.gethostbyaddr(address)[0]
            #        for address in result]))

    if(len(ipv6_arr) != 0):
        result = list(filter(lambda x: ipv6_arr.count(x) > 1,
                      ipv6_arr))
        
        if len(result) == 0:
            response_data["Status"] = "Ok"
            response_data["Description"] = "No duplicate records. It is recommended that MX records point to different IPs."
            response_data["moreInfo"] = [{"MX Records":i} for i in mx_records]
        else:
            response_data["Status"] = "Warning"
            response_data["Description"] = "Found Mail Servers resolving to the same IPv4 address. It is recommended that MX records point to different IPs."
            response_data["moreInfo"] = [{"MX Records":i} for i in mx_records]
            #    str(", ".join([socket.gethostbyaddr(address)[0]
            #        for address in result]))

    return response_data


############### get SPF records ################
def get_spf_records(target):
    load_dotenv()
    apikey = os.getenv("HackerTargetAPIKEY")
    response_data = {
        "TestName": "SPF",
        "Status": "Failed",
        "record": "",
        "Description": "Couldn't get SPF record. Email spam and phishing often use forged 'from' addresses, so publishing and checking SPF records can be considered anti-spam techniques. Please refer to RFC 7208 : https://datatracker.ietf.org/doc/html/rfc7208 for additional information.",
        "moreInfo":[{"SPF Record": "SPF record not found."}]
    }
    
    try:
        if len(apikey) == 0:
        
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}".format(target))
        
        else:
        
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}&apikey={}".format(target,apikey))
        
        p = r.text
        spli = p.split("\n")
        TXT = [s for s in spli if s.startswith("TXT :")]
        TXT = [j[6:].strip("\"") for j in TXT]
        #print(TXT)
        for txt in TXT:
            if "spf" in txt:
                response_data["Status"] = "Ok"
                response_data["record"] = txt
                response_data["Description"] = "SPF is configured. Email spam and phishing often use forged 'from' addresses, so publishing and checking SPF records can be considered anti-spam techniques. Please refer to RFC 7208 : https://datatracker.ietf.org/doc/html/rfc7208 for additional information."
                response_data["moreInfo"] = [{"SPF Record": txt}]
                return response_data 
    except:
        pass   
         
    if response_data["Status"] == "Failed":
        try:
            result = dns.resolver.resolve(target, 'TXT')
            print(result)
            txt_list = []
            for val in result:
                txt_list.append(str(val))
            txt_new_list = []     
            for i in txt_list:
                txt_new_list.append(i[1:-1])    
            a = 0
            for y in txt_new_list:
                if "spf" in y:
                    rec = y
                    a=+1
                else:
                    a = a
            if a>0:
                response_data["Status"] = "Ok"
                response_data["record"] = rec
                response_data["Description"] = "SPF is configured. Email spam and phishing often use forged 'from' addresses, so publishing and checking SPF records can be considered anti-spam techniques. Please refer to RFC 7208 : https://datatracker.ietf.org/doc/html/rfc7208 for additional information."
                response_data["moreInfo"] = [{"SPF Record": txt}]
                return response_data
            
        except:
            pass
    
    return response_data

############### get DMARC records ################
def get_dmarc_records(target):
    response_data = {
        "domain":target,
        "TestName":"DMARC",
        "Status": "Failed",
        "record": "",
        "Description": "Couldn't get DMARC record. DMARC configuration helps in mitigating risks involved in Email spoofing.",
        "moreInfo": [{"DMARC Record": "DMARC is not configured for "+str(target)+"; Configuration of DMARC helps in avoiding Email spoofing."}]
    }
    try:
        dmarc_response_1 = subprocess.Popen(["checkdmarc", target], stdout=subprocess.PIPE).stdout.read()
        #print(dmarc_response_1)
        result_1 = dmarc_response_1.decode("utf-8")
        dmarc_response = json.loads(result_1)
        #print(dmarc_response)
        rec = ""
        #print("\n******************\n")
        if dmarc_response["dmarc"]["valid"] == True:
            rec = dmarc_response["dmarc"]["record"]
            response_data = {
            "domain":target,
            "TestName":"DMARC",
            "Status": "Ok",
            "record": rec,
            "Description": "DMARC is configured. DMARC configuration helps in mitigating risks involved in Email spoofing.",
            "moreInfo": [{"DMARC Record": rec}]
            }
            #print(response_data)
        else:
            response_data = {
            "domain":target,
            "TestName":"DMARC",
            "Status": "Warning",
            "record": rec,
            "Description": "DMARC is not configured.",
            "moreInfo": [{"DMARC Record": "DMARC is not configured for "+str(target)+"; Configuration of DMARC helps in avoiding Email spoofing."}]
            }
            #print(response_data)
    except Exception as e:
        print("EXCEPTION: Not valid",e)
        response_data = {
            "domain":target,
            "TestName":"DMARC",
            "Status": "Failed",
            "record": "",
            "Description": "Couldn't get DMARC record.",
            "moreInfo": [{"DMARC Record": "DMARC is not configured for "+str(target)+"; Configuration of DMARC helps in avoiding Email spoofing."}]
        }
    if response_data["Status"] == "Ok":
        return response_data
    if response_data["Status"] == "Failed":
        cmd = ["nslookup", "-type=txt", f"_dmarc.{target}"]
        try:

            dmarc_response_2 = subprocess.Popen(
                cmd, stdout=subprocess.PIPE).stdout.read()
            result_2 = dmarc_response_2.decode("utf-8")
            res_2 = result_2.split("\r\n\r\n")[2].strip("\t\n\r\"")
            if (res_2):

                response_data["Status"] = "Ok"
                response_data["record"] = res_2
                response_data["Description"] = "DMARC is configured. DMARC configuration helps in mitigating risks involved in Email spoofing."
                response_data["moreInfo"] = [{"DMARC Record": res_2}]
        except:

            pass
    return response_data


############### checking if all name servers have identical SPF and DMARC records ################
def check_identical_spf_and_dmarc(target):
    time.sleep(1)
    ns = get_ns_records(target) 
    time.sleep(1)
    spf = get_spf_records(target)
    time.sleep(1)
    dmarc = get_dmarc_records(target)
    spf = spf["record"]
    dmarc = dmarc["record"]

    response_data = {"TestName":"Identical SPF and DMARC records", "Status": "", "Description": ""}

    if (len(ns) != 0):
        if (spf == "") and (dmarc == ""):
            response_data['Description'] = "Unable to find SPF and DMARC records. The SPF and DMARC TXT records should be identical. Please refer to RFC 7489 : https://datatracker.ietf.org/doc/html/rfc7489 for additional information."
            response_data['Status'] = "Failed"
            response_data['moreInfo'] = [{"SPF Record": "", "DMARC Record": ""}]
            return response_data     

        if (spf == "") and (dmarc != ""):
            response_data['Description'] = "Unable to find SPF record. The SPF and DMARC TXT records should be identical. Please refer to RFC 7489 : https://datatracker.ietf.org/doc/html/rfc7489 for additional information."
            response_data['Status'] = "Failed"
            response_data['moreInfo'] = [{"SPF Record": "", "DMARC Record": dmarc}]
            return response_data 

        if (spf != "") and (dmarc == ""):
            response_data['Description'] = "Unable to find DMARC record. The SPF and DMARC TXT records should be identical. Please refer to RFC 7489 : https://datatracker.ietf.org/doc/html/rfc7489 for additional information."
            response_data['Status'] = "Failed"
            response_data['moreInfo'] = [{"SPF Record": spf, "DMARC Record": ""}]
            return response_data    

        if (spf != "") and (dmarc != ""):
            if spf == dmarc:
                response_data['Description'] = "SPF record and DMARC record are identical on all the Name Servers. The SPF and DMARC TXT records should be identical. Please refer to RFC 7489 : https://datatracker.ietf.org/doc/html/rfc7489 for additional information."
                response_data['Status'] = "Ok"
                response_data['moreInfo'] = [{"SPF Record": spf, "DMARC Record": dmarc}]
                return response_data  
            else:
                response_data['Description'] = "SPF record and DMARC record are NOT identical on all the Name Servers. The SPF and DMARC TXT records should be identical. Please refer to RFC 7489 : https://datatracker.ietf.org/doc/html/rfc7489 for additional information."
                response_data['Status'] = "Warning"
                response_data['moreInfo'] = [{"SPF Record": spf, "DMARC Record": dmarc}]
                return response_data 
    else:
        response_data['Description'] = "SPF and DMARC records are NOT identical on all the Name Servers. The SPF and DMARC TXT records should be identical. Please refer to RFC 7489 : https://datatracker.ietf.org/doc/html/rfc7489 for additional information."
        response_data['Status'] = "Warning"
        response_data['moreInfo'] = [{"SPF Record": spf, "DMARC Record": dmarc}]
        return response_data 
