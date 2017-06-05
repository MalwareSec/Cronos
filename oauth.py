import yaml
import getpass
import uuid
import sys

def oauth():
    #def main():
    user = raw_input("Username: ")
    pwd = getpass.getpass("Password: ")
    key = raw_input("Please enter your token: ")

    with open("_config.yaml", "r") as config:
        cfg = yaml.load(config)

    while True:
        try:
            username = cfg[user]["username"]
            password = cfg[user]["password"]
            uid = cfg[user]["token"]

            if user == username and pwd == password and key == uid:
                print "[*] Authenticated"
                break
            else:
                print "Incorrect username or password or token!"
                sys.exit()
        except KeyError as err:
            print "Incorrect username or password or token!"
            sys.exit()


    config.close()
