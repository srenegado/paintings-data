# sqlhandler.py
#
# Handler for executing sql scripts.
#
# Scott Renegado

from sqlalchemy import Connection
from sqlalchemy import text
import pandas as pd


def load_script(script_filename):
    """
    Load sql script and return a text-formatted string.
    """
    with open(script_filename) as f:
        create_script = text(f.read())
    return create_script


def execute_script(script_filename, con: Connection):
    """
    Read and execute SQL using provided DB connection.
    """
    create_script = load_script(script_filename)
    con.execute(create_script)


def read_local_sql(script_filename, con: Connection):
    """
    Read a local SQL script into a dataframe.
    See pandas.read_sql.
    """
    script = load_script(script_filename)
    return pd.read_sql(script, con=con)
