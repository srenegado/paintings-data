# driver.py
#
# ETL driver for artist table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def artist_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the artist table
    execute_script("pipelines/artist/drop.sql", con=conn)
    execute_script("pipelines/artist/create.sql", con=conn)

    # Read csv data into dataframe
    df = pd.read_csv(f'data/artist.csv')

    # Transformations
    df = (
        df.drop(columns=['first_name', 'middle_names', 'last_name'])
        .rename(columns={'artist_id': 'id', 'birth': 'birth_year', 'death': 'death_year'})
        .drop_duplicates()
    )

    # Load dataframe into table
    df.to_sql('artist', con=conn, if_exists='append', index=False)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    artist_driver(engine)