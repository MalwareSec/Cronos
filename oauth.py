import yaml
import getpass
import sys

def oauth():
    user = raw_input("Username: ")
    pwd = getpass.getpass("Password: ")

    with open("_config.yaml", "r") as config:
        cfg = yaml.load(config)

    username = cfg["server"]["username"]
    password = cfg["server"]["password"]

    if user == username and pwd == password:
        print "[*] Authenticated"
    else:
        print "Incorrect username or password!"
        sys.exit()

    config.close()
