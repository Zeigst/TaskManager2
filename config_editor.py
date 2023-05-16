from configparser import ConfigParser

config = ConfigParser()

config["POSTGRESQL"] = {
    "Host": "localhost",
    "Port": "5432",
    "Username": "postgres",
    "Password": "CHM19902",
    "Database": "taskmanager"
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)