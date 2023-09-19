# function to get key-value from dictionary
def get_key_value(item):
    for i in item:
        return i, item[i]

# function to check the Validation of NS records


def test_ns_records(ns_records, ns_records_list):
    print([{"NS Records":i}for i in ns_records_list])
    ###### A Records ######
    res_A_Records = {
        "TestName":"Name servers have A record",
        "Status": "",
        "Description": "",
        "moreInfo": [{"NS Records": ""}]
    }
    ls_A_Records = []
    er_A_records = {}

    ###### AAAA Records ######
    res_AAAA_Records = {
        "TestName":"Name servers have AAAA record",
        "Status": "",
        "Description": "",
        "moreInfo": [{"NS Records": ""}]
    }
    ls_AAAA_Records = []
    er_AAAA_records = {}

    ###### NS Response ######
    res_NS_Response = {
        "TestName":"All name servers responded",
        "Status": "",
        "Description": "",
        "moreInfo": [{"NS Records": ""}]
    }
    ls_NS_Response = []
    er_NS_Response = {}

    ###### IP Status ######
    res_IP_Status = {
        "TestName":"All IPs are public",
        "Status": "",
        "Description": "",
        "moreInfo": [{"NS Records": ""}]
    }
    ls_IP_Status = []
    er_IP_Status = {}

    ###### TCP Connection ######
    res_TCP_Connection = {
        "TestName":"TCP connections allowed",
        "Status": "",
        "Description": "",
        "moreInfo": [{"NS Records": ""}]
    }
    ls_TCP_Connection = []
    er_TCP_Connection = {}

    for data in ns_records:
        for key, value in data.items():
            ####### checking A records #######
            if value["A_Records"]["Status"] == "Ok":
                ls_A_Records.append(value["A_Records"]["Status"])
            else:
                d = {key: value["A_Records"]["Status"]}
                ls_A_Records.append(d)

            ####### checking AAAA records #######
            if value["AAAA_Records"]["Status"] == "Ok":
                ls_AAAA_Records.append(value["AAAA_Records"]["Status"])
            else:
                d = {key: value["AAAA_Records"]["Status"]}
                ls_AAAA_Records.append(d)

            ####### checking NS Response #######
            if value["NS_Response"]["Status"] == "Ok":
                ls_NS_Response.append(value["NS_Response"]["Status"])
            else:
                d = {key: value["NS_Response"]["Status"]}
                ls_NS_Response.append(d)

            ####### checking IP Status #######
            if value["IP_Status"]["Status"] == "Ok":
                ls_IP_Status.append(value["IP_Status"]["Status"])
            else:
                d = {key: value["IP_Status"]["Status"]}
                ls_IP_Status.append(d)

            ####### checking TCP Connection #######
            if value["TCP_Connection"]["Status"] == "Ok":
                ls_TCP_Connection.append(value["TCP_Connection"]["Status"])
            else:
                d = {key: value["TCP_Connection"]["Status"]}
                ls_TCP_Connection.append(d)

    ####### checking A records #######
    for item in ls_A_Records:
        if (type(item) == dict):
            # print("Yes", item)
            # er_A_records[list(item.keys())[0]] = list(item.values())[0]
            k, v = get_key_value(item)
            er_A_records[k] = v

    if len(list(er_A_records.keys())) == 0:
        res_A_Records["Status"] = "Ok"
        res_A_Records["Description"] = "All the Name servers are configured with A records and are reachable via IPv4."
        res_A_Records["moreInfo"] = [{"NS Records":i} for i in ns_records_list]
    else:
        res_A_Records["Status"] = "Warning"
        res_A_Records["Description"] = "Found Name servers that are not configured with A records and cannot be reached via IPv4. As a good practise, it is recommended for Name servers to be configured with A records."           
        res_A_Records["moreInfo"] = [{"NS Records":i} for i in list(er_A_records.keys())]
        

    ####### checking AAAA records #######
    for item in ls_AAAA_Records:
        if (type(item) == dict):
            # print("Yes", item)
            # er_A_records[list(item.keys())[0]] = list(item.values())[0]
            k, v = get_key_value(item)
            er_AAAA_records[k] = v

    if len(list(er_AAAA_records.keys())) == 0:
        res_AAAA_Records["Status"] = "Ok"
        res_AAAA_Records["Description"] = "All the Name servers are configured with AAAA records and are reachable via IPv6."
        res_AAAA_Records["moreInfo"] = [{"NS Records":i} for i in ns_records_list]
    else:
        res_AAAA_Records["Status"] = "Warning"
        res_AAAA_Records["Description"] = "Found Name servers that are not configured with A records and cannot be reached via IPv6. As a good practise, it is recommended for Name servers to be configured with A records."
        res_AAAA_Records["moreInfo"] = [{"NS Records":i} for i in list(er_AAAA_records.keys())]

    ####### checking NS responses #######
    for item in ls_NS_Response:
        if (type(item) == dict):
            k, v = get_key_value(item)
            er_NS_Response[k] = v

    if len(list(er_NS_Response.keys())) == 0:
        res_NS_Response["Status"] = "Ok"
        res_NS_Response["Description"] = "All the Authoritative Name servers responded. Tests will be conducted from multiple network locations to verify the name server is responding."
        res_NS_Response["moreInfo"] = [{"NS Records":i} for i in ns_records_list]
    else:
        res_NS_Response["Status"] = "Failed"
        res_NS_Response["Description"] = "Found Name servers that did not respond. Please ensure if Denial of Service protection is enabled and no takeover of Name servers has happened."
        res_NS_Response["moreInfo"] = [{"NS Records":i} for i in list(er_NS_Response.keys())]
            

    ####### checking IP status #######
    for item in ls_IP_Status:
        if (type(item) == dict):
            k, v = get_key_value(item)
            er_IP_Status[k] = v

    if len(list(er_IP_Status.keys())) == 0:
        res_IP_Status["Status"] = "Ok"
        res_IP_Status["Description"] = "All the IP addresses for Name servers are reachable via Internet."
        res_IP_Status["moreInfo"] = [{"NS Records":i} for i in ns_records_list]
        
    else:
        res_IP_Status["Status"] = "Failed"
        res_IP_Status["Description"] = "Found Name servers that are not configured with public IP addresses. Please configure the Name servers with Public IP address to make them reachable via Internet."
        res_IP_Status["moreInfo"] = [{"NS Records":i} for i in list(er_IP_Status.keys())]
            

    ####### checking TCP Connection #######
    for item in ls_TCP_Connection:
        if (type(item) == dict):
            k, v = get_key_value(item)
            er_TCP_Connection[k] = v

    if len(list(er_TCP_Connection.keys())) == 0:
        res_TCP_Connection["Status"] = "Ok"
        res_TCP_Connection["Description"] = "TCP connections are allowed for all the Authoritative Name servers."
        res_TCP_Connection["moreInfo"] = [{"NS Records":i}for i in ns_records_list]
    else:
        res_TCP_Connection["Status"] = "Failed"
        res_TCP_Connection["Description"] = "Found Name servers for which TCP connections are not allowed."
        res_TCP_Connection["moreInfo"]= [{"NS Records":i}for i in list(er_TCP_Connection.keys())]
        

    # print("\nA:", res_A_Records)
    # print("\nAAAA:", res_AAAA_Records)
    # print("\nNS Response:", res_NS_Response)
    # print("\nIP Status:", res_IP_Status)
    # print("\nTCP Connection:", res_TCP_Connection)
    return res_A_Records, res_AAAA_Records, res_NS_Response, res_IP_Status, res_TCP_Connection


