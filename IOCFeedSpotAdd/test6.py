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
            item["ioc"] = "value"  # Replace "value" with the actual value you want to assign to the "ioc" field
        return payload
    except:
        payload = {
            "folder_id": "",
            "response": ""
        }
        return payload


print(dataFolderID("5758880"))
