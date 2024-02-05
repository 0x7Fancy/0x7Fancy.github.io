#/usr/bin/python3
#!coding=utf-8

import socket
import struct

address = ("239.255.255.250", 1900)
result = {}

def get_serv_ua(resp):
    lines = resp.split("\r\n")
    for i in lines:
        array = i.split(":")
        if array[0].upper() == "SERVER" or array[0].upper() == "USER-AGENT":
            return array[1]
    # end-for
# end get_serv_ua()


def ssdp_scan():
    print("[scan mode]")
    req = b'M-SEARCH * HTTP/1.1\r\nHost: 239.255.255.250:1900\r\nST:ssdp:all\r\nMan: "ssdp:discover"\r\nMX:1\r\n\r\n'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    # send "ssdp:all" query request
    sock.sendto(req, address)

    # receive and print
    while True:
        try:
            resp, raddr = sock.recvfrom(1024)
        except:
            break
        if raddr[0] not in result:
            data = get_serv_ua(resp.decode())
            result[raddr[0]] = data
            print(raddr[0], data)
    # end-while
# ssdp_scan()

def ssdp_sniffer():
    print("[sniffer mode] (stop by Ctrl-C)")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)

    # join the multicast group
    maddr = struct.pack("4sl", socket.inet_aton("239.255.255.250"), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, maddr)

    # receive and print
    while True:
        try:
            resp, raddr = sock.recvfrom(1024)
        except:
            break
        if raddr[0] not in result:
            data = get_serv_ua(resp.decode())
            result[raddr[0]] = data
            print(raddr[0], data)
# ssdp_sniffer()

if __name__ == "__main__":
    print("ssdp scan start")

    ssdp_scan()
    ssdp_sniffer()

    print("ssdp scan end")
# end main()
