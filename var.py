#!/usr/bin/Python2.7.12
import yaml

with open("_config.yaml", "r") as data:
    cfg = yaml.load(data)

host_data = []

host = cfg["server"]["host"]
server_port = cfg["server"]["port"]
server_user = cfg["server"]["username"]
server_pwd = cfg["server"]["password"]

host_data = [host, server_port, server_user, server_pwd]

data.close()
