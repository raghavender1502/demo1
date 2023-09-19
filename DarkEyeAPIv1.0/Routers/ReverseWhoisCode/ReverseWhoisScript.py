from dotenv import load_dotenv
import os
import time
import requests
import http.client as http
import json
import whois




def whoiscollector_script(domain):
    load_dotenv()
    api_key  = os.getenv("WhoisAPI")
    timestr = time.strftime("%Y%m%d-%Hhours%Mmins%Sseconds")
    
    response = requests.get("https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={}&domainName={}&outputFormat=JSON".format(api_key,domain))


    #print(response)
    wi_resp ={}
    if response.status_code == 200:
        wi_resp = response.json()
        #print(wi_resp)
        try:
            Registered_on = wi_resp["WhoisRecord"]["createdDate"]
        except:
            try:
                Registered_on = wi_resp["WhoisRecord"]["registryData"]["createdDate"]
            except:
                Registered_on = ""
        try:
            Updated_on = wi_resp["WhoisRecord"]["updatedDate"]
        except:
            try:
                Updated_on=wi_resp["WhoisRecord"]["registryData"]["updatedDate"]
            except:
                Updated_on = ""
        try:
            Expires_on = wi_resp["WhoisRecord"]["expiresDate"]
        except:
            try:
                Expires_on=wi_resp["WhoisRecord"]["registryData"]["expiresDate"]
            except:
                Expires_on = ""
        try:
            Organization = wi_resp["WhoisRecord"]["registrant"]["organization"]
        except:
            try:
                Organization=wi_resp["WhoisRecord"]["registryData"]["registrant"]["organization"]
            except:
                Organization = ""
        try:
            name=wi_resp["WhoisRecord"]["registryData"]["registrant"]["name"]
        except:
            try:
                name=wi_resp["WhoisRecord"]["registrant"]["name"]
            except:
                name=""
        try:
            state = wi_resp["WhoisRecord"]["registrant"]["state"]
        except:
            try:
                state=wi_resp["WhoisRecord"]["registryData"]["registrant"]["state"]
            except:
                state = ""
        try:
            country = wi_resp["WhoisRecord"]["registrant"]["country"]
        except:
            try:
                country = wi_resp["WhoisRecord"]["registryData"]["registrant"]["country"]
            except:
                country = ""
        try:
            countryCode = wi_resp["WhoisRecord"]["registrant"]["countryCode"]
        except:
            try:
                countryCode = wi_resp["WhoisRecord"]["registryData"]["registrant"]["countryCode"]
            except:
                countryCode = ""
        try:
            Registered_by = wi_resp["WhoisRecord"]["registrarName"]
        except:
            Registered_by = ""
        try:
            ContactEmail = wi_resp["WhoisRecord"]["contactEmail"]
        except:
            ContactEmail = ""
        try:
            estimatedDomainAge = wi_resp["WhoisRecord"]["estimatedDomainAge"]
        except:
            estimatedDomainAge = ""
        try:
            domain = domain
        except:
            pass
        
        try:
            administrativeContact = wi_resp["WhoisRecord"]["administrativeContact"]
        except:
            try:
                administrativeContact=wi_resp["WhoisRecord"]["registryData"]["administrativeContact"]
            except:
                administrativeContact={}
                
        try:
            administrativeContact.pop("rawText")
            administrativeContact.pop("unparsable")
        except:
            pass
            
        
        try:
            technicalContact=wi_resp["WhoisRecord"]["technicalContact"]
        except:
            try:
                technicalContact=wi_resp["WhoisRecord"]["registryData"]["technicalContact"]
            except:
                technicalContact={}
        
        try:
            technicalContact.pop("rawText")
            technicalContact.pop("unparsable")
        except:
            pass
        try:
            telephone=wi_resp["WhoisRecord"]["registrant"]["telephone"]
        except:
            try:
                telephone=wi_resp["WhoisRecord"]["registryData"]["registrant"]["telephone"]
            except:
                telephone=""
        try:
            fax=wi_resp["WhoisRecord"]["registrant"]["fax"]
        except:
            try:
                fax=wi_resp["WhoisRecord"]["registryData"]["registrant"]["fax"]
            except:
                fax="" 
        
        try:
            postalCode=wi_resp["WhoisRecord"]["registrant"]["postalCode"]+" "
        except:
            try:
                postalCode=wi_resp["WhoisRecord"]["registryData"]["registrant"]["postalCode"]+" "
            except:
                postalCode="" 
        
        try:
            city=wi_resp["WhoisRecord"]["registrant"]["city"]+" "
        except:
            try:
                city=wi_resp["WhoisRecord"]["registryData"]["registrant"]["city"]+" "
            except:
                city="" 
        
        try:
            street1=wi_resp["WhoisRecord"]["registrant"]["street1"]+" "
        except:
            try:
                street1=wi_resp["WhoisRecord"]["registryData"]["registrant"]["street1"]+" "
            except:
                street1="" 
        if state=="":        
            address=street1+postalCode+city
        else:
            address=street1+state+" "+postalCode+city
        

        #print(Registered_on,Updated_on,Expires_on,Organization,state,country,countryCode,Registered_by,ContactEmail,estimatedDomainAge,Domain)
        new_name = name.casefold()
        new_Organization = Organization.casefold()
        if(
            new_name == "registration private" or 
            new_name == "privacy administrator" or
            new_name == "domain name manager" or 
            new_name == "redacted for privacy" or 
            new_name == "withheld for privacy purposes" or 
            new_Organization == "whois privacy service" or 
            new_Organization == "domains by proxy, llc"
                                                        ):
            #Domain Name Manager, 
            payload = {
            "General information":{
            'Registered_on':Registered_on,
            "Updated_on": Updated_on,
            "Expires_on" : Expires_on,
            "Registered_by": Registered_by
            },
            "Domain owner":{
                
            
            "Name":"",
            "Organization_name": "",
            "State": "",
            "Country": "",
            "Country_code": "",
            
            "ContactEmail": "",
            "Fax":"",
            "Telephone":"",
            "Address":""
            }
            ,
            "EstimatedDomainAge": estimatedDomainAge,
            "Domain": domain,
            "AdministrativeContact":{
                "name": "",
                "organization": "",
                "street1" : "",
                "city": "",
                "state": "",
                "postalCode": "",
                "country":"",
                "telephone": "",
                # "telephoneExt": "",
                "fax":"",
                # "faxExt":""
            },
            "TechnicalContact":{
                "name":"",
                "organization": "",
                "street1" : "",
                "city": "",
                "state": "",
                "postalCode": "",
                "country":"",
                "telephone": "",
                # "telephoneExt": "",
                "fax":"",
                # "faxExt":""


            }
            
            
        }
        #print(Registered_on,Updated_on,Expires_on,Organization,state,country,countryCode,Registered_by,ContactEmail,estimatedDomainAge,Domain)
        else:
            payload = {
            "General information":{
            'Registered_on':Registered_on,
            "Updated_on": Updated_on,
            "Expires_on" : Expires_on,
            "Registered_by": Registered_by
            },
            "Domain owner":{
                
            
            "Name":name,
            "Organization_name": Organization,
            "State": state,
            "Country": country,
            "Country_code":countryCode,
            
            "ContactEmail": ContactEmail,
            "Fax":fax,
            "Telephone":telephone,
            "Address":address
            }
            ,
            "EstimatedDomainAge": estimatedDomainAge,
            "Domain": domain,
            "AdministrativeContact":administrativeContact,
            "TechnicalContact":technicalContact
            
        }
        #file_name = timestr+"data.csv"
        #folder_path = "C:\\Users\\Raghavender\\Downloads\\"+file_name
        #input_variable = [Registered_on,Updated_on,Expires_on,Organization,state,country,countryCode,Registered_by,ContactEmail,estimatedDomainAge,Domain]
        #######################code of mongoDB##################### data,loop,loop.run
        #data = {"Registered_on":Registered_on,"Updated_on":Updated_on,"Expires_on":Expires_on,"Organization":Organization,"state":state,"country":country,"countryCode":countryCode,"Registered_by":Registered_by,"ContactEmail":ContactEmail,"estimatedDomainAge":estimatedDomainAge,"Domain":Domain}
        '''with open(folder_path,'a',newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(input_variable)'''
    else:
        #print("Invalid Whoiscollector key")
        payload = {}
    #print(payload)
    return payload



