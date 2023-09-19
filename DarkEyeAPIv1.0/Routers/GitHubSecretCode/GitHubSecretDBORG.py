from .GithubSecretMain import getDataFromOrg

import motor.motor_asyncio
from dotenv import load_dotenv
import os
import asyncio


def Connect_Database():
    """
    Connection establishment to MongoDB
    """
    load_dotenv()
    UserName= os.getenv("MasterUser")
    PassWord=os.getenv("MasterPassword")
    MongoDBURL = os.getenv("MongoDBURL")
    client=None
    try:
        client=motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://"+UserName+":"+PassWord + MongoDBURL)
    except:
        print("Connection is not established")
    return client
        
async def search_in_githubsecretorg(domain):
    MongoDBName = os.getenv("MongoDBName")
    CollectionName = os.getenv("GithubSecretOrgCollection")
    client=Connect_Database()
    DB = client.get_database(MongoDBName)
    collection = DB[CollectionName]
    data = await collection.find_one({"Org": domain})
    return data

async def store_in_githubsecretorg(data):
    
    MongoDBName = os.getenv("MongoDBName")
    CollectionName = os.getenv("GithubSecretOrgCollection")
    client=Connect_Database()
    DB = client.get_database(MongoDBName)
    collection = DB[CollectionName]
    
    new_data=data.copy()
    result = await collection.insert_one(new_data)
    new_data["_id"]=str(new_data["_id"])

def GitHubSecretOrgChecks(domain):
    try:
        try:
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(search_in_githubsecretorg(domain))
            
        except:
            print("Can't connect to the database while searching in database")
            pass
        
        if(data):
                data['_id']=str(data['_id'])
                data1=data.copy()
                
                data1.pop('_id')
                return data1
        else:
            data = getDataFromOrg(domain)
            if len(data["TestResults"])==0:
                return data
            else:
                try:
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(store_in_githubsecretorg(data))
                except:
                    print("Can't connect to the database while storing")
                    pass
                data1=data.copy()
                return data1
    except:
        print("Something wrong in Auth or user permission")
        return {"Description":"Something went wrong"}

