# from logging import warning
from .NsConfigurationBestPractice import ConfigurationCheck
from .NsConfigurationCheckScript import CheckAllTest
from .MxConfigurationCheck import mxconfigmain
from .SOAConfigCheck import soaConfig
from .NsRecordsValidationScript import get_test_results
import json

# from DnsThreats import NsConfigurationBestPractice


warningcodes = {}
warningcodes["Name servers count"]=1012
warningcodes["Distributed over multiple networks"]=1014
warningcodes["Distributed over multiple ASNs"]=1013
warningcodes["Versions are hidden"]=1015
warningcodes["No CNAME in NS records"]=1008
warningcodes["Allow recursive queries"]=1003
warningcodes["Identical NS records"]=1010
warningcodes["Valid domain names"]=1007
warningcodes["Stealth name servers"]=1005	
warningcodes["Missing name servers"]=1006
warningcodes["LAME name servers"]=1004
warningcodes["Glue check"]=1009
warningcodes["A records configured"]=5006
warningcodes["AAAA records configured"]=5007
warningcodes["IPs are public"]=5010
warningcodes["Mail servers are not present in CNAME records"]=5008
warningcodes["Exchange fields contain valid domain names"]=5009
warningcodes["Exchange fields don't contain IPs"]=5011
warningcodes["Name servers return identical MX records"]=5012
warningcodes["No duplicate MX records"]=5013
warningcodes["SPF"]=5015
warningcodes["DMARC"]=5016
warningcodes["Identical SPF and DMARC records"]=5017
warningcodes["Name servers agreement on serial number"]=1022
warningcodes["Serial number format"]=1018
warningcodes["RNAME"]=1025
warningcodes["Refresh"]=1023
warningcodes["Retry"]=1024
warningcodes["Expire"]=1019
warningcodes["Minimum TTL"]=1020
warningcodes["Name servers have A record"]=1016
warningcodes["Name servers have AAAA record"]=1017
warningcodes["All name servers responded"]=1002
warningcodes["All IPs are public"]=1001
warningcodes["TCP connections allowed"]=1011

def GetDnsThreats(domain):
    try:
        nscbp = ConfigurationCheck(domain)
        nscbp = nscbp["Test Results"]
    except:
        nscbp = []
    try:
        nscc = CheckAllTest(domain)
        print(nscc)
        print(type(nscc))
        nscc = nscc["TestResult"]
    except Exception as e:
        print("Error in NSConfigCheck: ",e)
        nscc = []   
    try:
        mxcc = mxconfigmain.getTestResults(domain)
        mxcc = mxcc["detailedResponse"]["testResults"]
    except:
        mxcc = []
    try:
        scc = soaConfig(domain)
        scc = scc["TestResult"]
    except:
        scc = []
    try:
        nsrv = get_test_results(domain)
        nsrv = nsrv["detailedResponse"]["testResults"]
    except:
        nsrv = []
    
    data = [
        {
            "TestName": "NsConfigurationBestPractices",
            "TestResult":nscbp
        },
        {
            "TestName": 'NsConfigurationCheck',
            "TestResult":nscc
        },
        {
            "TestName": 'MxConfigurationCheck',
            "TestResult":mxcc
        },
        {
            "TestName": "SoaConfigurationCheck",
            "TestResult":scc
        },
        {
            "TestName": "NsRecordsValidation",
            "TestResult":nsrv
        },
    ]
    # data['Domain']=domain
    return data

# def testData():
    
   
def test(domain):
    data = GetDnsThreats(domain)
    testResult = []
    mainData={}
    mainData["Domain"]=domain
    mainData["DnsTests"]=data

    for i in data:
        for y in i["TestResult"]:
            if y["Status"] == "Failed" or y["Status"] == "Warning":
                testResult.append(y)

    for w in testResult:
        try: 
            w["warningCodes"] = warningcodes[w["TestName"]]
        except:
            w["warningCodes"] = "NA"

    mainData["TestResult"]=testResult
    mainData["extSource"]="dns.resolver Python Module"
    return mainData
    
