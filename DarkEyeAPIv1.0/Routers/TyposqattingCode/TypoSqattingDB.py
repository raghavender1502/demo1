from .typosquatting_script import similarDomains
import motor.motor_asyncio
from dotenv import load_dotenv
import os
import asyncio
import whois
import datetime
import requests

def connect_database():
    """
    Connection establishment to MongoDB
    """
    load_dotenv()
    userName= os.getenv("MasterUser")
    password=os.getenv("MasterPassword")
    mongoDBURL = os.getenv("MongoDBURL")
    client=None
    try:
        client=motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://"+userName+":"+password + mongoDBURL)
    except:
        print("Connection is not established")
    return client
        
async def search_in_Typosqatting(domain):
    load_dotenv()
    mongoDBName = os.getenv("MongoDBName")
    collectionName = os.getenv("TypoSquattingCollection")
    client=connect_database()
    db = client.get_database(mongoDBName)
    collection = db[collectionName]
    data = await collection.find_one({"Domain": domain})
    return data

async def store_in_Typosqatting(data):
    load_dotenv()
    mongoDBName = os.getenv("MongoDBName")
    collectionName = os.getenv("TypoSquattingCollection")
    client=connect_database()
    db = client.get_database(mongoDBName)
    collection = db[collectionName]
    
    new_data=data.copy()
    result = await collection.insert_one(new_data)
    new_data["_id"]=str(new_data["_id"])

    return data

def fetch_whois_details(data):
            # high_risk_countries = ['Afghanistan','Algeria','Belarus','Burma/Myanmar*','Burma/Myanmar',
            #                        'Cambodia','Central African Republic','China**','China','Cuba*','Cuba',
            #                        'Cyprus','Egypt','Ethiopia','Eritrea','Guinea','Iran*','Iran',
            #                        'Iraq','Liberia','Libya','Niger','North Korea*','North Korea','Russia**','Russia',
            #                        'Sierra Leone','Somalia','South Sudan','Sudan','Syria*','Syria','Taiwan',
            #                        'Ukraine/Crimea and Donbas Regions*','Ukraine/Crimea and Donbas Regions','Venezuela','Yemen']
            
            for i in data["Results"]:
                try:
                    r = whois.whois(i["domain"])
                    #print(r)
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

                    # try:
                    #     if type(r.country) != str:
                    #         whois_dict['country'] = ""
                    #     else:
                    #         whois_dict['country'] = r.country
                    # except: 
                    #     whois_dict['country'] = ""

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
                                "emails":"",}
                    #print(whois_dict)
                i["whois"] = whois_dict
                # try:
                #     if type(r.country) == str:
                #         if r.country in high_risk_countries:
                #             i["status"] = "Warning"
                #             i["description"] = (f"The domain {i['domain']} is registered in high risk country")
                #             i["moreinfo"] = f"The domain {i['domain']} is registered in {r.country}"
                #         else:
                #             i["status"] = "Ok"
                #             i["description"] = (f"The domain {i['domain']} is registered in low risk country")
                #             i["moreinfo"] = f"The domain {i['domain']} is registered in {r.country}"    
                #     else:
                #         i["status"] = "Skipped"
                #         i["description"] = ("Unable to fetch country field at the moment.")
                #         i["moreinfo"] = "Country field not found."           
                # except:
                #         i["status"] = "Skipped"
                #         i["description"] = ("Unable to fetch country field at the moment.")
                #         i["moreinfo"] = "Country field not found." 

            return data
            #print(data)

def TyposqattinChecks(domain):
    try:
        try:
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(search_in_Typosqatting(domain)) 
        except:
            print("Can't connect to the database while searching in database")
            pass
        try:
            data['_id']=str(data['_id'])
            data1=data.copy()
            
            data1.pop('_id')
            
            final_response = fetch_whois_details(data1)
            #print(final_response)
            return final_response
        except:
            data = similarDomains(domain)
            try:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(store_in_Typosqatting(data))
            except:
                data = {}
                print("Can't connect to the database while storing")
                pass
            data1=data.copy()
            final_response = fetch_whois_details(data1)
            #print(final_response)
            return final_response
    except:
        print("Something wrong in Auth or user permission")
        return None


