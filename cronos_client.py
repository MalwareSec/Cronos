#!/usr/bin/Python2.7.12
import socket
import sys
import threading
import subprocess
from var import *

port = int(server_port)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host,port))
        print "Connected to server!"
        #STDN
        if len(buffer):
            client.send(buffer)

        while True:
            # now wait for data back
            recv_len = 1
            response = ''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response+= data

                if recv_len < 4096:
                    break

            print response,
            # wait for more input
            buffer = raw_input('')
            buffer += '\n'
            # send it off
            client.send(buffer)
    except:
        # just catch generic errors - you can do your homework to beef this up
            print '[*] Exception! Exiting.'
            # teardown the connection
            client.close()

def main():
        buffer = raw_input("Enter command: ")
        client_sender(buffer)

main()
