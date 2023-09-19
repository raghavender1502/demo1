import dnstwist
#import argparse
import os
import json

# FUNCTION TO FIND TYPOSQUATTING / SIMILAR DOMAINS

def similarDomains(domain):
    try:
        cmd="dnstwist --registered --format json "+domain
        detail=os.popen(cmd).read()
        detail=json.loads(detail)
        
        data = {'Domain':domain,'Results':detail, "extSource": "dnstwist Python Module"}
    
    except:
        data = {'Domain':domain,'Results':"No records found", "extSource": "dnstwist Python Module"}
    
    #print(data)
    return data




