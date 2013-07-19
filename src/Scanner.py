#! /usr/bin/env python

import socket

host = "192.168.111.138"
ports = []

for i in xrange(65000):
    ports.append(i)

open_ports = []

for port in ports:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(0.01)

    try:
        sock.connect((host,port))
    except:
        print("Port %s is closed" % port )
    else:
        open_ports.append(port)
        print("Port %s is open" % port)

    sock.close()
