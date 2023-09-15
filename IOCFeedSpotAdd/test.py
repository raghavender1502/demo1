import requests

feedspotKey = "5xX15I8b6OoZ4uRH180cy+EZ+blnSuobGxLlSdbIF8ncD8u2lEsb/i3o6hbZyRPG4hL65JNM6ulL5OoaBfZL/OAV9uKTHunrG+YTStjIG8zcD8uwYxrp6h7e3ksJ+BbS40P45JRP6u4d5+YZ3fcX/BRFxrdnH+TpSxIS"
Headers = {
    "Authorization": feedspotKey,
    "Content-Type": "application/json; charset=utf-8"
}

def dataFolderID(folder_id):
    response = requests.get(f"https://api.feedspot.com/v1/folders/{folder_id}.json", headers=Headers).json()
    try:
        #response["response"]["ioc_parser"] = "example_ioc_parser" 
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
print(dataFolderID("5758880"))
# def folder_mapping():
#     folders = requests.get("https://api.feedspot.com/v1/subscriptions.json", headers=Headers).json()
#     folderInfo = {}
#     for folder in folders:
#         if 'folder_id' in folder:
#             folderInfo[folder["title"]] = folder["folder_id"]
#     return folderInfo

# def foldersList():
#     folders = requests.get("https://api.feedspot.com/v1/subscriptions.json", headers=Headers).json()
#     foldersList = [folder["title"] for folder in folders if 'folder_id' in folder]
#     response = {"response": foldersList}
#     return response

# def entriesFeedID(feed_id):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?feed_id={feed_id}", headers=Headers).json()
#     try:
#         payload = {
#             "feedID": feed_id,
#             "response": response
#         }
#         return payload
#     except:
#         payload = {
#             "feedID": "",
#             "response": ""
#         }
#         return payload

# def entriesTagID(tag_id):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?tag_id={tag_id}", headers=Headers).json()
#     try:
#         payload = {
#             "tagID": tag_id,
#             "response": response
#         }
#         return payload
#     except:
#         payload = {
#             "tagID": "",
#             "response": ""
#         }
#         return payload

# def entriesTagName(tag_name):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?tag_name={tag_name}", headers=Headers).json()
#     try:
#         payload = {
#             "tagName": tag_name,
#             "response": response
#         }
#         return payload
#     except:
#         payload = {
#             "tagName": "",
#             "response": ""
#         }
#         return payload

# def entriesSort(order):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?sort={order}", headers=Headers).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def entriesUnread(value):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?unread={value}", headers=Headers).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def entriesShared(value):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?shared={value}", headers=Headers).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def entriesStarred(value):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?starred={value}", headers=Headers).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def entriesLimit(limit):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?limit={limit}", headers=Headers).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def entriesUnreadDate(date):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?unread_date={date}", headers=Headers).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def entriesFeedEntryID(feed_entry_id):
#     response = requests.get(f"https://api.feedspot.com/v1/entries/{feed_entry_id}.json", headers=Headers).json()
#     try:
#         payload = {
#             "feedEntryID": feed_entry_id,
#             "response": response
#         }
#         return payload
#     except:
#         payload = {
#             "feedEntryID": "",
#             "response": ""
#         }
#         return payload

# def feedsMapping():
#     response = requests.get("https://api.feedspot.com/v1/feeds.json", headers=Headers).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def makeStarred(entry_ids):
#     payload = {
#         "entry_ids": entry_ids
#     }
#     response = requests.post("https://api.feedspot.com/v1/starred_entries.json", headers=Headers, data=json.dumps(payload)).json()
#     try:
#         payload = {"response": response}
#         return payload
#     except:
#         payload = {"response": ""}
#         return payload

# def searchFilter(filter_name):
#     response = requests.get(f"https://api.feedspot.com/v1/entries.json?filter={filter_name}", headers=Headers).json()
#     try:
#         payload = {
#             "filterName": filter_name,
#             "response": response
#         }
#         return payload
#     except:
#         payload = {
#             "filterName": "",
#             "response": ""
#         }
#         return payload

# def ioc_parser(input_url):
#     url = "https://api.iocparser.com/url"

#     payload = {
#         "url": str(input_url)
#     }

#     headers = {
#     'Content-Type': 'application/json',
#     }

#     response = requests.request("POST", url, headers=headers, json = payload)
#     finalPayload = response.json()
#     return finalPayload

# # Example usage:
# folder_id = "YOUR_FOLDER_ID"
# print(dataFolderID(folder_id))

# tag_id = "YOUR_TAG_ID"
# print(entriesTagID(tag_id))

# tag_name = "YOUR_TAG_NAME"
# print(entriesTagName(tag_name))

# order = "asc"  # or "desc"
# print(entriesSort(order))

# unread_value = True  # or False
# print(entriesUnread(unread_value))

# shared_value = True  # or False
# print(entriesShared(shared_value))

# starred_value = True  # or False
# print(entriesStarred(starred_value))

# limit = 10
# print(entriesLimit(limit))

# date = "2023-06-25"
# print(entriesUnreadDate(date))

# feed_entry_id = "YOUR_FEED_ENTRY_ID"
# print(entriesFeedEntryID(feed_entry_id))

# print(feedsMapping())

# entry_ids = ["ENTRY_ID_1", "ENTRY_ID_2"]  # Replace with actual entry IDs
# print(makeStarred(entry_ids))

# filter_name = "YOUR_FILTER_NAME"
# print(searchFilter(filter_name))

# url = "https://www.grahamcluley.com/feed/" # Replace with the actual URL
# print(ioc_parser(url))
