import requests

feedspotKey = "5xX15I8b6OoZ4uRH180cy+EZ+blnSuobGxLlSdbIF8ncD8u2lEsb/i3o6hbZyRPG4hL65JNM6ulL5OoaBfZL/OAV9uKTHunrG+YTStjIG8zcD8uwYxrp6h7e3ksJ+BbS40P45JRP6u4d5+YZ3fcX/BRFxrdnH+TpSxIS"
feedspotHeaders = {
    "Authorization": feedspotKey,
    "Content-Type": "application/json; charset=utf-8"
}

url = "https://api.iocparser.com/url"
iocHeaders = {
    'Content-Type': 'application/json'
}

def dataFolderID(folder_id):
    response = requests.get(f"https://api.feedspot.com/v1/folders/{folder_id}.json", headers=feedspotHeaders).json()
    try:
        payload = {
            "folder_id": folder_id,
            "response": response
        }
        return payload
    except:
        payload = {
            "folder_id": "",
            "response": ""
        }
        return payload

def iocParser(url):
    iocPayload = {"url": url}
    response = requests.request("POST", url, headers=iocHeaders, json=iocPayload)
    return response.json()

folder_id = "5758880"
folder_data = dataFolderID(folder_id)

if folder_data["folder_id"] == folder_id:
    response = folder_data["response"]
    urls = []

    for item in response:
        if "feedurl" in item:
            urls.append(item["feedurl"])

    for url in urls:
        ioc_data = iocParser(url)
        print(f"IOC Parser results for URL: {url}")
        print(ioc_data)
        print("-" * 50)
else:
    print("Folder not found.")
print(iocParser("https://feeds.feedburner.com/TheHackersNews?format=xml"))