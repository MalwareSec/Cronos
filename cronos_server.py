#!/usr/bin/Python2.7.12
import socket
import sys
import getopt
import threading
import subprocess
from var import *

def handle_client(client_socket):
        request = client_socket.recv(1024)
        print "[*] Recieved: " + request
        client_socket.send("ACK")
        client_socket.close()

def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, int(server_port)))
    server.listen(5)
    print "[*] Listening on: " + host + ":" + server_port

    while 1:
        client, addr = server.accept()
        print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

#tcp_server()

def client_handler(client_socket):
    #global UPLOAD
    #global EXECUTE
    global COMMAND
    COMMAND = True

    '''
    # check for upload
    if len(UP_DEST):
        file_buf = ''

        # keep reading data until no more data is available
        while 1:
            data = client_socket.recv(1024)
            if data:
                file_buffer += data
            else:
                break

        # try to write the bytes (wb for binary mode)
        try:
            with open(UP_DEST, 'wb') as f:
                f.write(file_buffer)
                client_socket.send('File saved to %s\r\n' % UP_DEST)
        except:
            client_socket.send('Failed to save file to %s\r\n' % UP_DEST)
    '''

    # Check for command execution:
    #if len(EXECUTE):
        #output = run_command(EXECUTE)
        #client_socket.send(output)

    # Go into a loop if a command shell was requested
    if COMMAND:
        while True:
            # show a prompt:
            client_socket.send('NETCAT: ')
            cmd_buffer = ''

            # scans for a newline character to determine when to process a command
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                print "[*] Recieved: " + cmd_buffer

            # send back the command output
            response = run_command(cmd_buffer)
            client_socket.send(response)

def server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, int(server_port)))
        sock.listen(100)
        print "[+] Listening for connection ..."
    except Exception, e:
        print "[-] Connection Failed: " + str(e)
        sys.exit(1)


    while True:
        client, addr = sock.accept()
        #client_socket, addr = sock.accept()
        print "[+] Connection Established!"
        print "[*] Accepted connection from: %s:%d" %(addr[0], addr[1])
        # spin off thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client,))
        client_thread.start()

server_loop()
