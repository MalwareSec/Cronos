#Cronos Main
from banner import banner
from oauth import *
from var import *

oauth()

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
