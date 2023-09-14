import requests

def Zone_Transfer(domain):
    response = requests.get("https://api.hackertarget.com/zonetransfer/?q="+domain)
    response = response.text.splitlines()

    resp = []
    temp = ''
    for i in response:
        if(i == '' and temp != ''):
            resp.append(temp)
            temp = ''
        else:
            temp = temp + i + " "

    dict1 = {}
    dict2 = {}
    dict1["domain"] = domain
    dict1["status"] = "OK"
    dict1["description"] = f"Zone transfer failed for all the name servers for the {domain}"
    dict2["domain"] = domain
    dict1["response"] = []
    dict2["response"] = []
    dict2["status"] = "warning"
    dict2["description"] = f"Zone transfer successful for the following name servers for the {domain}"

    countF = 0
    countS = 0
    for i in resp:
        i = i.replace(';', '')  # Remove semicolons
        i = i.replace('<', '').replace('>', '')  # Remove angle brackets
        if "Transfer failed." in i:
            countF += 1 
            dict1["response"].append(i)
        elif "Transfer sucseess" in i:
            countS += 1 
            dict2["response"].append(i)

    return dict1, dict2

failureC, successC = Zone_Transfer('tamu.edu')
if failureC["response"] != []:
    print(failureC)
else:
    print(successC)
