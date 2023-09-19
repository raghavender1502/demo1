from xml.dom.minidom import Element
from tld import get_tld,get_fld
import random
import dns.resolver
import sys
import re
import os
import dns.name
import dns.message
import dns.query
import dns.flags
import socket
import validators
import whois
import time
from dotenv import load_dotenv
import os
import ast


#find list of parent Parent Name Server for top level domain
def getParentNameServer(res): # Accepts TLD as input

    cmd ="dig @8.8.8.8 "+res+" ns +noall +answer"

    try:
        output = os.popen(cmd).read()
        output = re.sub(' +', ' ', output)
        output= output.split('\n')
        output.pop()
        parent_list = []
        for str in output:
            new_string= str.split('\t')
            if validators.domain(new_string[-1][:-1]) == True:
                parent_list.append(new_string[-1])
        #print(parent_list)
        parent_random = random.choice(parent_list)
        print("parent_random", parent_random)
        return parent_random
    except Exception as e:
        print("Exception at getParentNameServer: ",e)
        return []


""" Cname for Ns record  -----------Start-------------------"""
def isCname(ns):
    cnames = []
    try:
        result = dns.resolver.resolve(ns, 'CNAME')
        for cnameval in result:
            cnames.append(cnameval.target)
        return cnames
    except:
        return cnames

# check wheather nsrecord point to cname
def checkCNAME(NS_records):
    CnameList = []
    try:
        for ns_record in NS_records:
            cnames = []
            cnames = isCname(ns_record)
            if len(cnames)>0:
                for cname in cnames:
                    CnameList.append(cname)

        return CnameList
    except:
        return CnameList
""" Cname for Ns record  -----------End-------------------"""


""" Recursive allowed or not -----------------------Start-------------------------"""
def check_recursive(ns_server,Domain):
    """
    Check if a NS Server is recursive.
    """
    load_dotenv()
    timeout_check_recursive = os.getenv("timeout_check_recursive")
    timeout_check_recursive = ast.literal_eval(timeout_check_recursive)
    timeout= int(timeout_check_recursive)                                                    
    is_recursive = False
    query = dns.message.make_query(Domain, dns.rdatatype.NS)
    try:
        response = dns.query.udp(query,ns_server,timeout)
        recursion_flag_pattern = "\.*RA\.*"
        flags = dns.flags.to_text(response.flags)
        result = re.findall(recursion_flag_pattern, flags)
        if (result):
            print("\t Recursion enabled on NS Server {0}".format(ns_server))
            return True
    except (socket.error, dns.exception.Timeout):
        return is_recursive 
    return is_recursive 


def findRecursive(NS_records,Domain):
    recursive_allow = []
    try:
        for ns in NS_records:
            result = dns.resolver.resolve(ns, 'A')
            for ipval in result:
                #need ip for that ns record to check recursive as this funtion only work when we pass ip ie a record for that name server
                if check_recursive(ipval.to_text(),Domain):
                    recursive_allow.append(ns)
        return recursive_allow
    except:
        return recursive_allow
""" Recursive allowed or not -----------------------End-------------------------"""


""" Identical NameServers or not ---------------------Start---------------------------"""
diffrent_ns = []
def helperIdenticalRecord(Ns):
    cmd = "nslookup -query=NS "+ Ns+" 8.8.8.8"
    try:
        #print(Ns)
        output = os.popen(cmd).read()
        new_string = re.sub(r'\n', '', output)
        #print("new_string: ",new_string)
        new_string2 = new_string.split("primary name server")[1].split()[1]
        #print("new_string2: ",new_string2)
        diffrent_ns.append([Ns,new_string2])
    except:
        print("error in identical ns record function")
        return 0
 
def CheckIdenticalNsRecord(NS_records):
    IdenticalNS = []
    diffrent_ns.clear()
    for ns in NS_records:
        try:
            helperIdenticalRecord(ns)
        except:
            try:
                time.sleep(3)
                print("Trying again for ",ns)
                helperIdenticalRecord(ns)
            except:
                print("Skipped ",ns)
                continue
    length = len(diffrent_ns)
    for i in range(0,length):
        for j in range(i+1,length):
            if diffrent_ns[i][1]!=diffrent_ns[j][1] :
                IdenticalNS.append(diffrent_ns[i][0]+ " and " + diffrent_ns[j][0])
    #print("IdenticalNS: ",IdenticalNS)
    return IdenticalNS

""" Identical NameServers or not ---------------------End---------------------------"""


""" Valid Nameserver Domain --------------------------Start----------------------------"""
def checkValidNameServer(Ns):
    try:
        size = len(Ns)
        return validators.domain(Ns[0:size-1])
    except:
        return False

