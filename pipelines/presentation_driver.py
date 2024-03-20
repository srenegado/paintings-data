# presentation_driver.py
#
# Driver for presentation tables.
#
# Scott Renegado

from sqlalchemy import Engine

from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script
from pipelines.resources.sqlhandler import read_local_sql


def presentation_driver(engine: Engine, tablename: str):
    """
    Base driver for presentation tables.
    """

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the presentation table
    execute_script("pipelines/" + tablename + "/create.sql", con=conn)

    # Read table into dataframe
    df = read_local_sql("pipelines/" + tablename +"/load.sql", con=conn)

    # Load dataframe into table
    df.to_sql(tablename, con=conn, if_exists='append', index=False)

    # Create indexes
    execute_script("pipelines/" + tablename + "/indexes.sql", con=conn)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()