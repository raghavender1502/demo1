#!/bin/python3
import re
import requests
#import csv
import socket
from bs4 import BeautifulSoup
import time
import json 
#import tldextract
from urllib.parse import urlparse

'''
parser = argparse.ArgumentParser( description = "" )
parser.add_argument('-d','--domain', type=str) 
args = parser.parse_args()
domain = args.domain
'''


# Extract Information

def extractInfo(domain):
    #to store json data
    dictionary = []
    li=[]
    url = domain
    try:
        hostname1 = urlparse(domain).netloc 
        if("www" in hostname1):
            hostname1=hostname1[4:] 
        c=0
        #user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

        # perform get request to the url
        reqs = requests.get(url)
        
        content = reqs.text

    # convert the text to a beautiful soup object
        soup = BeautifulSoup(content, 'html.parser')
        #urls4 = []

        # For loop that iterates over all the iframe tags
        for h in soup.findAll('iframe'):
            try:
                if 'src' in h.attrs:
                    
                    url1 = h.get('src')
                    li.append(url1)
                    #to find the exact domain name
                    hostname = urlparse(url1).netloc
                    try:
                        if(li.count(url1)<=1):
                            ip_address = socket.gethostbyname(hostname)
                            if(ip_address!="0.0.0.0"):
                                if("http" not in url1 and "https" not in url1):
                                    url1="https:"+url1 
                                ## storing all values in dictionary
                                url_dict = {} 
                                url_dict['URL'] = url1
                                if(hostname1 in hostname):
                                    url_dict['Category'] = "Internal Iframe Source"
                                else:
                                    url_dict['Category'] = "External Iframe Source"
                                
                                url_dict['Ip']  = ip_address
                                
                                dictionary.append(url_dict)

                    except:
                        pass
                    
            # tag does not has a href params we pass
            except:
                pass
        
        # For loop that iterates over all the <a> tags
        for h in soup.findAll('a'):
            try:
                # looking for href inside anchor tag
                if 'href' in h.attrs:
                    
                    # storing the value of href in a separate
                    # variable
                    url1 = h.get('href')
                    li.append(url1)
                    url_dict = {}  
                    #finding exact domain name
                    hostname = urlparse(url1).netloc
                    
                    try:
                        if(hostname1 not in hostname):
                            if(li.count(url1)<=1):
                                ip_address = socket.gethostbyname(hostname)
                                if(ip_address!="0.0.0.0"):    
                                    if(url1[0]!="/" and "mailto" not in url1):
                                        if("http" not in url1 and "https" not in url1):
                                            url1="https:"+url1 
                                        url_dict['URL'] = url1
                                        
                                        #if(hostname1 in hostname):
                                        #    url_dict['Category'] = "Internal Link"
                                            
                                        #else:

                                        url_dict['Category'] = "Outgoing Link"
                                        
                                        url_dict['Ip']  = ip_address
                                        dictionary.append(url_dict)
                    except:
                        pass
            except:
                pass
        
    
        # looking for href inside li tag
        for h in soup.findAll('li'):
            a=h.find('a')
            try:
                if 'href' in a.attrs:
                    url=a.get('href')
                    li.append(url)
                    hostname = urlparse(url).netloc
                    try:
                        if(hostname1 not in hostname):
                            
                            if(li.count(url)<=1):
                                ip_address=socket.gethostbyname(hostname)
                                if(ip_address!="0.0.0.0"):
                            
                                    url_dict={}
                                    if(url[0]!="/" and "mailto" not in url):
                                        if("http" not in url and "https" not in url):
                                            url="https:"+url 
                                        url_dict['URL']=url 
                                        
                                        #if(hostname1 not in hostname):
                                        #    url_dict['Category'] = "Internal Link"
                                            
                                        #else:
                                        
                                        url_dict['Category'] = "Outgoing link"
                                        
                                        url_dict['Ip']  = ip_address
                                        
                                        dictionary.append(url_dict)
                    except:
                        pass
                    
            except:
                pass
        # For loop that iterates over all the script tags
        for h in soup.findAll('script'):
                
            try:
                # looking for src inside script tag
                if 'src' in h.attrs:
                    
                    url1 = h.get('src')
                    li.append(url1)
                    hostname = urlparse(url1).netloc
                    try:
                        if(li.count(url1)<=1):
                            ip_address = socket.gethostbyname(hostname)
                            if(ip_address!="0.0.0.0"):
                                if("http" not in url1 and "https" not in url1):
                                    url1="https:"+url1     
                                url_dict = {} 
                                url_dict['URL'] = url1
                                if(hostname1 in hostname):
                                    url_dict['Category'] = "Internal JavaScript"
                                else:
                                    url_dict['Category'] = "External JavaScript"
                                url_dict['Ip']  = ip_address
                                
                                dictionary.append(url_dict)
                    except:
                        pass
            except:
                pass
        
        # For loop that iterates over all the img tags
        for h in soup.findAll('img'):
            
            # looking for src inside the <img>tag
            
            try:
                if 'src' in h.attrs:
                    
                    # storing the value of href in a separate
                    # variable
                    url1 = h.get('src')
                    li.append(url1)
                    hostname = urlparse(url1).netloc
                    try:
                        if(li.count(url1)<=1):
                            ip_address = socket.gethostbyname(hostname)
                            if(ip_address!="0.0.0.0"):
                                if("http" not in url1 and "https" not in url1):
                                    url1="https:"+url1 
                                url_dict = {} 
                                url_dict['URL'] = url1
                                if(hostname1 in hostname):
                                    url_dict['Category'] = "Internal image"
                                else:
                                    url_dict['Category'] = "External image"
                                
                                url_dict['Ip']  = ip_address
                                
                                dictionary.append(url_dict)
                    except:
                        pass
            except:
                pass
        #print(urls2)
        
        #print("##########")
        urls3 = []

        # For loop that iterates over all the link tags
        for h in soup.findAll('link'):
            try:
                # looking for href inside link tag
                if 'href' in h.attrs:
                    
                    # storing the value of href in a separate
                    # variable
                    url = h.get('href')
                    #print("URL: ",url)
                    if "css" in url: 
                        li.append(url)
                        #print("LI tag: ",li)
                        hostname = urlparse(url).netloc
                        try:
                            if(li.count(url)<=1):
                                ip_address = socket.gethostbyname(hostname)
                                if(ip_address!="0.0.0.0"):
                                    if("http" not in url and "https" not in url):
                                        url="https:"+url             
                                    url_dict = {} 
                                    url_dict['URL'] = url
                                    if(hostname1 in hostname):
                                        url_dict['Category'] = "Internal CSS"
                                    else:
                                        url_dict['Category'] = "External CSS"
                                    
                                    url_dict['Ip']  = ip_address
                                    
                                    dictionary.append(url_dict)
                        except:
                            pass
            except:
                pass
        
        
        
        
        #print(dictionary1)
        #f = open('newalvaradohospital24.json', 'w') 
        #f.write(json.dumps(dictionary1))
        #f.close() 
        #file = open('newalvaradohospital24.json')
        #data = json.load(file)
        data = {  url : dictionary }
        output={}
        output["Domain"] = hostname1 
        output["Testresult"] = dictionary
        output["extSource"] = "Website Crawling"
        #pprint.pprint(new_dict)
        #print(new_dict)
        #with open("sample1.json", "w") as outfile: 
            #json.dump(new_dict, outfile)
        return output
    except Exception as e:
        print("Exception: Connected Domains: ",e)
        output = {
            "Domain":hostname1 ,
            "Testresult": [],
            "extSource": "Website Crawling"
        }
        return output


def extract(domain):
    if("https" not in domain):
        if("www" not in domain):
            domain="https://" + "www." + domain
        else:
            domain="https://" + domain
    output= extractInfo(domain)
    #output=json.dumps(output)
    #print(output)
    return output

#extract(domain)