def is_registered(domain_name):
    """
    A function that returns a boolean indicating 
    whether a `domain_name` is registered
    """
    size = len(domain_name)
    domain_name =domain_name[0:size-1]
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

def validNS(NS_records):
    InvalidNS = []
    for ns in NS_records:
        if is_registered(ns) and checkValidNameServer(ns):
            pass
        else:
            InvalidNS.append(ns)
    return InvalidNS

""" Valid Nameserver Domain --------------------------End----------------------------"""


""" Missing Name servers and Stealth Name servers ---------------------start----------------------- """
#get list of Name Servers that got from parent
def getDomainNameServerFromParent(domain,parent):
    nsParent = []
    cmd="dig NS "+domain+" @"+parent+" +noall +authority +tries=1"
    try:
        output = os.popen(cmd).read()
        if output.find("connection timed out")!=-1:
            return nsParent
        output = re.sub(' +', ' ', output)
        output= output.split('\n')
        output.pop()
        for str in output:
            new_string= str.split('\t')
            nsParent.append(new_string[-1])
        #print("nsParentNameServer: ",nsParent)
        return nsParent
    except:
        print("something wrong while fetching parent name server")
        return nsParent

#get list of NameServer that got using authoritative nameservers
def getDomainNameServerFromAuthoritative(domain,authoritative):
    nsauthoritative = []
    cmd="dig NS "+domain+" @"+authoritative+" +noall +answer +tries=1"
    try:
        output = os.popen(cmd).read()
        if output.find("connection timed out")!=-1:
            return nsauthoritative
        output = re.sub(' +', ' ', output)
        output= output.split('\n')
        output.pop()
        for str in output:
            new_string= str.split('\t')
            nsauthoritative.append(new_string[-1])
        #print("nsauthoritative: ",nsauthoritative)
        return nsauthoritative
    except:
        print("something wrong while fetching parent name server")
        return nsauthoritative

     #ie authoritative name servers 

#now we have to check name servers that present in authoritative name server

def findMissingNSAndStealthNS(Domain,parent):
    stealthNameServers = []
    missingNameServers = []
    try:
        NameServerFromParent = getDomainNameServerFromParent(Domain,parent)
        for ns in NameServerFromParent:
            listNameServerUsingAuthoritative = getDomainNameServerFromAuthoritative(Domain,ns)
            for AuthoritativeNS in listNameServerUsingAuthoritative:
                if AuthoritativeNS not in NameServerFromParent:
                    stealthNameServers.append(AuthoritativeNS+ " at " + ns)

            for parentNs in NameServerFromParent:
                if parentNs not in listNameServerUsingAuthoritative:
                    missingNameServers.append(parentNs+" isn't listed at "+ns)
        return stealthNameServers , missingNameServers
    except:
        return stealthNameServers , missingNameServers

""" Missing Name servers and Stealth Name servers ---------------------End----------------------- """


""" Glue check------------------Start-----------------------"""
def GluefromNS(Domain,parent):
    gluerecords = []
    cmd="dig NS "+Domain+" @"+parent+" +noall +additional"
    try:
        output = os.popen(cmd).read()
        if output.find("connection timed out")!=-1:
            return gluerecords
        output= output.split('\n')
        output.pop()
        for record in output:
            gluerecords.append(record.split('\t').pop())
        #print("gluerecords: ",gluerecords)
        return gluerecords
    except Exception as e:
        print(e.args)
        return gluerecords

def CheckGlue(Domain,NS_records,parent):
    GlueNotFound = []
    try:
        gluerecords=GluefromNS(Domain,parent)
        gluerecords.sort()
        for ns in NS_records:
            gluerecordsbyns =GluefromNS(Domain,ns)
            gluerecordsbyns.sort()
            if((gluerecords==gluerecordsbyns)==False):
                GlueNotFound.append(ns)
        return GlueNotFound
    except Exception as e:
        print(e.args)
        return GlueNotFound
def CheckCustomNS(Domain,NS_records):
    try:
        CountNSContainfld=0
        for ns in NS_records:
            if get_fld("https://"+ns).lower()==Domain.lower():
                CountNSContainfld+=1
        return len(NS_records)==CountNSContainfld 
    except:
        return False
""" Glue check------------------End-----------------------"""


""" Lame NS ---------------------Start------------------------"""

def CheckNSReturnARecord(ns):
    try:
        result = dns.resolver.resolve(ns, 'A')
        return True
    except Exception as e :
        print(e.args)
        return False

def CheckLame(NS_record):
    LameNSList = []
    try:
        for ns in NS_record:
            if CheckNSReturnARecord(ns)==False :
                LameNSList.append(ns)
        return LameNSList
    except Exception as e :
        print(e.args)
        return LameNSList

