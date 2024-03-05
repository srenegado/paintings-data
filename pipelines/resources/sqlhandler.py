# sqlhandler.py
#
# Handler for executing sql scripts.
#
# Scott Renegado

from sqlalchemy import text


def load_script(script_filename):
    """
    Load sql script and return a text-formatted string.
    """
    with open(script_filename) as f:
        create_script = text(f.read())
    return create_script


def execute_script(script_filename, con):
    """
    Read and execute SQL using provided DB connection.
    """
    create_script = load_script(script_filename)
    con.execute(create_script)