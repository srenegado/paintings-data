# driver.py
#
# ETL driver for dim_artist table in presentation area.
#
# Scott Renegado

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import read_local_sql

def dim_artist_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the dim_artist table
    df = read_local_sql("pipelines/dim_artist/load.sql", con=conn)

    print(df)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()

    return

if __name__ == "__main__":
    engine = get_db_engine()
    dim_artist_driver(engine)