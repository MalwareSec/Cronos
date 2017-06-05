#!/usr/bin/Python2.7.12
import yaml

with open("_config.yaml", "r") as data:
    cfg = yaml.load(data)

target_data = []
host_data = []

target = cfg["target"]["host"]
target_port = cfg["target"]["port"]
target_user = cfg["target"]["username"]
target_pwd = cfg["target"]["password"]

target_data = [target, target_port, target_user, target_pwd]

host = cfg["server"]["host"]
server_port = cfg["server"]["port"]
server_user = cfg["server"]["username"]
server_pwd = cfg["server"]["password"]

host_data = [host, server_port, server_user, server_pwd]

data.close()
