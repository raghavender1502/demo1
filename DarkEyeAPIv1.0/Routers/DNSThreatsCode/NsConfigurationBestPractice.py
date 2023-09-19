import requests
import dns.resolver
from ipwhois.asn import IPASN
from ipwhois.net import Net
import json
import argparse
from ipaddress import ip_network
from dotenv import load_dotenv
import os 
import subprocess


def GetNameServer(domain):
    result = dns.resolver.resolve(domain, 'NS')
    len_res = len(result)
    return len_res,result

def NameServerCount(count):
    info1="Domain has {} name servers".format(count)
    info2="Domain has {} name servers. Recommended to be between 2 and 7".format(count)
    if(count>=2 and count<=7):
        return "Ok",info1
    else:
        return "Warning",info2

def GetIP(nsrecord):
    res = dns.resolver.resolve(nsrecord, 'A')
    for val in res:
        return val

def FindNetwork(ip,IP):
    if(ip >= 0 and ip <= 127):
        NetVal=IP+"/8"
        NetworkVal=ip_network(NetVal, strict = False).network_address
        NetworkVal=str(NetworkVal)+"/8"
    elif(ip >=128 and ip <= 191):
        NetVal=IP+"/16"
        NetworkVal=ip_network(NetVal, strict = False).network_address
        NetworkVal=str(NetworkVal)+"/16"
    elif(ip >= 192 and ip <= 223):
        NetVal=IP+"/24"
        NetworkVal=ip_network(NetVal, strict = False).network_address
        NetworkVal=str(NetworkVal)+"/24"
    else:
        NetworkVal=None
    return NetworkVal

def DistributedNetwork(IPList,NsList):
    info1="Name Servers are distributed over different networks."
    info2="Some Name Servers are located in the same network."
    NetWorkList=[]
    info2dict=[]
    for i in range(len(IPList)):
        ip = IPList[i].split(".")
        NetworkVal = FindNetwork(int(ip[0]),IPList[i])
        info2dict.append({"Name Server":NsList[i],"Network":NetworkVal})
        NetWorkList.append(NetworkVal)
    if len(NetWorkList)==len(set(NetWorkList)):
        return "Ok",info1,None
    else:
        return "Warning",info2,info2dict

def GetAsnFromHackerTarget(IPList):
    load_dotenv()
    apikey = os.getenv("HackerTargetAPIKEY")
    AsnList=[]
    for IP in IPList:
        if len(apikey) == 0:
            
            url = requests.get("https://api.hackertarget.com/aslookup/?q={}".format(IP))
            
        else:
            
            url = requests.get("https://api.hackertarget.com/aslookup/?q={}&apikey={}".format(IP,apikey))
        response = requests.get(url)
        if response.status_code == 200:
            AsnList.append((response.text.split(",")[1].strip('"')))
    return AsnList


def DistributedMultipleASN(NsList,AsnList):
    info1="Name Servers are distributed over multiple ASNs."
    info2="Some Name Servers are located on a single ASN."
    
    info2dict=[]
    for i in range(len(AsnList)):
        
        info2dict.append({"Name Server":NsList[i],"Autonomous System Number ASN": "AS"+AsnList[i]})
    if(len(AsnList)==len(set(AsnList))):
        return "Ok",info1,None
    else:
        return "Warning",info2,info2dict

def IsVersionPublicNsLookup(Ns):
    
    try:
        r = subprocess.run(['nslookup', '-q=txt','-class=CHAOS','version.bind',Ns], timeout=1,capture_output=True,text=True)
    except subprocess.TimeoutExpired as e:
        r=None

    if r!=None:
        output=r.stdout
    else:
        output=" "
    
    splitout=output.split("\n")
    ver_str= "version.bind\ttext ="
    for val in splitout:
        if ver_str in val:
            
            if any(map(str.isdigit, val)):
                return 1,{"Name Server":Ns,"Version":val.strip(ver_str).strip('""')}
            else:
                return 0,{"Name Server":Ns,"Version":None}
     
    return 0,{"Name Server":Ns,"Version":None}

    
