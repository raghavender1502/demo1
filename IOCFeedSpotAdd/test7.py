import requests

feedspotKey = "5xX15I8b6OoZ4uRH180cy+EZ+blnSuobGxLlSdbIF8ncD8u2lEsb/i3o6hbZyRPG4hL65JNM6ulL5OoaBfZL/OAV9uKTHunrG+YTStjIG8zcD8uwYxrp6h7e3ksJ+BbS40P45JRP6u4d5+YZ3fcX/BRFxrdnH+TpSxIS"
Headers = {
    "Authorization": feedspotKey,
    "Content-Type": "application/json; charset=utf-8"
}

def dataFolderID(folder_id):
    response = requests.get(f"https://api.feedspot.com/v1/folders/{folder_id}.json", headers=Headers).json()
    try:
        payload = {
            "folder_id": folder_id,
            "response": response
        }
        # Add "ioc" field to each item in the response
        for item in response:
            feed_url = item["feed_url"]
            ioc_payload = ioc_parser(feed_url)
            item["ioc"] = ioc_payload
        return payload
    except:
        payload = {
            "folder_id": folder_id,
            "response": response
        }
        return payload

def ioc_parser(input_url):
    url = "https://api.iocparser.com/url"

    payload = {
        "url": str(input_url)
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    finalPayload = response.json()
    return finalPayload

print(dataFolderID("5758880"))
print(ioc_parser("https://www.grahamcluley.com/feed/"))
