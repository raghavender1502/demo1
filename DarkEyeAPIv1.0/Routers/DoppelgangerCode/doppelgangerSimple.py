import tld
from .doppelganger import get_simple_permutations 
from tld import get_tld
import dns.resolver
import datetime
import whois
import os
import requests
from dotenv import load_dotenv
load_dotenv()
whois_apikey = os.getenv("WhoisAPI")

lang_codes = {'org': ['bs', 'bg', 'be', 'mk', 'ru', 'sr', 'uk', 'da', 'de', 'hu', 'is', 'lv', 'lt', 'pl', 'es',
                          'sv'], 'com': ['latin', 'lisu'], 'se': ['latin']}

def getDoppelgangerDomains(domain):
    doppelganger_domain_exist = []
    doppelganger_domain_not_exist = []
    try:
        res = get_tld("http://"+domain, as_object=True)

        tld_of_domain = str(res)
        domain_wo_tld = str(res.domain)

        doppelganger_domains_list = []
 
        try:
            if tld_of_domain in lang_codes.keys():

                for lang in lang_codes[tld_of_domain]:
                  
                    doppelganger_domains_list+=get_simple_permutations(domain_wo_tld,tld_of_domain,lang)
            else:  
                doppelganger_domains_list = get_simple_permutations(domain_wo_tld,tld_of_domain,)
                
            for doppelganger_domain in doppelganger_domains_list:
                try:
                    dns.resolver.resolve(doppelganger_domain, 'A')

                    doppelganger_domain_exist.append(doppelganger_domain)
                except:
                    doppelganger_domain_not_exist.append(doppelganger_domain)
            try:
                all_e_values = []
                for e_values in doppelganger_domain_exist:
                    e_dict = {"name": e_values}
                    all_e_values.append(e_dict)
            except:
                all_e_values = []
            
            try:
                all_ne_values = []
                for ne_values in doppelganger_domain_not_exist:
                    ne_dict = {"name": ne_values}
                    all_ne_values.append(ne_dict)    
            except:
                all_ne_values = []
        
        
            
        except Exception as e:
            print(e)
        

    except:
        pass

    e_result_list = []
    for i in all_e_values:
        try:
            r = whois.whois(i["name"])
            whois_dict = {}
            try:
                if type(r["creation_date"]) == list:
                    c_date = r["creation_date"]
                    whois_dict['creation_date'] = c_date[0].strftime('%Y-%m-%d %H:%M:%S')
                elif type(r["creation_date"]) == datetime.datetime:
                    whois_dict['creation_date'] = r["creation_date"].strftime('%Y-%m-%d %H:%M:%S')
                elif(type(r['creation_date']) == None or r['creation_date'] == None):
                    whois_dict['creation_date'] = ""
                else:
                    whois_dict['creation_date'] = str(r['creation_date'])
            except:
                whois_dict['creation_date'] = ""   

            try:
                if type(r["updated_date"]) == list:
                    u_date = r["updated_date"]
                    whois_dict['updated_date'] = u_date[0].strftime('%Y-%m-%d %H:%M:%S')
                elif type(r["updated_date"]) == datetime.datetime:
                    whois_dict['updated_date'] = r["updated_date"].strftime('%Y-%m-%d %H:%M:%S')
                elif(type(r['updated_date']) == None or r['updated_date'] == None):
                    whois_dict['updated_date'] = ""
                else:
                    whois_dict['updated_date'] = str(r['updated_date'])
            except:
                whois_dict['updated_date'] = "" 

            try:
                if(type(r['registrar']) == list):
                    whois_dict['registrar'] = r['registrar'][0]
                elif(type(r['registrar']) == None or r['registrar'] == None):
                    whois_dict['registrar'] = ""
                else:
                    whois_dict['registrar'] = r['registrar']
            except:
                whois_dict['registrar'] = ""    

            try:
                if type(r["emails"]) == list:
                    c_date = r["emails"]
                    whois_dict['emails'] = str(c_date)
                elif(type(r['emails']) == None or r['emails'] == None):
                    whois_dict['emails'] = ""
                else:
                    whois_dict['emails'] = str(r['emails'])
            except:
                whois_dict['emails'] = ""

            if whois_dict["emails"] == "":
                whois_key = os.getenv("WhoisAPI")
                whois_xml = requests.get("https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey="+whois_key+"&domainName="+i["domain"]+"&outputFormat=JSON")                  
                if whois_xml.status_code ==200:
                    wi_resp = whois_xml.json()
                    try:
                        whois_dict['emails'] = wi_resp["WhoisRecord"]["contactEmail"] 
                    except:
                        whois_dict['emails'] = ""     
                         
        except Exception as e:
            print("Exception#: ",e)
            whois_dict = {"creation_date": "",
                          "updated_date":"",
                          "registrar":"",
                          "emails":""}
        e_result_dict = {"domain": i["name"],
                         "whois": whois_dict}
        e_result_list.append(e_result_dict)
    
    return {"Domain":domain , "extSource": "Github Doppelganger VPav", "ExistingDomain":e_result_list , "NonExistingDomain":all_ne_values}

