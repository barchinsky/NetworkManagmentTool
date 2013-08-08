#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Retrieve device ports from vxemulator

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 9090))
sock.listen(10)

while True:
    conn, addr = sock.accept()
    data = conn.recv(8192)
    out = open('devices.txt','w')
    if not data:
        continue
    else:
        print data
        # make timestamp
        
        out = open('devices.txt','w')
        out.write(data)
        out.close()

conn.close()
