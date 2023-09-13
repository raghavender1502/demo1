import requests
import json

def search_cves(domain):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    search_url = f"{base_url}?keyword={domain}"

    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            json_response = response.json()
            # Extract the CVE information from the JSON response
            cve_items = json_response.get('result', {}).get('CVE_Items', [])
            for item in cve_items:
                cve_id = item.get('cve', {}).get('CVE_data_meta', {}).get('ID')
                print(f"CVE ID: {cve_id}")
                # Extract more information as needed

        else:
            print("Failed to retrieve CVE information.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
search_cves("tamu.edu")