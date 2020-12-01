#!/usr/bin/env python3

import socket
from sendall import my_sendall
import sys
from serverfunctions import *
import struct

HOST = ''  # Standard loopback interface address (localhost)
PORT = 6444        # Port to listen on (non-privileged ports are > 1023)


if len(sys.argv) == 5:
    PORT = int(sys.argv[4])  

heap_dict = { "A": int(sys.argv[1]),
             "B": int(sys.argv[2]),
            "C": int(sys.argv[3]) }
while True:  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
        except socket.error as exc:
            print("Caught exception socket.error : {prob}".format(prob = exc))
            sys.exit(1)

        with conn:
            '''In transmission protocol 0:INTIAL_MESSAGE, 1:LEGAL, 2:ILLEGAL, 3:WIN, 4:LOSE, 5:QUIT, 6:INVALID INPUT'''
            print('Connected by', addr)
            initial_data = struct.pack('iiii', 0, heap_dict['A'], heap_dict['B'], heap_dict['C'])   
            my_sendall(conn, initial_data)
            while True:
                data = conn.recv(1024)

                if not data:
                    break

                message_type, heap_num, num_taken = struct.unpack("iii", data)
            
                if (message_type == 5):
                    data_to_send = struct.pack("iiii", 5, 0, 0, 0)
                    my_sendall(conn, data_to_send)
                    reset_heap(heap_dict, int(sys.argv[1]), int(sys.argv[2]) , int(sys.argv[3]))
                    break

                elif (message_type == 6):
                    binary_data = struct.pack("i i i i", 6, heap_dict['A'], heap_dict['B'], heap_dict['C'])
                    my_sendall(conn, binary_data)

                else:        
                    heap = bring_heap_letter(heap_num)
                    validity = choice_validity(heap_dict, heap, num_taken)
                    if validity == "LEGAL":
                        if heap_sum(heap_dict) == 0:
                            binary_data = struct.pack("i i i i", 3, heap_dict['A'], heap_dict['B'], heap_dict['C'])
                            my_sendall(conn, binary_data)
                            reset_heap(heap_dict, int(sys.argv[1]), int(sys.argv[2]) , int(sys.argv[3]))
                            break
                        elif heap_sum(heap_dict) == 1:
                            binary_data = struct.pack("i i i i", 4, heap_dict['A'], heap_dict['B'], heap_dict['C'])
                            my_sendall(conn, binary_data)
                            reset_heap(heap_dict, int(sys.argv[1]), int(sys.argv[2]) , int(sys.argv[3]))
                            break
                        else:
                            server_heap_choice(heap_dict)
                            binary_data = struct.pack("i i i i", 1, heap_dict['A'], heap_dict['B'], heap_dict['C']) 
                            my_sendall(conn, binary_data)
                    elif validity == "ILLEGAL":
                        server_heap_choice(heap_dict)
                        binary_data = struct.pack("i i i i", 2, heap_dict['A'], heap_dict['B'], heap_dict['C']) 
                        my_sendall(conn,binary_data)