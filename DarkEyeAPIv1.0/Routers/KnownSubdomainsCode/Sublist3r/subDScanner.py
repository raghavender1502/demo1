from ..Sublist3r import sublist3r
import json
import socket
import argparse

def getsubDomains(domain):
    subdomains = sublist3r.main("{}".format(domain), 10, savefile=None, ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
    #json_res_subdomains = json.dumps(subdomains)
    #print(json_res_subdomains)
    #Logic for set type data of subdomains
    comparetype=set()
    if type(subdomains)==type(comparetype):
        subdomains=list(subdomains)
    ipv4s = list()
    for subdomain in subdomains:
        ip = getIP(subdomain)
        ipv4s.append(ip)
    #json_res_ipv4s = json.dumps(ipv4s)
    #print(json_res_ipv4s)
    data={}
    try:
        data["Domain"]=domain
        data["SubDomains"]=subdomains
        data["IPV4s"]=ipv4s
    except:
        data={}
    #data=json.dumps(data)
    return data

def getIP(subdomain):
    try:
        subdomain_ip = socket.gethostbyname(subdomain)
    except:
        #print("Unable to get Hostname and IP")
        subdomain_ip = "NA"
    return subdomain_ip
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomains finder : use -D as switch/flag")
    parser.add_argument("-D", dest="domain",
                  help="Single domain to be checked for getting its subdomains")
    args = parser.parse_args()
    domain = str(args.domain)
    getsubDomains(domain)'''
