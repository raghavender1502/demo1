import dns.resolver
import json
import requests 
import os
from dotenv import load_dotenv

def soaHackertarget(target):
    load_dotenv()
    apikey = os.getenv("HackerTargetAPIKEY")
    
    if len(apikey) == 0:
        response = requests.get("https://api.hackertarget.com/dnslookup/?q={}".format(target))
    else:
        response = requests.get("https://api.hackertarget.com/dnslookup/?q={}&apikey={}".format(target,apikey))
    r = response.text
    p = r.split('\n')
    SOA = []
    for item in p:
        if item.startswith('SOA'):
            SOA.append(item[6:])
    # return SOA
    return p

#   ['dns1.p02.nsone.net. hostmaster.nsone.net. 1645034807 43200 7200 1209600 3600']
def soaConfig(target):
    SOA = []
    
    # Implementation using dns.resolver python module
    for x_soa in dns.resolver.resolve(target, 'SOA'):     
        x_soa = x_soa.to_text()
        SOA.append(x_soa)
    
    # if dns resolver module fails to get the SOA records, use the hackertarget API
    if len(SOA) == 0:
        SOA = soaHackertarget(target)

    # if SOA records could not be found by dns resolver and hackertarget API both
    if len(SOA) == 0:
        payload = {
        "Domain": target,
        "TestResult": [
            {
            "TestName": "SOA Config Check",
            "Status": "Skipped",
            "Description": "We are unable to find SOA records for the domain {} at this moment.".format(target)
            }
        ]
    }
        return payload    

              
     
    
    # Row 1   
    Primary_name_server = SOA[0].split()[2]
    data = {
            "TestName":'Name servers agreement on serial number',
            'Status':'',
            'Description':''
        }
    data['moreInfo']= [{"More Info":"For all name servers to be up to date with the current version of your zone, they must have the same SOA serial number. "+str(Primary_name_server)}]
    if (type(Primary_name_server)) != list:
        data['Status'] = 'Ok'
        data['Description']= f'All name servers have the same serial number: {Primary_name_server}'

    else:
        data['Status'] = 'Failed'
        data['Description']= f'Some name servers have different serial numbers: {Primary_name_server}'    
        
    #print(data)  
    #print(Primary_name_server[0:4])
    #Row 2
    data1 = {
            "TestName":'Serial number format',
            'Status':'',
            'Description':''
        }
    if ((1900 <= int(Primary_name_server[0:4]) <=2050) and   #year
        (1 <= int(Primary_name_server[4:6]) <=12) and        #month
        (1 <= int(Primary_name_server[6:8]) <=31)):          #day
        data1['Status'] = "Ok"
        data1['Description'] = "The serial number format meets the general convention."
        data1['moreInfo']= [{"More Info":"The serial number is an unsigned 32 bit value assigned to your SOA record and is a representation of your DNS zone's version. It must be between 1 and 4294967295. Recommended Serial number format uses 10 digits to represent the date and then a two digit sequence number with the format of YYYYmmddss. "}]
    else:
        data1['Status'] = "Warning"
        data1['Description'] = f"Although the serial number is valid, it's not following the general convention: {Primary_name_server}"
        data1['moreInfo']= [{"More Info":"The serial number is an unsigned 32 bit value assigned to your SOA record and is a representation of your DNS zone's version. It must be between 1 and 4294967295. Recommended Serial number format uses 10 digits to represent the date and then a two digit sequence number with the format of YYYYmmddss. Check if your serial is either invalid by being outside of the allowed range or if it does not conform to this format. "}]      
    
    #print(data1)  
      
    #Row 3
    RNAME = SOA[0].split()[1]
    #print(RNAME)
    data2 = {
        "TestName":'RNAME',
        'Status':'',
        'Description':''
    }
    if RNAME != 'null':
        data2['Status'] = 'Ok'
        data2['Description']= f"Zone's administrative contact email is {RNAME}."
        data2['moreInfo']= [{"More Info":"The 'RNAME' value here represents the administrator's email address with '@' being replaced by '.'."+str(RNAME)}]
    else:
        data2['Status'] = 'Failed'
        data2['Description']= "Zone's administrative contact email is not set."
        data2['moreInfo']= [{"More Info":" For smooth administration, please set the zone's administrative contact email in SOA records."+str(RNAME)}]    
             
    #Row 4
    Refresh  = int(SOA[0].split()[3]) 
    data3 = {
        "TestName":'Refresh',
        'Status':'',
        'Description':''
    }
    if 1200 <= Refresh <= 43200:
        data3['Status'] = 'Ok'
        data3['Description']= "The value is within the recommended range. Recommended range is [1200 .. 43200]."
        data3['moreInfo']= [{"More Info":"This is the number of seconds between update requests from secondary and slave name servers. The recommended range is between [1200,43200]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ; Current value is: "+str(Refresh)}]
    else:
        data3['Status'] = 'Warning'
        data3['Description']= f"The refresh interval is {Refresh}. Recommended range is [1200 .. 43200]."
        data3['moreInfo']= [{"More Info":"This is the number of seconds between update requests from secondary and slave name servers. The recommended range is between [1200,43200]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ; Current value is: "+str(Refresh)}]

    #Row 5
    Retry = int(SOA[0].split()[4])
    #print(Retry)
    data4 = {
        "TestName": 'Retry',
        'Status':'',
        'Description':''
    }
    if 600 <= Retry <= 3600:
        data4['Status'] = 'Ok'
        data4['Description']= "The value is within the recommended range. Recommended range is [600 .. 3600]."
        data4['moreInfo']= [{"More Info":"This is the number of seconds the secondary or slave will wait before retrying when the last attempt has failed. The recommended range is between [600, 3600]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ; Current value is : "+str(Retry)}]
    else:
        data4['Status'] = 'Warning'
        data4['Description']= f"The retry interval is {Retry}. Recommended range is [600 .. 3600]."
        data4['moreInfo']= [{"More Info":"This is the number of seconds the secondary or slave will wait before retrying when the last attempt has failed. The recommended range is between [600, 3600]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ; Current value is : "+str(Retry)}]
  
    #Row 6
    Expire = int(SOA[0].split()[5])

    data5 = {
        "TestName": 'Expire',
        'Status':'',
        'Description':''
    }
    if 1209600 <= Expire <= 2419200:
        data5['Status'] = 'Ok'
        data5['Description']= "The value is within the recommended range. Recommended range is [1209600 .. 2419200]."
        data5['moreInfo']= [{"More Info":"This is the number of seconds a master or slave will wait before considering the data stale if it cannot reach the primary name server. The recommended range is between [1209600, 2419200]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ;  Current value is : "+str(Expire)}]
    else:
        data5['Status'] = 'Warning'
        data5['Description']= f"The expire interval is {Expire}. Recommended range is [1209600 .. 2419200]."
        data5['moreInfo']= [{"More Info":"This is the number of seconds a master or slave will wait before considering the data stale if it cannot reach the primary name server. The recommended range is between [1209600, 2419200]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ;  Current value is : "+str(Expire)}]
        
    #Row 7
    MinimumTTL = int(SOA[0].split()[6])

    data6 = {
        "TestName": 'Minimum TTL',
        'Status':'',
        'Description':''
    }
    if 3600 <= MinimumTTL <= 86400:
        data6['Status'] = 'Ok'
        data6['Description']= "The value is within the recommended range. Recommended range is [3600 .. 86400]."
        data6['moreInfo']= [{"More Info":"This is the default TTL in seconds if the domain does not specify a TTL, how long data will remain in other nameservers' cache.  The recommended range is between [3600, 86400]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ; Current value is : "+str(MinimumTTL)}]
    else:
        data6['Status'] = 'Warning'
        data6['Description']= f"The minimum TTL is {MinimumTTL}. Recommended range is [3600 .. 86400]."
        data6['moreInfo']= [{"More Info":"This is the default TTL in seconds if the domain does not specify a TTL, how long data will remain in other nameservers' cache.  The recommended range is between [3600, 86400]. For additional information, please refer to RFC 1912 https://datatracker.ietf.org/doc/rfc1912/ ; Current value is : "+str(MinimumTTL)}]

   
    payload = {
        "Domain": target,
        "TestResult": [
            data,data1,data2,data3,data4,data5,data6,
        ]
    }
    # payload=json.dumps(payload)
    #print(payload)
    return payload

