import yaml
import getpass
import uuid
import sys

#def main():
user = raw_input("Username: ")
pwd = getpass.getpass("Password: ")
key = raw_input("Please enter your token: ")

    #oauth(user, pwd, key)

#def oauth(user, pwd, key):
with open("_config.yaml", "r") as config:
    cfg = yaml.load(config)

    #if cfg[user]["username"] == True:
username = cfg[user]["username"]
    #else:
        #print "User not in the system!"
        #sys.exit()
password = cfg[user]["password"]
uid = cfg[user]["token"]

if user == username and pwd == password and key == uid:
    print "Welcome!"
else:
    print "Incorrect username or password or token!"
    sys.exit()

config.close()

print "[*] Authenticated"
#main()
