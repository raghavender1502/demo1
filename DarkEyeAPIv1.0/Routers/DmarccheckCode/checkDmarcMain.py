import subprocess
import json

def get_dmarc_records(target):
    response_data = {
        "domain":target,
        "TestName":"DMARC",
        "Status": "Failed",
        "record": "",
        "Description": "Couldn't get DMARC record."
    }
    try:
        dmarc_response_1 = subprocess.Popen(["checkdmarc", target], stdout=subprocess.PIPE).stdout.read()
        #print(dmarc_response_1)
        result_1 = dmarc_response_1.decode("utf-8")
        dmarc_response = json.loads(result_1)
        #print(dmarc_response)
        rec = ""
        #print("\n******************\n")
        if dmarc_response["dmarc"]["valid"] == True:
            rec = dmarc_response["dmarc"]["record"]
            response_data = {
            "domain":target,
            "TestName":"DMARC",
            "Status": "Ok",
            "record": rec,
            "Description": "DMARC is configured."
            }
            #print(response_data)
        else:
            response_data = {
            "domain":target,
            "TestName":"DMARC",
            "Status": "Warning",
            "record": rec,
            "Description": "DMARC is not configured."
            }
            #print(response_data)
    except Exception as e:
        print("EXCEPTION: Not valid",e)
        response_data = {
            "domain":target,
            "TestName":"DMARC",
            "Status": "Failed",
            "record": "",
            "Description": "Couldn't get DMARC record."
        }
    if response_data["Status"] == "Ok":
        return response_data
    if response_data["Status"] == "Failed":
        cmd = ["nslookup", "-type=txt", f"_dmarc.{target}"]
        try:

            dmarc_response_2 = subprocess.Popen(
                cmd, stdout=subprocess.PIPE).stdout.read()
            result_2 = dmarc_response_2.decode("utf-8")
            res_2 = result_2.split("\r\n\r\n")[2].strip("\t\n\r\"")
            if (res_2):

                response_data["Status"] = "Ok"
                response_data["record"] = res_2
                response_data["Description"] = "DMARC is configured."
        except:

            pass
    return response_data

#print(get_dmarc_records("DOMAIN_NAME"))