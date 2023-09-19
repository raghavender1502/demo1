# function to get key-value from dictionary
def get_key_value(item):
    for i in item:
        return i, item[i]


# function to check the Validation of NS records
def test_mx_records(mx_records):
    ###### A Records ######
    res_A_Records = {
        "TestName":"A records configured" ,
        "Status": "",
        "Description": ""
    }
    ls_A_Records = []
    er_A_records = {}

    ###### AAAA Records ######
    res_AAAA_Records = {
        "TestName":"AAAA records configured",
        "Status": "",
        "Description": ""
    }
    ls_AAAA_Records = []
    er_AAAA_records = {}

    ###### CNAME records ######
    res_CNAME_record = {
        "TestName":"Mail servers are not present in CNAME records",
        "Status": "",
        "Description": ""
    }
    ls_CNAME_record = []
    er_CNAME_record = {}

    ###### domain records ######
    res_domain_names = {
        "TestName":"Exchange fields contain valid domain names",
        "Status": "",
        "Description": ""
    }
    ls_domain_names = []
    er_domain_names = {}

    ###### IP Status ######
    res_IP_Status = {
        "TestName":"IPs are public",
        "Status": "",
        "Description": ""
    }
    ls_IP_Status = []
    er_IP_Status = {}

    ###### contain IPs ######
    res_contain_IP = {
        "TestName":"Exchange fields don't contain IPs",
        "Status": "",
        "Description": ""
    }
    ls_contain_IP = []
    er_contain_IP = {}

    ###### NS return identical MX ######
    res_identical_MX = {
        "TestName":"Name Servers return identical MX records",
        "Status": "",
        "Description": ""
    }
    ls_identical_MX = []
    # er_identical_MX = {}
    # print("MX records ", mx_records)
    #print(mx_records)
    mx_records_list = []
    
    for data in mx_records:

        for key, value in data.items():
            mx_records_list.append(key)
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

            ####### checking CNAME records #######
            if value["CNAME_records"]["status"] == "Ok":
                ls_CNAME_record.append(value["CNAME_records"]["status"])
            else:
                d = {key: value["CNAME_records"]["status"]}
                ls_CNAME_record.append(d)

            ####### checking valid domain names #######
            if value["isValidDomain"]["Status"] == "Ok":
                ls_domain_names.append(value["isValidDomain"]["Status"])
            else:
                d = {key: value["isValidDomain"]["Status"]}
                ls_domain_names.append(d)

            ####### checking IP Status #######
            if value["IP_Status"]["Status"] == "Ok":
                ls_IP_Status.append(value["IP_Status"]["Status"])
            else:
                d = {key: value["IP_Status"]["Status"]}
                ls_IP_Status.append(d)

            ####### checking if contains IPs #######
            if value["is_IP"]["Status"] == "Failed":
                ls_contain_IP.append(value["is_IP"]["Status"])
            else:
                d = {key: value["is_IP"]["Status"]}
                ls_contain_IP.append(d)

            ####### NS returns identical MX records #######
            if value["NS_records"]:
                ls_identical_MX.append(value["NS_records"])

    ####### checking A records #######
    for item in ls_A_Records:
        if (type(item) == dict):
            # print("Yes", item)
            # er_A_records[list(item.keys())[0]] = list(item.values())[0]
            k, v = get_key_value(item)
            er_A_records[k] = v

    print("mx_records_list: ", mx_records_list)

    if len(list(er_A_records.keys())) == 0:
        res_A_Records["Status"] = "Ok"
        res_A_Records["Description"] = "All the mail servers are configured with A records. This test is performed to check reachability of mail servers via IPv4."
        res_A_Records["moreInfo"]= [{"MX Records":i} for i in mx_records_list]
    else:
        res_A_Records["Status"] = "Warning"
        res_A_Records["Description"] = "Found mail servers that are not configured with A records. This test is performed to check reachability of mail servers via IPv4."
        
        res_A_Records["moreInfo"]= [{"MX Records":i} for i in list(er_A_records.keys())]

    ####### checking AAAA records #######
    for item in ls_AAAA_Records:
        if (type(item) == dict):
            # print("Yes", item)
            # er_A_records[list(item.keys())[0]] = list(item.values())[0]
            k, v = get_key_value(item)
            er_AAAA_records[k] = v

    if len(list(er_AAAA_records.keys())) == 0:
        res_AAAA_Records["Status"] = "Ok"
        res_AAAA_Records["Description"] = "All the mail servers are configured with AAAA records. This test is performed to check reachability of mail servers via IPv6."
        res_AAAA_Records["moreInfo"] = [{"MX Records":i} for i in mx_records_list]
    else:
        res_AAAA_Records["Status"] = "Warning"
        res_AAAA_Records["Description"] = "Found mail servers that are not configured with AAAA records. This test is performed to check reachability of mail servers via IPv6."
        res_AAAA_Records["moreInfo"] = [{"MX Records":i} for i in list(er_AAAA_records.keys())]

    ####### checking CNAME records #######
    for item in ls_CNAME_record:
        if (type(item) == dict):
            k, v = get_key_value(item)
            er_CNAME_record[k] = v

    if len(list(er_CNAME_record.keys())) == 0:
        res_CNAME_record["Status"] = "Ok"
        res_CNAME_record["Description"] = "No Mail Servers present in CNAME records."
        res_CNAME_record["moreInfo"] = [{"More Info":"As per RFC 1034, section 3.6.2: if a name appears in the right-hand side of RR (Resource Record) it should not appear in the left-hand name of CNAME RR, thus CNAME records should not be used with NS and MX records."}]
    else:
        res_CNAME_record["Status"] = "Failed"
        res_CNAME_record["Description"] = "Found Mail Servers that are present in CNAME records. As per RFC 1034, section 3.6.2: if a name appears in the right-hand side of RR (Resource Record) it should not appear in the left-hand name of CNAME RR, thus CNAME records should not be used with NS and MX records."
        res_CNAME_record["moreInfo"] = [{"MX Records":i} for i in list(er_CNAME_record.keys())]

    ####### checking if domain names valid #######
    for item in ls_domain_names:
        if (type(item) == dict):
            k, v = get_key_value(item)
            er_domain_names[k] = v

    if len(list(er_domain_names.keys())) == 0:
        res_domain_names["Status"] = "Ok"
        res_domain_names["Description"] = "All MX record's Exchange fields contain valid domain names. Provide only valid domain names in the Exchange field of MX Record. Also, Mail servers with bad Exchange fields are unreachable."
        res_domain_names["moreInfo"] = [{"MX Records":i} for i in mx_records_list]
    else:
        res_domain_names["Status"] = "Failed"
        res_domain_names["Description"] = "Found MX record's Exchange fields that contain invalid domain names. Provide only valid domain names in the Exchange field of MX Record. Also, Mail servers with bad Exchange fields are unreachable."
        res_domain_names["moreInfo"] = [{"MX Records":i} for i in list(er_domain_names.keys())]

    ####### checking IP status #######
    for item in ls_IP_Status:
        if (type(item) == dict):
            k, v = get_key_value(item)
            er_IP_Status[k] = v

    if len(list(er_IP_Status.keys())) == 0:
        res_IP_Status["Status"] = "Ok"
        res_IP_Status["Description"] = "All IP addresses associated with mail servers are public and reachable via Internet."
        res_IP_Status["moreInfo"] = [{"MX Records":i} for i in mx_records_list]
    else:
        res_IP_Status["Status"] = "Failed"
        res_IP_Status["Description"] = "Found mail servers that have private IP address. It is recommended to use public IP addresses for the mail servers to be able to reach via Internet." 
        res_IP_Status["moreInfo"] = [{"MX Records":i} for i in list(er_IP_Status.keys())]

    ####### checking if contains IP #######
    for item in ls_contain_IP:
        if (type(item) == dict):
            k, v = get_key_value(item)
            er_contain_IP[k] = v

    if len(list(er_contain_IP.keys())) == 0:
        res_contain_IP["Status"] = "Ok"
        res_contain_IP["Description"] = "All the Exchange fields contain domain names only."
        res_contain_IP["moreInfo"] = [{"MX Records":i} for i in mx_records_list]
    else:
        res_contain_IP["Status"] = "Failed"
        res_contain_IP["Description"] = "IP addresses found in the Exchange fields." 
        res_contain_IP["moreInfo"] = [{"MX Records":i} for i in list(er_contain_IP.keys())]

    ####### checking if NS returns identical MX records #######
    # print(ls_identical_MX)
    if (len(ls_identical_MX) != 0):
        if ls_identical_MX.count(ls_identical_MX[0]) == len(ls_identical_MX):
            res_identical_MX["Description"] = "All the Name Servers return identical MX records."
            res_identical_MX["Status"] = "Ok"
            res_identical_MX["moreInfo"] = [{"More Info":"It is recommended that MX records point to different IPs."}]
        else:
            res_identical_MX["Status"] = "Failed"
            res_identical_MX["Description"] = "Some Name Servers returned different MX records."
            res_identical_MX["moreInfo"] = [{"More Info":"It is recommended that MX records point to different IPs."}]
    else:
        res_identical_MX["Description"] = "All the Name Servers return identical MX records."
        res_identical_MX["Status"] = "Ok"
        res_identical_MX["moreInfo"] = [{"More Info":"It is recommended that MX records point to different IPs."}]

    return res_A_Records, res_AAAA_Records, res_IP_Status, res_CNAME_record, res_domain_names, res_contain_IP, res_identical_MX