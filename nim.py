#!/usr/bin/env python3

import socket
import sys
from sendall import my_sendall
import struct 
from clientfunctions import game_seq_progress

HOST = socket.gethostname() # The server's hostname or IP address
PORT = 6444        # The port used by the server

n = len(sys.argv) 

if n == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except socket.gaierror as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)
        
    with s:
        while True:
            data = s.recv(1024)

            if (len(data) == 0):
                print("Disconnected from server")
                break

            res = struct.unpack("iiii", data)
            message_type, heap_A, heap_B, heap_C = res
            game_continues = game_seq_progress(s, message_type, heap_A, heap_B, heap_C)

            if game_continues is not True:
                break
            

