#from .MainInfraStructureServices import dnslookup
#from .OpenBuckets import open_buckets
from .OtherDomainOnSameIP import getDomains


def assetsInventory(target):
    payload = {
        "Domain": target,
        "TestResults": {
            #"Main Infrastructure Services": dnslookup(target),
            #"Open Buckets": open_buckets(target),
            "Other Domains on same IP": getDomains(target),
        },
        "Warnings in Assets Inventory": []
    }

    warnings = []
    for key, value in payload["TestResults"].items():
        if ("Status" in value.keys() and value["Status"] == "Warning"):
            slug = {
                "testName": key, "status": value["Status"], "description": value["Description"], "moreInfo": value["moreInfo"]}
            warnings.append(slug)

    payload["Warnings in Assets Inventory"] = warnings

    return payload


