# -*- coding: utf-8 -*-

import socket

socket.setdefaulttimeout(3)
sk = socket.socket()

sk.connect(('172.16.26.7', 1111))
sk.sendall("hack it and docker it!")
sk.recv()