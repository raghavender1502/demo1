import requests
from bs4 import BeautifulSoup
import json


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
#print(ioc_parser("https://fast.com/"))

def alertUrls(url):
    finalPayload = []
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    # to get the alertIDs
    urls = []
    for link in soup.find_all('a'):
        if str(link.get('href')).startswith("/ncas/alerts/a"):
            urls.append(str(link.get('href')))
    alertIds = []
    for i in urls:
        alertIds.append(i[13:].upper()) 
    # to get the list of URLs
    urlList = []        
    for item in urls:
        newitem  = "https://www.cisa.gov/uscert"+item   
        urlList.append(newitem)
    # get the titles of all the urls:
    titles = []
    for i in range(len(urlList)):
        URL = urlList[i]
        reqss = requests.get(URL)
        soup = BeautifulSoup(reqss.text, 'html.parser')
        for title in soup.find_all('title'):
            Title = title.get_text()
            titles.append(Title)
        
    for i in range(len(urlList)):
        payload = ioc_parser(urlList[i])
        alertID = alertIds[i]
        json_data = {}
        json_data["alertID"] = alertID
        json_data["title"] = titles[i]
        json_data["response"] = payload
        finalPayload.append(json_data)
    return finalPayload        
print(alertUrls("https://fast.com/"))