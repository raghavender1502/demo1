
import requests

from .mx_functions import check_duplicate_MX_records, check_IP, get_ns_records, check_domain, check_IP_status, get_spf_records, get_dmarc_records, check_identical_spf_and_dmarc, get_IPv4, get_IPv6, check_A_records, check_AAAA_records, check_CNAME_records
from .checkConfiguration import test_mx_records

import dns.resolver
from dotenv import load_dotenv
import os

################### function to get the MX records for target domain #####################
def get_MX_records(target):
    load_dotenv()
    apikey = os.getenv("HackerTargetAPIKEY")
    try:
        if len(apikey) == 0:
            
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}".format(target))
            
        else:
            
            r = requests.get("https://api.hackertarget.com/dnslookup/?q={}&apikey={}".format(target,apikey))

        p = r.text
        spli = p.split("\n")

        try:
            MX = [s for s in spli if s.startswith("MX :")]
            MX = [j[8:].strip(".") for j in MX]

        except:
            pass
        print("MX; From HT: ",MX)    
        return MX
    except:
        return("An error occurred.")

def get_mx_server(domain):
    res_list = []
    mx_list = []
    try:
        result = dns.resolver.resolve(domain, 'MX')
        for val in result:
            res_list.append(str(val))
        for i in res_list:
            mx_list.append(i.split()[1])
        print("mx_list; From dns.resolver: ",mx_list)
        return mx_list  
    except:
           return mx_list      

def getTestResults(target):
    mx_data = {
        "domain": target,
        "detailedResponse": {
            "MX-records": [],
            "testResults": []
        }}

    
    mx_records = get_mx_server(target)
    if(len(mx_records)==0):
         mx_records=get_MX_records(target)
         if len(mx_records) ==0:
            mx_data_new = {"detailedResponse":{"testResults": [
                        {
                        "TestName": "A records configured",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"This test is performed to check reachability of mail servers via IPv4."}]
                        },
                        {
                        "TestName": "AAAA records configured",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"This test is performed to check reachability of mail servers via IPv6."}]
                        },
                        {
                        "TestName": "IPs are public",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"It is recommended to use public IP addresses for the mail servers to be able to reach via Internet."}]
                        },
                        {
                        "TestName": "Mail servers are not present in CNAME records",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"As per RFC 1034, section 3.6.2: if a name appears in the right-hand side of RR (Resource Record) it should not appear in the left-hand name of CNAME RR, thus CNAME records should not be used with NS and MX records."}]
                        },
                        {
                        "TestName": "Exchange fields contain valid domain names",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"Provide only valid domain names in the Exchange field of MX Record. Also, Mail servers with bad Exchange fields are unreachable."}]
                        },
                        {
                        "TestName": "Exchange fields don't contain IPs",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"All the Exchange fields should contain domain names only."}]
                        },
                        {
                        "TestName": "Name Servers return identical MX records",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"Configure DNS to return identical MX records."}]
                        },
                        {
                        "TestName": "No duplicate MX records",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"It is recommended that MX records point to different IPs."}]
                        },
                        {
                        "TestName": "SPF",
                        "Status": "Skipped",
                        "record": "",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"Email spam and phishing often use forged 'from' addresses, so publishing and checking SPF records can be considered anti-spam techniques. Please refer to RFC 7208 : https://datatracker.ietf.org/doc/html/rfc7208 for additional information."}]
                        },
                        {
                        "domain": target,
                        "TestName": "DMARC",
                        "Status": "Skipped",
                        "record": "",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"DMARC configuration helps in mitigating risks involved in Email spoofing."}]
                        },
                        {
                        "TestName": "Identical SPF and DMARC records",
                        "Status": "Skipped",
                        "Description": "This test was skipped since Mail Server for "+str(target)+ " were not found.",
                        "moreInfo": [{"More Info":"The SPF and DMARC TXT records should be identical. Please refer to RFC 7489 : https://datatracker.ietf.org/doc/html/rfc7489 for additional information."}]
                        }
            ]}}
            
            return mx_data_new
    
    ########## setting key-value fields for all the MX records ##########
    print("mx_records: ",mx_records)
    for record in mx_records:
        data = {record: {}}

        ipv4 = get_IPv4(record)
        ipv6 = get_IPv6(record)
        A_records = check_A_records(record)
        AAAA_records = check_AAAA_records(record)
        CNAME_records = check_CNAME_records(target)
        ip_status = check_IP_status(record)
        is_domain = check_domain(record[:-1])
        is_IP = check_IP(record)
        ns_records = get_ns_records(record)

        data[record]["IPv4"] = ipv4
        data[record]["IPv6"] = ipv6
        data[record]["A_Records"] = A_records
        data[record]["AAAA_Records"] = AAAA_records
        if CNAME_records["Status"] == "Failed":
            data[record]["CNAME_records"] = {
                "status": "Ok", "description": "Mail Server not present in CNAME records"}
        data[record]["IP_Status"] = ip_status
        data[record]["isValidDomain"] = is_domain
        data[record]["is_IP"] = is_IP
        data[record]["NS_records"] = ns_records

        mx_data["detailedResponse"]["MX-records"].append(data)

    A_records, AAAA_records, IP_status, CNAME_records, domain_names, contains_IPs, identical_MX = test_mx_records(
        mx_data["detailedResponse"]['MX-records'])

    mx_data["detailedResponse"]["testResults"].append(A_records)
    mx_data["detailedResponse"]["testResults"].append(AAAA_records)
    mx_data["detailedResponse"]["testResults"].append(IP_status)
    mx_data["detailedResponse"]["testResults"].append(CNAME_records)
    mx_data["detailedResponse"]["testResults"].append(domain_names)
    mx_data["detailedResponse"]["testResults"].append(contains_IPs)
    mx_data["detailedResponse"]["testResults"].append(identical_MX)
    mx_data["detailedResponse"]["testResults"].append(check_duplicate_MX_records(
        mx_records))
    mx_data["detailedResponse"]["testResults"].append(get_spf_records(target))
    mx_data["detailedResponse"]["testResults"].append(get_dmarc_records(
        target))
    mx_data["detailedResponse"]["testResults"].append(check_identical_spf_and_dmarc(
        target))
    
    mx_data_new={}
    mx_arry=[]
    mx_data_new['domain']=mx_data['domain']
    mx_data_new["detailedResponse"]={"testResults":mx_data["detailedResponse"]["testResults"]}
    try:
        for k in mx_data["detailedResponse"]['MX-records']:
            temp={}
            temp["MxRecordName"]=list(k.keys())[0]
            temp.update(list(k.values())[0])
            mx_arry.append(temp)
    except:
        mx_arry=[]
    mx_data_new["detailedResponse"]['MX-records']=mx_arry

    return mx_data_new
