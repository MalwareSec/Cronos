import yaml
import getpass
import uuid
import sys

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
token = uuid.uuid4()
key = str(token)
print "This is your ID token: " + key + " Please save this in your local directory."

#num = uuid.uuid4()
#uid = str(num)
new_user = {user_name:{'username':user_name, 'password':pwd, 'token':key}}


with open("_config.yaml", "a") as config:
    yaml.dump(new_user, config, default_flow_style = False)

print "User: " + user_name + " created succesfully!"