""" Lame NS ----------------------End--------------------------"""


def ExtractData(Domain):
    Domain=Domain
    try:
        res = get_tld("https://"+Domain)
    except Exception as e:
        print(e)
        return {"Proper domain needed " , e.args}
    
    parent = getParentNameServer(res)
    #print("parent: ",parent)
    NS_records = []
    try:
        for i in range(5):
            NS_records=getDomainNameServerFromParent(Domain,parent)
            #print("NS_records: ",NS_records)      
            #print(type(NS_records))
            parent = getParentNameServer(res)
            if len(NS_records)!=0:
                break
    except Exception as e:
        print("Exception: ",e.args)
        pass
    if len(NS_records)==0:
        return "Parent NS records not found. Try again with a Proper Domain"
    
    CnameList = checkCNAME(NS_records)
    # print("Cname " ,CnameList)
    
    recursive_allow = findRecursive(NS_records,Domain)
    # print("Recursive ",recursive_allow)

    IdenticalNS=CheckIdenticalNsRecord(NS_records)
    # print("Identical Nameservers ",diffrent_ns)
    
    
    InvalidNS=validNS(NS_records)
    # print("Valid Ns ",InvalidNS)
    
    # print("Missing and stealth")
    stealthNameServers,missingNameServers=findMissingNSAndStealthNS(Domain,parent)
    # print(stealthNameServers,missingNameServers)

    #Lame name servers 
    LameNSList=CheckLame(NS_records)

    data= {}
    data['No CNAME in NS records']=''
    data['Allow recursive queries']=''
    data['Identical NS records']=''
    data['Valid domain names']=''
    data['Stealth name servers']=''
    data['Missing name servers']=''
    data['LAME name servers']=''

    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if len(CnameList)==0:
        subdict['Status']='Ok'
        subdict['Description']='No NS records with CNAME found.'
        subdict['moreInfo']= [{"More Info":"Name servers should map directly to one or more address records (A or AAAA records) and should not be pointing to CNAME records. Please refer to RFC 2181 : https://www.ietf.org/rfc/rfc2181.txt for additional information. "}] 
        data['No CNAME in NS records']=subdict
    else:
        subdict['Status']='Failed'
        subdict['Description']= 'NS records with CNAME found. Name servers should map directly to one or more address records (A or AAAA records) and should not be pointing to CNAME records. If a name appears in the right-hand side of RR (Resource Record) it should not appear in the left-hand name. Please refer to RFC 2181 : https://www.ietf.org/rfc/rfc2181.txt for additional information. '
        subdict['moreInfo']= [{"NS Records":i} for i in CnameList] 
        data['No CNAME in NS records']=subdict
    
    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if len(recursive_allow)==0:
        subdict['Status']='Ok'
        subdict['Description']="Name Servers don't allow recursive queries."
        subdict['moreInfo']= [{"More Info":"The Name servers don't allow recursive queries which is a good configuration for the Authoritative Name servers."}]
        data['Allow recursive queries']=subdict
    else:
        subdict['Status']='Failed'
        subdict['Description']='Found Name Servers that allow recursive queries. Recursive queries involves name resolution from both inside and outside of the network which is a security risk and RA flag should not be set in the Name server configuration.'
        subdict['moreInfo']= [{"NS Records":i} for i in recursive_allow] 
        data['Allow recursive queries']=subdict
    
    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if len(IdenticalNS)==0:
        subdict['Status']='Ok'
        subdict['Description']='All Name Servers returned identical NS records.'
        subdict['moreInfo']= [{"More Info": "All the Authoritative Name servers are configured with identical Name servers and it is a good practise to have DNS records configured correctly with authentic Name servers."}]
        data['Identical NS records']=subdict
    else:
        subdict['Status']='Failed'
        subdict['Description']="Found Name servers that do not have identical Name server records. Please validate if there is no Rogue Name server is active. Also, if the Authoritative Name servers do not possess identical Name servers records, more likely some of the visitors won't be able to see the site."
        subdict['moreInfo'] = [{"NS Records":i} for i in IdenticalNS] 
        data['Identical NS records']=subdict
    
    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if len(InvalidNS)==0:
        subdict['Status']='Ok'
        subdict['Description']='All Name Servers have valid domain names.'
        subdict['moreInfo']= [{"More Info": "It is recommended to have valid domain names for the Name servers, please refer to RFC 1123 : https://www.rfc-editor.org/rfc/rfc1123.html. for additional information."}]
        data['Valid domain names']=subdict
    else:
        subdict['Status']='Failed'
        subdict['Description']="Found Name servers that do not have valid domain names. Hostnames for Authoritative Name servers must comply with the requirements specified in RFC 1123 : https://www.rfc-editor.org/rfc/rfc1123.html."
        subdict['moreInfo'] =  [{"NS Records":i} for i in InvalidNS] 
        data['Valid domain names']=subdict
    
    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if len(stealthNameServers)==0:
        subdict['Status']='Ok'
        subdict['Description']='All Name Servers listed by parent Name Servers are listed by the authoritative ones as well.'
        subdict['moreInfo']= [{"More Info": "Stealth name servers (or hidden name servers) are present on the authoritative name servers, but not listed by the parent ones. Please refer to RFC 7719 : https://www.ietf.org/rfc/rfc7719.txt for additional information."}]
        data['Stealth name servers']=subdict
    else:
        subdict['Status']='Failed'
        subdict['Description']='Found Name Servers which are listed by the authoritative servers, but not by the parent ones. Stealth name servers (or hidden name servers) are present on the authoritative name servers, but not listed by the parent ones. Please refer to RFC 7719 : https://www.ietf.org/rfc/rfc7719.txt for additional information.'
        subdict['moreInfo'] = [{"NS Records":i} for i in stealthNameServers] 
        data['Stealth name servers']=subdict

    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if len(missingNameServers)==0:
        subdict['Status']='Ok'
        subdict['Description']='All Name servers possess list of Authoritative Name servers. This is a good practise.'
        subdict['moreInfo']= [{"NS Records": i} for i in NS_records]
        data['Missing name servers']=subdict
    else:
        subdict['Status']='Failed'
        subdict['Description']='Found Name Servers which are not listed by the authoritative Name Servers. Name Server configuration should be correctly done to avoid DNS related attacks.'
        subdict['moreInfo'] = [{"NS Records":i} for i in missingNameServers] 
        data['Missing name servers']=subdict

    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if len(LameNSList)>0:
        subdict['Status']='Failed'
        subdict['Description']="Found Name servers do not have A records configured. Please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ for additional information." 
        subdict['moreInfo'] = [{"NS Records":i} for i in LameNSList] 
        data['LAME name servers']=subdict
    else:
        subdict['Status']='Ok'
        subdict['Description']='All the Authoritative Name servers are configured with A records. A  Name server which gives a non-authoritative answer is called lame.'
        subdict['moreInfo']= [{"NS Records": i} for i in NS_records]
        data['LAME name servers']=subdict
    
    #if your name server contain your domain ie custom name server 
    #example google.com have ns1.google.com as one of the name servers.
    subdict = {}
    subdict['Status']=''
    subdict['Description']=''
    subdict['moreInfo']= [{"NS Records": ""}]
    if CheckCustomNS(Domain,NS_records):
        GlueNotfound = CheckGlue(Domain,NS_records,parent)
        if len(GlueNotfound)==0:
            subdict['Status']='Ok'
            subdict['Description']="Glue is required and provided."
            subdict['moreInfo']= [{"More Info":"Glue records are required when configuration of domain's Name servers is to be done for a hostname which is a subdomain of the domain itself."}]
            data['Glue check']=subdict
        else:
            subdict['Status']='Failed'
            subdict['Description']='Glue is required, but not provided. No IPv4/IPv6 glue found on the authoritative or parent Name Servers'
            subdict['moreInfo'] = [{"NS Records":i} for i in GlueNotfound]
            data['Glue check']=subdict
    else:
        subdict['Status']='Skipped'
        subdict['Description']='Glue is not required.'
        subdict['moreInfo']= [{"More Info":"Glue records are required when configuration of domain's Name servers is to be done for a hostname which is a subdomain of the domain itself."}]
        data['Glue check']=subdict

    payload_new = []
    for k,v in data.items():
        x = {"TestName": k}
        payload_new.append(x)
    
    payload_new[0].update(data["No CNAME in NS records"])
    payload_new[1].update(data["Allow recursive queries"])
    payload_new[2].update(data["Identical NS records"])
    payload_new[3].update(data["Valid domain names"])
    payload_new[4].update(data["Stealth name servers"])
    payload_new[5].update(data["Missing name servers"])
    payload_new[6].update(data["LAME name servers"])
    payload_new[7].update(data["Glue check"])




    CompleteData={}
    CompleteData["Domain"]=Domain
    CompleteData["TestResult"]=payload_new
    return CompleteData


def CheckAllTest(domain):
    try:
        data = ExtractData(domain)
        return data
    except Exception as e:
        print(e.args)
        return {"Details":"Pass Proper domain with tld Example google.com"}

# if __name__ == '__main__':
#     domain = sys.argv[1]
#     print(CheckAllTest(domain))
