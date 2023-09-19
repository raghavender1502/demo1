
from pythonping import ping
import dns.resolver
from netaddr import *
import socket
import threading



def get_IP(target):
    try:
        target_IP = socket.gethostbyname(target)
        return target_IP
    except:
        print("Failed: Could not get IP")
        return ""


def get_IPv4(target):
    try:
        target_IP = socket.gethostbyname(target)
        ips = socket.getaddrinfo(
            target, "http", family=socket.AF_INET, proto=socket.IPPROTO_TCP
        )

        return ips[0][-1][0]
    except:
        print("Failed: Could not get IPv4")
        return ""


def get_IPv6(target):
    try:
        target_IP = socket.gethostbyname(target)
        ips = socket.getaddrinfo(
            target, "http", family=socket.AF_INET6, proto=socket.IPPROTO_TCP
        )
        
        return ips[0][-1][0]
    except:
        print("Failed: Could not get IPv6")
        return ""


################ check A record ################
def check_A_records(target):
    response_data = {
        "test": "A record",
        "status": "",
        "description": "",
    }

    # Finding A record
    try:
        result = list(dns.resolver.resolve(target, "A"))
        if len(result) != 0:
            response_data["status"] = "Ok"
            response_data["description"] = f"{target} have A record"
        else:
            response_data["status"] = "Warning"
            response_data["description"] = f"{target} have no A record"
    except:
        print("Failed to get the A records")
        response_data["status"] = "Failed"
        response_data["description"] = f"Failed to get the A records for {target}"

    
    return response_data


############### check AAAA record ################
def check_AAAA_records(target):
    response_data = {
        "test": "AAAA record",
        "status": "",
        "description": "",
    }
    # Finding AAAA record
    try:
        result = list(dns.resolver.query(target, "AAAA"))

        if len(result) != 0:
            response_data["status"] = "Ok"
            response_data["description"] = f"{target} have AAAA record"
        else:
            response_data["status"] = "Warning"
            response_data["description"] = f"{target} have no AAAA record"

    except:
        print("Failed to get the AAAA records")
        response_data["status"] = "Failed"
        response_data["description"] = f"Failed to get the AAAA records for {target}"

    
    return response_data


############### check if IP public or not ################
def check_IP_status(target):
    response_data = {
        "test": "IP Status",
        "status": "",
        "description": "",
    }
    try:
        result = IPAddress(socket.gethostbyname(target)).is_private()
        if result == False:
            response_data["status"] = "Ok"
            response_data["description"] = "IP is Public"
        else:
            response_data["status"] = "Warning"
            response_data["description"] = "IP is not Public"
    except:
        print("Failed: NS not valid")

    
    return response_data


############### check if name server responded or not ################
def run_with_ping(server):
    result = ping(server)
    return result.success()


def run_with_timeout(timeout,  server):
    event = threading.Event()

    def wrapper():
        socket.gethostbyname(server)
        event.set()
    thread = threading.Thread(target=wrapper)
    thread.daemon = True
    thread.start()
    return event.wait(timeout)


def check_NS_response(target):
    response_data = {
        "test": "NS response",
        "status": "",
        "description": "",
    }
    try:
        dns_ping = run_with_ping(target)
        

        if (dns_ping):
            response_data["status"] = "Ok"
            response_data["description"] = f"'{target}' responded successfully"
    except:
        
        response_data["status"] = "Failed"
        response_data["description"] = f"No response from '{target}'"
    
    return response_data

############### check if TCP connections allowed or not ################


def check_TCP_connection(target):
    response_data = {
        "test": "TCP connection",
        "status": "",
        "description": "",
    }
    try:
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = (socket.gethostbyname(target), 53)
        result = a_socket.connect_ex(location)
        
        if result == 0:
            
            response_data["status"] = "Ok"
            response_data["description"] = "TCP connection allowed"
        else:
            
            response_data["status"] = "Failed"
            response_data["description"] = f"TCP connection not allowed for {target}"

        a_socket.close()
    except:
        pass

    return response_data

