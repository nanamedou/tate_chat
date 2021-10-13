#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

HOST = 'localhost'
PORT = 51234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))
