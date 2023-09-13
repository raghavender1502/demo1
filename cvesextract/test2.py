import requests

def get_cve_for_domain(domain):
    base_url = "https://services.nvd.nist.gov/rest/json/"
    search_url = f"{base_url}cves/1.0"
    
    # Prepare the query parameters
    params = {
        "keyword": domain,
        "isExactMatch": "true"
    }
    
    try:
        # Send the API request
        response = requests.get(search_url, params=params)
        
        if response.status_code == 200:
            # Extract the CVE data from the response
            cve_data = response.json()
            
            if "result" in cve_data and "CVE_Items" in cve_data["result"]:
                cve_items = cve_data["result"]["CVE_Items"]
                
                if cve_items:
                    print("CVEs for domain", domain, ":")
                    
                    # Print the CVE IDs and descriptions
                    for item in cve_items:
                        cve_id = item["cve"]["CVE_data_meta"]["ID"]
                        description = item["cve"]["description"]["description_data"][0]["value"]
                        print("CVE ID:", cve_id)
                        print("Description:", description)
                        print("---------------------")
                else:
                    print("No CVEs found for domain", domain)
            else:
                print("No CVE data found for domain", domain)
        else:
            print("Error:", response.status_code)
    
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# Example usage
get_cve_for_domain("tamu.edu")
