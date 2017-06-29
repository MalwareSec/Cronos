import socket
from var import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(server_port)

def ServerBind():
    s.bind((host, port))
    s.listen(2)
    print "[*] Spinning up server on " + host
    print "Listening on port " + str(port) + " ... "

def ServerAccept():
    (client, (ip, port)) = s.accept()
    print " Received connection from: ", ip

    while True:
        command = raw_input('~Cronos: ')
        client.send(command)
        response = client.recv(2048)
        if response != "* Error":
            print response
        else:
            print "[*] Error encountered in command"
            print "Closing connection"
            s.close()
            break

def Main():
    ServerBind()
    ServerAccept()
    print "Closing connection"
    s.close()
