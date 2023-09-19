import socket
from OpenSSL import SSL
import argparse
import sys
import dns.resolver

"""
Check if ssl certificate provide by a server
is the same sent by dns (DANE protocol)
"""

def get_remote_certificate(host, port):
    """
    Return certificate of remote server
    Arguments:
    - host: server host of server who propose tlsa
    - port: server port of server who propose tlsa
    """
    addr = socket.getaddrinfo(host, port)[0]

    context = SSL.Context(SSL.SSLv23_METHOD)
    
    if addr[0] == socket.AF_INET6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        sock = SSL.Connection(context, sock)
        sock.connect((addr[4][0], port, 0, 0))
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock = SSL.Connection(context, sock)
        sock.connect((addr[4][0], port))

    sock.do_handshake()
    return sock.get_peer_certificate().digest('sha256').upper()


def get_tlsa(host, port):
    """
    Return TLSA dns field. If is not exist
    Arguments:
    - host: server host of server who propose tlsa
    - port: server port of server who propose tlsa
    """
    try:
        tlsa_name_field = '_' + str(port) + '._tcp.' + host
        #print(tlsa_name_field)
        tlsa_field = dns.resolver.resolve(tlsa_name_field, 'TLSA') #[0].to_text()
        #print(tlsa_field)
    except (dns.resolver.NXDOMAIN):
        return None
    except:
        return None
    return tlsa_field.split(' ')[3].upper()


def get_details(host):
    
    """
    parser = argparse.ArgumentParser(
        prog='check_dane_validity',
        description='Check if DANE field equals to server certificate')
    parser.add_argument(
        '-H', '--host',
        nargs='+',
        help='host to check')
    parser.add_argument(
        '-p', '--port',
        nargs='?',
        type=int,
        default=443,
        help='port with ssl certificate')
    """   
    args=argparse.Namespace(hosts=[host], port=443) 
    #args = parser.parse_args()
    #print(args)
    threats = []
    global_verification = True
    try:
        for host in args.host:
            remote_certificate = get_remote_certificate(host, args.port).decode("utf-8")
            #print(remote_certificate)
            
            remote_certificate = remote_certificate.replace(':', '')
            tlsa_field = get_tlsa(host, args.port)
            is_good_certificate = (tlsa_field == remote_certificate)
            #print(host + ' ' + str(is_good_certificate))
            global_verification = (global_verification & is_good_certificate)
            
    except: 
        is_good_certificate = False
        #print(host + ' ' + str(is_good_certificate))
    '''    
    if global_verification:
        sys.exit(0)
    else:
        sys.exit(2)
    '''
    if is_good_certificate == False:
        response = {
            "Details": "Not configured",
            "Status": "Warning",
            "Description": "TLSA record is not configured for the domain name."
        }
        threats.append(response)
    else:
        response = {
            "Details": "OK",
            "Status": "OK",
            "Description": "TLSA record is correctly configured."
        }    

    payload = {
        "Domain": host,
        "TLSA DNS record configuration":response,
        "SSL Threats": threats
    }
    
    return payload
    