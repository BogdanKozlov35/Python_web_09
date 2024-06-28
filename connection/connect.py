from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('connection/config.ini')


def get_connection():
    mongo_user = config.get('DB', 'user')
    mongo_pass = config.get('DB', 'pass')
    db_name = config.get('DB', 'db_name')
    domain = config.get('DB', 'domain')

    uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/?retryWrites=true&w=majority&appName={db_name}"

    return connect(db=db_name, host=uri)

