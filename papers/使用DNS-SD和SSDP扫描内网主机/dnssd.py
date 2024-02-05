#/usr/bin/python3
#!coding=utf-8

import socket
import sys
from scapy.all import raw, DNS, DNSQR

def get_service_info(sock, target, resp):
    service = (resp.an.rdata).decode()

    # query each service detail informations
    req = DNS(id=0x0001, rd=1, qd=DNSQR(qtype="PTR", qname=service))
    #req.show()
    sock.sendto(raw(req), target)
    data, _ = sock.recvfrom(1024)
    resp = DNS(data)
    #resp.show()
    
    # parse additional records
    repeat = {}
    for i in range(0, resp.arcount):
        rrname = (resp.ar[i].rrname).decode()
        rdata  = resp.ar[i].rdata

        if rrname in repeat:
            continue
        repeat[rrname] = rdata

        if hasattr(resp.ar[i], "port"):
            rrname += (" " + str(resp.ar[i].port))

        if rrname.find("._device-info._tcp.local.") > 0:
            print(" "*4, rrname, rdata)
        else:
            print(" "*4, rrname)
# end get_service_info()

def dnssd_scan(target):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    # query all service name
    req = DNS(id=0x0001, rd=1, qd=DNSQR(qtype="PTR", qname="_services._dns-sd._udp.local"))
    #req.show()
    try:
        sock.sendto(raw(req), target)
        data, _ = sock.recvfrom(1024)
    except KeyboardInterrupt:
        exit(0)
    except:
        print("[%s] OFFLINE" % target[0])
        return
    resp = DNS(data)
    #resp.show()

    print("[%s] ONLINE" % target[0])
    for i in range(0, resp.ancount):
        get_service_info(sock, target, resp)
# end dnssd_scan()

if __name__ == "__main__":
    if not (len([sys.argv]) > 0 and sys.argv[1].endswith(".0")):
        print("usage: python3 dnssd.py 192.168.1.0")
        exit(0)

    print("dnssd scan start")
    network = sys.argv[1].rstrip("0")

    # scan local network
    for i in range(1, 256):
        target = (network + str(i), 5353)
        dnssd_scan(target)

    print("dnssd scan end")
# end main()
