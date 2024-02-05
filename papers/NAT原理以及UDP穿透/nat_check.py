#!/usr/bin/python3
#coding=utf-8

import socket
import sys

def server(addr):
    print("[NAT CHECK launch as server on %s]" % str(addr))

    # listen UDP service
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)

    # [1. check "Open Internet" and "Symmetric NAT"]
    # recevie client request and return export ip
    data, cconn = sock.recvfrom(1024)
    print("server get client info: %s" % str(cconn))
    data = "%s:%d" % (cconn[0], cconn[1])
    sock.sendto(data.encode("utf-8"), cconn)

    # receive assist data about client another export ip
    data, aconn = sock.recvfrom(1024)
    print("server get client info (from assist): %s" % data.decode("utf-8"))
    sock.sendto(data, cconn)

    # [2. check "Full-Cone NAT", "Restricted NAT" and "Restricted-Port NAT"]
    # recevie client request
    data, cconn = sock.recvfrom(1024)
    print("server get client info: %s" % str(cconn))
    # receive assist data about client another export ip
    data, aconn = sock.recvfrom(1024)
    print("server get client info (from assist): %s" % data.decode("utf-8"))

    # send data to client through (assist get) export ip
    print("send packet for testing Full-Cone NAT")
    array = data.decode("utf-8").split(":")
    caconn = (array[0], int(array[1]))
    sock.sendto("TEST FOR FULL-CONE NAT".encode("utf-8"), caconn)

    # send data to client through (server get) export ip and with different port
    sock.recvfrom(1024) # NEXT flag
    print("send packet for testing Restricted NAT")
    cdconn = (cconn[0], cconn[1] - 1)
    sock.sendto("TEST FOR Restricted NAT".encode("utf-8"), cdconn)

    # send data to client through (server get) export ip
    sock.recvfrom(1024) # NEXT flag
    print("send packet for testing Restricted-Port NAT")
    sock.sendto("TEST FOR Restricted-Port NAT".encode("utf-8"), cconn)
# server()

def assist(addr, serv):
    print("[NAT CHECK launch as assist on %s && server=%s]" %
                                                    (str(addr), str(serv)))

    # listen UDP service
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(addr)

    # [1. check "Open Internet" and "Symmetric NAT"]
    # recevie client request and forward to server
    data, conn = sock.recvfrom(1024)
    print("assist get client info: %s" % str(conn))
    data = "%s:%d" % (conn[0], conn[1])
    sock.sendto(data.encode("utf-8"), serv)

    # [2. check "Full-Cone NAT", "Restricted NAT" and "Restricted-Port NAT"]
    # recevie client request and forward to server
    data, conn = sock.recvfrom(1024)
    print("assist get client info: %s" % str(conn))
    data = "%s:%d" % (conn[0], conn[1])
    sock.sendto(data.encode("utf-8"), serv)
# assist()

def client(serv, ast):
    print("[NAT CHECK launch as client to server=%s && assist=%s]" %
                                                    (str(serv), str(ast)))

    # [1. check "Open Internet" and "Symmetric NAT"]
    print("send data to server and assist")
    # get local address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(serv)
    localaddr = sock.getsockname()

    # send data to server and assist with same socket
    # and register so that the server can obtain the export ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("register".encode("utf-8"), serv)
    sock.sendto("register".encode("utf-8"), ast)

    # receive export ip from server
    data, conn = sock.recvfrom(1024)
    exportaddr = data.decode("utf-8")
    print("get export ip: %s, localaddr: %s" % (exportaddr, str(localaddr)))

    # check it is "Open Internet"
    if exportaddr.split(":")[0] == localaddr[0]:
        print("[Open Internet]")
        return
    # end if

    # receive another export ip (assist) from server
    data, conn = sock.recvfrom(1024)
    anotheraddr = data.decode("utf-8")
    print("get export ip(assist): %s, export ip(server): %s" % (anotheraddr, exportaddr))

    # check it is "Symmetric NAT"
    if exportaddr != anotheraddr:
        print("[Symmetric NAT]")
        return
    # end if

    # [2. check "Full-Cone NAT", "Restricted NAT" and "Restricted-Port NAT"]
    # send data to server and assist with different socket
    # receive the data sent back by the server through the export ip(assist) mapping
    ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ssock.sendto("register".encode("utf-8"), serv)
    asock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    asock.sendto("register".encode("utf-8"), ast)

    asock.settimeout(5)
    try:
        data, conn = asock.recvfrom(1024)
        print("[Full-Cone NAT]")
        return
    except:
        pass

    # receive the data sent back by the server with different port
    ssock.sendto("NEXT".encode("utf-8"), serv)
    ssock.settimeout(5)
    try:
        data, conn = ssock.recvfrom(1024)
        print("[Restricted NAT]")
        return
    except:
        pass

    # receive the data sent back by the server
    ssock.sendto("NEXT".encode("utf-8"), serv)
    ssock.settimeout(5)
    try:
        data, conn = ssock.recvfrom(1024)
        print("[Restricted-Port NAT]")
    except:
        print("[Unknown, something error]")
# client()

def usage():
    print("Usage:")
    print("  python3 nat_check.py server [ip:port]")
    print("  python3 nat_check.py assist [ip:port] [server]")
    print("  python3 nat_check.py client [server] [assist]")
# end usage()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        exit(0)
    # end if

    role = sys.argv[1]
    array = sys.argv[2].split(":")
    address1 = (array[0], int(array[1]))
    if role == "assist" or role == "client":
        if len(sys.argv) > 3:
            array = sys.argv[3].split(":")
            address2 = (array[0], int(array[1]))
        else:
            usage()
            exit(0)
    # end if

    # server/client launch
    if role == "server":
        server(address1)
    elif role == "assist":
        assist(address1, address2)
    elif role == "client":
        client(address1, address2)
    else:
        usage()
# end main()
