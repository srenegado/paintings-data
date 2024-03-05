# driver.py
#
# ETL driver for museum_hours table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def museum_hours_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the museum_hours table
    execute_script("pipelines/museum_hours/drop.sql", con=conn)
    execute_script("pipelines/museum_hours/create.sql", con=conn)
    
    # Read csv data into dataframe
    df = pd.read_csv(f'data/museum_hours.csv')

    # Transformations
    df = df.drop_duplicates()
    
    df['close'] = (
        df['close'].replace('08 :00:PM', '08:00:PM')
        .apply(lambda t: pd.to_datetime(t, format='%I:%M:%p'))
    )

    df['open'] = pd.to_datetime(df['open'], format='%I:%M:%p')

    # Load dataframe into table
    df.to_sql('museum_hours', con=conn, if_exists='append', index=False)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    museum_hours_driver(engine)