def get_reverse_whois(includeList):
    api_key  = os.getenv("WhoisAPI")
    sinceAfter = os.getenv("ReverseWhois_sinceAfter")
    payload = {
        "apiKey": api_key,
        "mode": "purchase",
        "searchAfter": int(sinceAfter),
        "punycode": True,
        "basicSearchTerms":
        {
            "include": includeList
        }
    } 

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn = http.HTTPSConnection('reverse-whois.whoisxmlapi.com')
    conn.request('POST', '/api/v2', json.dumps(payload), headers)
    text = conn.getresponse().read().decode('utf8')
    response_json = json.loads(text)
    #print(response_json)
    return response_json["domainsList"]


def GetReverseWhoIsData(domain):
    
    payload=whoiscollector_script(domain)
    
    #############Reverse whois ---- start
    reverse_whois = []
    includeList = []
    reverse = payload["Domain owner"]
    if reverse["ContactEmail"] != "":
        includeList.append(reverse["ContactEmail"])
    if reverse["Name"] != "":
        includeList.append(reverse["Name"])
    if reverse["Organization_name"] != "":
        includeList.append(reverse["Organization_name"])
    print("includeList: ",includeList)
    try:
        if includeList == []:
            finaly_payload = {
            "target_domain": domain,
            "privacyEnabled": True,
            "displayMessage": "Reverse Whois Information cannot be obtained as the Domain Information is protected and hidden by Private Proxy/ Whois Guard.",
            "data": []
            }
            return finaly_payload


            
        else:
            
            relatedDomainList = get_reverse_whois(includeList)
            for relatedDomain in relatedDomainList:
                reversedict = {}               
                r = whois.whois(relatedDomain)

                try:
                    if type(r['domain_name']) == list:
                        reversedict['domain'] = r['domain_name'][0]
                    elif(type(r['domain_name']) == None or r['domain_name'] == None):
                        reversedict['domain'] = ""
                    else:
                        reversedict['domain'] = r['domain_name']
                except:
                    reversedict['domain'] = ""
                

                try:
                    if(type(r['creation_date']) == list):
                        reversedict['date'] = str(r['creation_date'][0])
                    elif(type(r['creation_date']) == None or r['creation_date'] == None):
                        reversedict['date'] = ""
                    else:
                        reversedict['date'] = str(r['creation_date'])
                except:
                    reversedict['date'] = ""
                
                
                try:
                    if(type(r['registrar']) == list):
                        reversedict['registrar'] = r['registrar'][0]
                    elif(type(r['registrar']) == None or r['registrar'] == None):
                        reversedict['registrar'] = ""
                    else:
                        reversedict['registrar'] = r['registrar']
                except:
                    reversedict['registrar'] = ""
                
                reverse_whois.append(reversedict)
        #############Reverse whois ---- end    
        
            finaly_payload = {
                "target_domain": domain,
                "privacyEnabled": False,
                "displayMessage": "",
                "data": reverse_whois
                
                
            }
        return finaly_payload
    except:
        finaly_payload = {
            "target_domain": domain,
            "privacyEnabled": True,
            "displayMessage": "Reverse Whois Information cannot be obtained as the Domain Information is protected and hidden by Private Proxy/ Whois Guard.",
            "data": []
            }
        return finaly_payload
