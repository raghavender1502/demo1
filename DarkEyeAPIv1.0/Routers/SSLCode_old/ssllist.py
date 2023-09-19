#from logging.config import valid_ident
import requests
from datetime import datetime
import sys
import logging
from .sslpurposes import get_data_sslpurpose
from ocspchecker import ocspchecker          #pip install ocsp-checker
from .check_TLSA_dane import get_details
#from .sslyzer_script import sslyze_scan
import time

API = 'https://api.ssllabs.com/api/v3/'

def requestAPI(path, payload={}):
    '''This is a helper method that takes the path to the relevant
        API call and the user-defined payload and requests the
        data/server test from Qualys SSL Labs.
        Returns JSON formatted data'''
    url = API + path
    try:
        response = requests.get(url, params=payload)
    except requests.exception.RequestException:
        logging.exception('Request failed.')
        sys.exit(1)
    data = response.json()
    return data

def newScan(host, publish='off', startNew='on', all='done', ignoreMismatch='on'):
    t1 = time.time()
    path = 'analyze'
    payload = {
                'host': host,
                'publish': publish,
                'startNew': startNew,
                'all': all,
                'ignoreMismatch': ignoreMismatch
              }
    results = requestAPI(path, payload)

    payload.pop('startNew')
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    while results['status'] != 'READY' and results['status'] != 'ERROR':
        time.sleep(15)
        results = requestAPI(path, payload)
        with open("/app/SSL_log_file_"+host[:-4]+"_"+timestamp+".log", "a") as f:
            print("DEBUG: ",results, file=f)
            print("\n**********************\n", file=f)

    ssllist_main = [] 
    ssllists = []
    threats = []
    #print(results)    # complete ssllabs response
    for certs in results["certs"]:
        try:
            commonNames = certs["commonNames"][0]
        except:
            commonNames = ""
        
        try:
            validfrom = certs["notBefore"]
            validfrom = str(datetime.fromtimestamp(validfrom/1000))
            validfrom_status = "Ok"
            #print(validfrom)
        except:
            validfrom = ""
            validfrom_status = "Failed"
        
        try:
            validuntil = certs["notAfter"]  
            validuntil = str(datetime.fromtimestamp(validuntil/1000))
            validuntil_status = "Ok"
        except:
            validuntil = ""
            validuntil_status = "Ok"          
        
        try:
            iss_by_cn = certs["issuerSubject"].split(",")[0][3:]
        except:
            iss_by_cn = ""
            
        try:
            iss_by_c = certs["issuerSubject"].split(",")[-1][3:]      
        except:
            iss_by_c = ""
            

            # "CN=RapidSSL TLS DV RSA Mixed SHA256 2020 CA-1, O=DigiCert Inc, C=US"
        #iss = []    
        iss_by_o = certs["issuerSubject"].split(",")
        #print("ISS List****", iss_by_o)
        for org in iss_by_o:
            if org.startswith(" O="):
                iss_by_o = org.split("=")[1]
                
                #iss.append(i[3:])
                #print(iss_by_o)
                break
            else:
                iss_by_o = ""
                #iss = []    
        #print(iss_by_o)

        
            # "CN=*.adani.com"
        subj = []    
        subject = certs["subject"].split(",")
        #print("Subj list ****",subject)
        for p in subject:
            if p.startswith(" O=")==True :
                subj.append(p[3:])
                #print(subject)
            else:
                subject = []
        
        
        
        if len(subj)==0 :
                valtype = "Domain Validated"
        else:
            valtype = "Organization Validated"          
        
        
        try:
            sigalg = certs["sigAlg"]+"Encryption"
        except:
            sigalg = ""   
            
        try:
            srnum = certs["serialNumber"]
        except:
            srnum = ""         
        
        try:
            publickeysizetype = certs["keyAlg"] +" "+ str(certs["keySize"])
        except:
            publickeysizetype = ""    
        
        try:
            crlurl = certs["crlURIs"][0]
            crl_status = "Ok"
            crl_des = "The certificate's not present in the CRL provided by the certificates' issuer."
        except:
            crlurl = "No CRL endpoints available"
            crl_status=  "Skip"
            crl_des = "The CRL endpoints not found in the certificate's extensions. Test skipped."
                          
  
        
        try:    
            payload = {
                "commonName"          : commonNames,
                "validfrom"            : {"date":validfrom,"status": validfrom_status},
                "validuntil"           : {"date":validuntil,"status": validuntil_status}, 
                "issuedBy"             : {
                    "CommonName"       : iss_by_cn,
                    "Country"          : iss_by_c,
                    "Organization"     : iss_by_o,  
                },
                "validationtype"       : valtype,
                "signaturealogirithm"  : sigalg,
                "allowedpurposes"      : get_data_sslpurpose(host),
                "serialnumber"         : srnum,
                "publickeysizetype"    : publickeysizetype, 
                "CRL_check"            : {
                    "CRL_URL"          : crlurl,
                    "CRL_status"       : crl_status,
                    "CRL_description"  : crl_des,
                },
                           
            } 
            ssllists.append(payload)
            ssllists[0]["certificatechain"] = "end-user"
            ssllists[-1]["certificatechain"] = "root"
            try:
                for w in ssllists[1:-1]:
                    w["certificatechain"]  = "intermediate" 
            except:
                pass  
               
        except:
            ssllists = {} 
            
    ssllist_main.append(ssllists)
    if len(ssllist_main) == 0:

        sslcertconfig = {

            "Details": "SSL certificate is not configured",

            "Status": "Warning"

        }

    else:

        sslcertconfig = {
            "Details": "Ok",
            "Status": "Ok"
        }    
        
    ocsp_request = ocspchecker.get_ocsp_status(host) 
    OCSP_check= {
               "Details": ocsp_request[1].split(":",1)[1],
               "Status": ocsp_request[2].split(":")[1]
           }
    if OCSP_check["Status"] == " GOOD":
       OCSP_check.update({"Status" : "Ok"})
     
    if host in results["certs"][0]["altNames"]:
        host_valid = str(host) + " found in Subject Alternative Names"
        tag_valid = "Ok"
        des_valid = "The domain name matches one of the certificate's Subject Alternative Names (SAN)."
    elif host in certs["commonNames"]:
        host_valid = str(host) + " found in Common Name"
        tag_valid = "Ok"  
        des_valid = "The domain name matches the certificate's Common Name (CN) field."
    else:
        host_valid = str(host) + " does not match the certificate"
        tag_valid = "Failed"
        des_valid = "The domain name is not referenced in Common Name (CN) neither Subject Alternative Names (SAN) certificate's fields. The certificate can't be used for the target website."         
    
    hostname_valid = {
        
            "Details": host_valid,
            "Status": tag_valid,
            "Description": des_valid
        
    }
    #sllist_main.append(hostname_valid)
    
    protocols = results["endpoints"][0]["details"]["protocols"] 
    supported= []
    for pro in protocols:
        supported.append(pro["name"]+"v"+pro["version"]+" is supported")
    
    if len(supported)==0:
        supported_proto = {
        "Details":'No supported protocol found',
        "Status":'Warning'
        }
    else:
        
        supported_proto = {
        "Details":'Your server supports protocols :' +str(supported)[1:-1],
        "Status":"Ok"
        }
        
    my_cipher_list= []

    try:
        suits = results["endpoints"][0]["details"]["suites"]
        for x in suits:
            for y in x["list"]:
                #print(y["name"])
                my_cipher_list.append(y["name"])
                
        #print(my_cipher_list)
        if len(my_cipher_list) == 0:
            cipher_response = {
                "Details" : "No suboptimal cipher suites found.",
                "Status": "Ok",
                "Description": "Host does not support suboptimal cipher suites."
            } 
        else:
            cipher_response = {
                "Field":"Supported Cipher Suites",
                "Details" : "Your server supports suboptimal cipher suites: "+str(my_cipher_list)[1:-1],
                "Status": "Warning",
                "Description": "It's not recommended to support suboptimal cipher suites: " +str(my_cipher_list)[1:-1],  
            } 
            threats.append(cipher_response)          
    except:
        cipher_response = {
                "Details" : "No suboptimal cipher suites found.",
                "Status": "Ok",
                "Description": "Host does not support suboptimal cipher suites."
            }
    
    try:
        hpkpe = results['endpoints'][0]["details"]["hpkpPolicy"]
        if hpkpe["status"] == "absent":
            hpkpe_response = {
                "Details": "Headers not set",
                "Status": "Ok",
                "Description" : "Host's response does not contain HPKP headers (Public-Keys-Pins, Public-Keys-Pins-Report-Only)"
            }
        else:
            hpkpe_response = {
                "Field":"HTTP Public Key Pinning Extension",
                "Details": "Headers set",
                "Status": "Warning" ,
                "Description": "Host's response contains HPKP headers. Configuration meets recommendations."
            }  
            threats.append(hpkpe_response)
    except:
        hpkpe_response = {
                "Details": "Headers not set",
                "Status": "Ok",
                "Description" : "Host's response does not contain HPKP headers (Public-Keys-Pins, Public-Keys-Pins-Report-Only)"
                
            }
    
    try: 
        http = results["endpoints"][0]["details"]["hstsPolicy"]["status"]
        if http == "absent":
            http_response = {
                "Field":"Force HTTPS Connections",
                "Details": "No",
                "Status": "Warning",
                "Description": "HSTS headers are not set. HTTPs protocol is not forced. To protect against protocol downgrade attacks and cookie hijacking it's recommended to configure HSTS headers."
            }
            threats.append(http_response)  
        else:
            http_response = {
                "Details": "Yes",
                "Status": "Ok",
                "Description": "HSTS header is set. HTTPs protocol is forced. Configuration meets best practises."
            } 
    except:
        http_response = {
                "Details": "Yes",
                "Status": "Ok",
                "Description": "HSTS header is set. HTTPs protocol is forced. Configuration meets best practises."
                
            }
    
    try:
        fallback = results["endpoints"][0]["details"]["protocols"]
        if len(fallback) == 0:
            fallback_response = {
                "Field":"TLS_FALLBACK_SCSV supported",
                "Details": "No",
                "Status": "Failed",
                "Description": "It's recommended to enable TLS_FALLBACK_SCSV to protect against POODLE attacks."
            }
            threats.append(fallback_response)
        elif len(fallback) == 1:
            fallback_response = {
                "Field":"TLS_FALLBACK_SCSV supported",
                "Details": "Only 1 protocol supported",
                "Status": "Warning",
                "Description": "The server supports only 1 protocol. Fallback isn't possible."
            }
            threats.append(fallback_response)
        else:
            fallback_response = {
                "Details": "Yes",
                "Status": "Ok",
                "Description": "TLS_FALLBACK_SCSV is supported by the host. Configuration meets recommendations."
            }        
    except:
        fallback_response = {
                "Field":"TLS_FALLBACK_SCSV supported",
                "Details": "No",
                "Status": "Failed",
                "Description": "It's recommended to enable TLS_FALLBACK_SCSV to protect against POODLE attacks."
            }
        threats.append(fallback_response)
    
    try:
        debian = results['certs']
        if "keyKnownDebianInsecure" in debian:
            if debian["keyKnownDebianInsecure"]== False:
                debian_response = {
                    "Details": "Ok",
                    "Status": "Ok",
                    "Description": "The certificate's public key is not present in the Debian blacklist."
                }
            else:
                debian_response = {
                    "Field":"Debian blacklist check",
                    "Details": "The certificate's public key is present in the Debian blacklist.",
                    "Status": "Failed",
                    "Description": "The certificate's public key is present in the Debian blacklist."
                }   
                threats.append(debian_response) 
        else:
            debian_response = {
                "Details": "Ok",
                "Status": "Ok",
                "Description": "The certificate's public key is not present in the Debian blacklist."
            }      
    except:
        debian_response = {
                "Details": "Ok",
                "Status": "Ok",
                "Description": "The certificate's public key is not present in the Debian blacklist."
            }
    
    try:    
        stapling = results['endpoints'][0]["details"]["ocspStapling"]    
        if stapling == False:
            stapling_response = {
                "Field":"OCSP stapling enabled",
                "Details": "No",
                "Status": "Warning",
                "Description": "Host doesn't support OCSP stapling."
            }
            threats.append(stapling_response)
        else:
            stapling_response = {
                "Details": "Certificate status: ok",
                "Status": "Ok",
                "Description": "Host supports OCSP stapling."
            }       
    except:
        stapling_response = {
                "Details": "Certificate status: ok",
                "Status": "Ok",
                "Description": "Host supports OCSP stapling."
            }    
    try:
        if results["certs"][0]["subject"].split(",")[0].split("CN=")[1] == results["certs"][0]["issuerSubject"].split(",")[0].split("CN=")[1]:
            Self_signed_cert = {
                "Field":"Self-signed certificate",
                "Details" : "Self-signed certificate.",
                "Status": "Failed",
                "Description": "The certificate is self-signed. Issuer matches the subject."
            }
            threats.append(Self_signed_cert)
            
        else:
            Self_signed_cert = {
                "Details" : "CA-signed certificate.",
                "Status": "Ok",
                "Description": "The certificate is signed by a Certificate Authority. Issuer does not match the subject."
            }
    except:
        Self_signed_cert = {
                "Details" : "CA-signed certificate.",
                "Status": "Ok",
                "Description": "The certificate is signed by a Certificate Authority. Issuer does not match the subject."
            }
    
    # poodle
    
    try: 
        poodle = results["endpoints"][0]["details"]["poodle"]
        if poodle == False:
            poodle_response = {
                "Field":"Vulnerable to Poodle attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": "Confidential data that is transmitted, for example, passwords or session cookies are secure."
            }
              
        else:
            poodle_response = {
                "Field":"Vulnerable to Poodle attack",
                "Details": "Yes",
                "Status": "Warning",
                "Description": "Confidential data that is transmitted, for example, passwords or session cookies are vulnerable to poodle attack."
            }
            threats.append(poodle_response) 
    except:
        poodle_response = {
                "Field":"Vulnerable to Poodle attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": "Confidential data that is transmitted, for example, passwords or session cookies are secure."
            } 
        
    # freak
    
    try: 
        freak = results["endpoints"][0]["details"]["freak"]
        if freak == False:
            freak_response = {
                "Field":"Vulnerable to Freak attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            }
              
        else:
            freak_response = {
                "Field":"Vulnerable to Freak attack",
                "Details": "Yes",
                "Status": "Warning",
                "Description": "There is a cryptographic weakness in SSL/TLS which may invite Freak attack."
            }
            threats.append(freak_response) 
    except:
        freak_response = {
                "Field":"Vulnerable to Freak attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            }
    
    # logjam
    
    try: 
        logjam = results["endpoints"][0]["details"]["logjam"]
        if logjam == False:
            logjam_response = {
                "Field":"Vulnerable to Logjam attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            }
              
        else:
            logjam_response = {
                "Field":"Vulnerable to Logjam attack",
                "Details": "Yes",
                "Status": "Warning",
                "Description": "Website is found to support DH(E) export cipher suites, or non-export DHE cipher suites using either DH primes smaller than 1024 bits, or commonly used DH standard primes up to 1024 bits which may invite Logjam attack."
            }
            threats.append(logjam_response) 
    except:
        logjam_response = {
                "Field":"Vulnerable to Logjam attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            }
    
    # drown 
    
    try: 
        drown = results["endpoints"][0]["details"]["drown"]
        if drown == False:
            drown_response = {
                "Field":"Vulnerable to Drown attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            }
              
        else:
            drown_response = {
                "Field":"Vulnerable to Drown attack",
                "Details": "Yes",
                "Status": "Warning",
                "Description": "HTTPS and other services that rely on SSL and TLS, some of the essential cryptographic protocols for Internet security may be affected."
            }
            threats.append(drown_response) 
    except:
        drown_response = {
                "Field":"Vulnerable to Drown attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            } 
    
    # ticketbleed
    
    try: 
        ticketbleed = results["endpoints"][0]["details"]["ticketbleed"]
        if ticketbleed == 1:
            ticketbleed_response = {
                "Field":"Vulnerable to Ticketbleed attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            }
              
        else:
            ticketbleed_response = {
                "Field":"Vulnerable to Ticketbleed attack",
                "Details": "Yes",
                "Status": "Warning",
                "Description": "The possibility of exposing sensitive information that could compromise HTTPS connection is High."
            }
            threats.append(ticketbleed_response) 
    except:
        ticketbleed_response = {
                "Field":"Vulnerable to Ticketbleed attack",
                "Details": "No",
                "Status": "Ok",
                #"Description": ""
            } 
    
    try:
        grade = results["endpoints"][0]["grade"]
    except:
        grade = []
    
    try:
        talsadata=get_details(host)
    except:
        talsadata="NA"
    if talsadata!="NA":
        talsadatathrets={"Field":"TLSA DNS record configuration"}
        talsadatathrets.update(talsadata["SSL Threats"][0])
        threats.append(talsadatathrets)
    
    # sslyzer = sslyze_scan(host)
    # heartbleed = sslyzer["Response"]["Heartbleed vulnerability check"]
    # if heartbleed["Status"] == "Failed":
    #     threats.append(heartbleed) 
    
    # compression = sslyzer["Response"]["SSL compression"] 
    # if compression["Status"] == "Failed":
    #     threats.append(compression) 
    
        
    valid_from_details =  {
            "Details": "Valid from " + str(ssllists[0]["validfrom"]["date"]),
            "Status": ssllists[0]["validfrom"]["status"]
        } 
    
    valid_until_details = {
            "Details": "Valid to " + str(ssllists[0]["validuntil"]["date"]),
            "Status": ssllists[0]["validuntil"]["status"]
        }
     
    final_payload = {
        "domain": host,
        "Grade": grade,
        "ssl_lists"               : ssllists,
        "sslCertificateConfigured": sslcertconfig,
        "ocsp_check"             : OCSP_check,
        "hostname_validation"     : hostname_valid,
        "self_signed_certificate": Self_signed_cert,
        "supported_protocols"     : supported_proto,
        "supported_cipher_suites" : cipher_response,
        "http_public_key_pinning_extension": hpkpe_response,
        "force_https_connections": http_response,
        "tls_fallback_scsv_supported": fallback_response,
        "debian_blacklist_check": debian_response,
        "ocsp_stapling_enabled": stapling_response,
        # "heartbleed_vulnerability_check" : heartbleed,
        # "ssl_compression"          : compression,
        "vulnerable_to_poodle_attacks": poodle_response,
        "vulnerable_to_freak_attacks": freak_response,
        "vulnerable_to_logjam_attacks": logjam_response,
        "vulnerable_to_drown_attacks": drown_response,
        "vulnerable_to_ticketbleed_attacks": ticketbleed_response,
        "tlsa_dns_records_configuration":talsadata["TLSA DNS record configuration"],
        "ssl_threats": threats,
        "valid_from_details": valid_from_details,
        "valid_until_details": valid_until_details,
        "executionTime": time.time() - t1,
        "extSource": "SSLlabs API"    
    }
    
    return final_payload            
      
