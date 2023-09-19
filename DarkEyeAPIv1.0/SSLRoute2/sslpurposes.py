import subprocess
import os
import time

timestr = time.strftime("%Y%m%d-%Hhours%MMins%Sseconds")

def download_pem(host):
    
    cmd0 = "openssl s_client -connect "+host+":443 2>&1 < /dev/null | sed -n '/-----BEGIN/,/-----END/p' > c-"+timestr+".pem"
    os.popen(cmd0)


def get_ca_purpose( pem="c-"+timestr+".pem"):
  
        cmd = ['openssl', 'x509', '-noout','-text', '-purpose', '-in', 'c-'+timestr+'.pem']
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        out = p.communicate(input=pem.encode())[0].decode('utf-8').strip()
         
        mylist = out.split("Certificate purposes:")[1].split("\n")[1:]
        #print(mylist)
        allowed_purposes = []
        for i in mylist:
            if "Yes" in i:
                allowed_purposes.append(i[:-6])
        allowed_ca_purposes= []
        for x in allowed_purposes:
            if "CA" in x:
                allowed_ca_purposes.append(x[:-3])
                allowed_purposes.remove(x)

        payload = {
            "Allowed purposes": allowed_purposes,
            "Allowed CA purposes": allowed_ca_purposes,
        }
        
        return payload

def del_pem():
    os.remove("c-"+timestr+".pem")
def get_data_sslpurpose(domain):
    try:
        download_pem(domain)
        time.sleep(5)
        data=get_ca_purpose() 
    except:
        data={}
    new_data={}
    new_data["Domain"] =domain
    new_data["TestResult"]=data
    try:
        del_pem()
    except:
        new_data["Domain"] =domain
        new_data["TestResult"]=data
    return new_data
    

