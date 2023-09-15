import requests
import time
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
            time.sleep(1)
            feed_url = item["feed_url"]
            ioc_payload = get_ioc_from_url(feed_url)
            if "status" in ioc_payload and ioc_payload["status"] == "error":
                item["ioc"] = {}
            else:
                item["ioc"] = ioc_payload
            #print(item)
        return payload
    except:
        payload = {
            "folder_id": folder_id,
            "response": response
        }
        return payload

def get_ioc_from_url(url):
    ioc_url = "https://api.iocparser.com/url"

    payload = {
        "url": url
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(ioc_url, headers=headers, json=payload)
    ioc_data = response.json()
    return ioc_data

print(dataFolderID("5758880"))
