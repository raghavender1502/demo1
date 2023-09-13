import requests

def get_domain_info(domain):
    """
    Returns the CPE, CPE23, and vulnerabilities for the given domain.

    Args:
        domain: The domain name to lookup.

    Returns:
        A dictionary containing the CPE, CPE23, and vulnerabilities for the given domain.
    """
    url = f"https://nvd.nist.gov/cpe/api/cpe/lookup/?name={domain}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cpe_list = data.get("cpe_list", [])
        if cpe_list:
            cpe = cpe_list[0].get("cpe")
            cpe23 = cpe_list[0].get("cpe23")
        else:
            cpe = None
            cpe23 = None

        vulns = data.get("vulnerabilities", [])
        return {"cpe": cpe, "cpe23": cpe23, "vulns": vulns}
    else:
        return {}

if __name__ == "__main__":
    domain = "primehealthcare.com"
    domain_info = get_domain_info(domain)
    print(domain_info)
