import requests 

def ioc_parser(input_url):
    url = "https://api.iocparser.com/url"

    payload = {
        "url": str(input_url)
    }

    headers = {
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, json = payload)
    finalPayload = response.json()
    return finalPayload
print(ioc_parser("https://www.securitymadesimple.org/cybersecurity-blog?format=rss"))