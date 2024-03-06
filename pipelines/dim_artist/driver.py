# driver.py
#
# Driver for dim_artist table in presentation area.
#
# Scott Renegado

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script
from pipelines.resources.sqlhandler import read_local_sql


def dim_artist_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the dim_artist table
    execute_script("pipelines/dim_artist/create.sql", con=conn)

    # Read table into dataframe
    df = read_local_sql("pipelines/dim_artist/load.sql", con=conn)

    # Add surrogate key
    df['dim_artist_skey'] = df.index + 1

    # Load dataframe into table
    df.to_sql('dim_artist', con=conn, if_exists='append', index=False)

    # Create indexes
    execute_script("pipelines/dim_artist/indexes.sql", con=conn)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    dim_artist_driver(engine)