def IsVersionPublicFPDNS(Ns):
    try:
        r = subprocess.run(['fpdns', Ns], timeout=1,capture_output=True,text=True)
    except subprocess.TimeoutExpired as e:
        r=None

    if r!=None:
        output=r.stdout
    else:
        output=" "

    output_l= output.split(":")
    
    flag = 0
    for val in output_l:
        if "TIMEOUT" in val:
            flag=1
        elif "No match found" in val:
            flag=1
        elif len(output_l)<=1:
            flag=1
    if flag==0:
        return 1,{"Name Server":Ns,"Version":output_l[1].strip("\n").strip()}
    else:
        return 0,{"Name Server":Ns,"Version":None}

def HiddenVersion(NsList):
    info1="All the Name Server's versions are hidden."
    info2="Version is exposed for the listed Name Servers."
    
    info2dict=[]
    sum_st=0
    for val in NsList:
        st,infd=IsVersionPublicNsLookup(val)
        if st==0:
            try:
                st,infd=IsVersionPublicFPDNS(val)
            except:
                pass
        info2dict.append(infd)
        sum_st+=st
    if sum_st>0:
        return "Warning",info2,info2dict
    else:
        return "Ok",info1,None

def ConfigurationCheck(domain):
    data ={}
    IPList=[]
    NsList=[]
    AsnList=[]
    
    try:
        len_ns,res=GetNameServer(domain)
    except:
        res=None
    try:
        for ns in res:
            try:
                NsList.append(str(ns))
                temp=str(GetIP(str(ns)))
                IPList.append(temp)
            except Exception as e:
                print(e)
            try:
                net = Net(temp)
                obj = IPASN(net)
                results = obj.lookup()
                AsnList.append(results['asn'])
            except Exception as e:
                print(e)
            
    except Exception as e:
        print(e)
    
    if(len(AsnList)==0):
        try:
            AsnList=GetAsnFromHackerTarget(IPList)
        except Exception as e:
            print(e)

    try:
        status1,info1 = NameServerCount(len_ns)
    except:
        status1=None
        info1=None

    try:
        status2,info2,info2dict2=DistributedNetwork(IPList,NsList)
    except:
        status2=None
        info2=None

    try:
        status3,info3,info2dict3=DistributedMultipleASN(NsList,AsnList)
    except:
        status3=None
        info3=None
    
    try:
        status4,info4,info2dict4=HiddenVersion(NsList)
    except:
        status4=None
        info4=None
    
    data={"Domain":domain,"Test Results":[
        {
            "TestName":"Name servers count",
            "Status":status1,
            "Description":info1,
            "moreInfo": [{"NS Records":i} for i in NsList]},
        {
            "TestName":"Distributed over multiple networks",
            "Status":status2,
            "Description":info2,
            "moreInfo":info2dict2},
        {
            "TestName":"Distributed over multiple ASNs",
            "Status":status3,
            "Description":info3,
            "moreInfo":info2dict3},
        {
            "TestName":"Versions are hidden",
            "Status":status4,
            "Description":info4,
            "moreInfo":info2dict4}]}
    

    return data



def WriteJson(data):
    """
    Takes data and dump this data in json format data.
    Parameters:
        data: Data which is to be stored in json file and format. 
    Returns:
        Dump the json file and prints the json data. 
    """
    final_data=json.dumps(data)
    print(final_data)
    #return final_data

    #Store the data in json file
    """
    with open("sample.json", "w") as outfile:
        json.dump(final_data), outfile)
    """

if __name__ == "__main__":
    #Argument parser to take command line input
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", help = "To choose domain as argumet")
        parser.add_argument("-f", help = "To choose file as argument")
        args = parser.parse_args()
    except Exception as e:
        print("Command is not proper:",e)

    #For argument as domain
    if(args.d):
        try:
            user_inp = args.d
            data =ConfigurationCheck(user_inp)
            WriteJson(data)
        except Exception as e:
            print(e)
    
    #For argument as file
    elif(args.f):
        #For storing data
        data={}
        try:
            #File Location
            inp_file_path=args.f
            file_path=inp_file_path

            #Reading text file
            with open(file_path) as f:
                lines = f.readlines() 
                
            #Finding gitrootcheck for each domain from the file
            for line in lines:
                d =ConfigurationCheck(line.strip())
                data.update({line.strip():d})
        except Exception as e:
            print(e)
        #Json function to dump file in json format
        WriteJson(data)  

    else:
        print("You have not entered proper command")
