import sslyze
import json

def sslyze_scan(host):
    try:
        all_scan_requests = [
            sslyze.ServerScanRequest(server_location=sslyze.ServerNetworkLocation(hostname=host))
            ]
    except sslyze.ServerHostnameCouldNotBeResolved:
        
        print("Error resolving the supplied hostnames")
        pass

    scanner = sslyze.Scanner()
    scanner.queue_scans(all_scan_requests)

    
    for server_scan_result in scanner.get_results():
        
        if server_scan_result.scan_status == sslyze.ServerScanStatusEnum.ERROR_NO_CONNECTIVITY:
            
            continue
        
        assert server_scan_result.scan_result
        
        threats = []
        heartbleed =   server_scan_result.scan_result.heartbleed
        heartbleed_result = heartbleed.result
        assert heartbleed_result
        
        if  str(heartbleed_result).split("=")[1][:-1] == "False":
            heart = {"Details": "Ok",
                    "Status": "Ok",
                    "Description": "OpenSSL installed on the host is fixed against Heartbleed vulnerability."
                    }
        else:
            heart = {"Details": "The host is vulnerable. OpenSSL should be updated.",
                    "Status": "Failed",
                    "Description": "The host has the vulnerable OpenSSL version installed. Should be updated."
                    }       
            threats.append(heart)
        
        compression = server_scan_result.scan_result.tls_compression
        compression_result = compression.result
        assert compression_result
        
        if  str(compression_result).split("=")[1][:-1] == "False":
            comp = {"Details":"Disabled",
                    "Status": "Ok",
                    "Description": "Configuration is correct."
                    }
        else:
            comp = {"Details":"Enabled",
                    "Status": "Failed",
                    "Description": "SSL connection compression is enabled by the host. It's recommended to disable it to protect against BREACH attacks."}   
            threats.append(comp)
            
        payload = {
            "Domain": host,
            "Response": {
            "SSL compression": comp,
            "Heartbleed vulnerability check": heart,},
            "SSL Threats": threats,
        }   
        
        return payload


