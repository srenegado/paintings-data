# connection.py
#
# Handler for database connections.
#
# Scott Renegado

from sqlalchemy import Engine
from sqlalchemy import create_engine
import json
import sys


def get_connection_config():
    """
    Get DB connection settings from config file.
    """
    # Load config file
    with open("pipelines/config.json") as conn_config:
        conn_config = json.load(conn_config)

    return conn_config


def get_connection_string(config):
    """
    Get connection string from config.
    """
    # Read config file
    user = config["user"]
    password = config["password"]
    host = config["host"]
    dbname = config["dbname"]

    # Setup string
    conn_string = f"postgresql://{user}:{password}@{host}/{dbname}"

    return conn_string


def get_db_connection(engine: Engine):
    """
    Get a new database connection with provided engine.
    Raise exception if connections fails.
    """
    try:
        # Create a new DB connection
        conn = engine.connect()
        return conn

    except Exception as e:
        print("There is an error with the config: ", e)
        sys.exit(1)


def get_db_engine():
    """
    Get a new database engine. Edit config file accordingly.
    """
    config = get_connection_config()
    conn_string = get_connection_string(config)
    engine = create_engine(conn_string)
    return engine
