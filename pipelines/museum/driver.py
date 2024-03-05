# driver.py
#
# ETL driver for museum table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def museum_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the museum table
    execute_script("pipelines/museum/drop.sql", con=conn)
    execute_script("pipelines/museum/create.sql", con=conn)
    execute_script("pipelines/museum/insert.sql", con=conn)

    # Read csv data into dataframe
    df = pd.read_csv(f'data/museum.csv')

    # Transformations
    df = (
        df.drop(columns=['url'])
        .rename(columns={'museum_id': 'id'})
        .drop_duplicates()
    )

    # Load dataframe into table
    df.to_sql('museum', con=conn, if_exists='append', index=False)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    museum_driver(engine)