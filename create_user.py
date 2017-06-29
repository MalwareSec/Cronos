import yaml
import getpass
import sys
import uuid

def create():
    print "Welcome new user!"
    print "Please create your new account"
    print ""
    user_name = raw_input("Enter your username: ")
    pwd = getpass.getpass("Enter your password: ")
    pwd_confirmation = getpass.getpass("Please re-enter your password: ")
    if pwd == pwd_confirmation:
        print "Passwords match up!"
    else:
        print "Passwords did not match"
        sys.exit()
    srv = raw_input("Please enter the server IP: ")
    port = raw_input("Please enter the listening port: ")
    token = str(uuid.uuid4())

    new_server = {"server":{'host':srv, 'port':port, 'username':user_name, 'password':pwd, 'token':token}}

    with open("_config.yaml", "w") as config:
        yaml.dump(new_server, config, default_flow_style = False)

    print "User: " + user_name + " created succesfully!"
    print "Please store your token: " + token
