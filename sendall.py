import socket

def my_sendall(sock, data):
    if (len(data) == 0):
        return None
    ret = sock.send(data)
    return my_sendall(sock, data[ret:])