# driver.py
#
# ETL driver for work table to staging area.
#
# Scott Renegado

import pandas as pd
import numpy as np

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def work_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the work table
    execute_script("pipelines/work/drop.sql", con=conn)
    execute_script("pipelines/work/create.sql", con=conn)

    # Read csv data into dataframe
    df = pd.read_csv(f'data/work.csv')

    # Transformations
    df = (
        df.drop_duplicates()
        .rename(columns={'work_id': 'id'})
    )

    # Change nulls in museum_id to default value
    df['museum_id'] = (
        df['museum_id']
        .replace(np.NaN, 0) 
        .apply(lambda string: pd.to_numeric(string))
        .astype('int64')
    )

    # Load dataframe into table
    df.to_sql('work', con=conn, if_exists='append', index=False)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    work_driver(engine)