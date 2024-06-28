from mongoengine import connect
import configparser
import os


def get_connection():

    config_file = '/Users/kozlovalex/Documents/GitHub/Python_web_09/connection/config.ini'

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    config = configparser.ConfigParser()
    config.read(config_file)

    try:

        mongo_user = config.get('DB', 'user')
        mongo_pass = config.get('DB', 'pass')
        db_name = config.get('DB', 'db_name')
        domain = config.get('DB', 'domain')

    except configparser.NoSectionError as e:
        raise ValueError(f"Missing section in configuration file: {e.section}")

    uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/?retryWrites=true&w=majority&appName={db_name}"

    return connect(db=db_name, host=uri)

