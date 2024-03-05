# driver.py
#
# ETL driver for work_subject table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def work_subject_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the work_subject table
    execute_script("pipelines/work_subject/drop.sql", con=conn)
    execute_script("pipelines/work_subject/create.sql", con=conn)

    # Read csv data into dataframe
    df = pd.read_csv(f'data/subject.csv')

    # Transformations
    df = df.drop_duplicates()

    # Load dataframe into table
    df.to_sql('work_subject', con=conn, if_exists='append', index=False)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    work_subject_driver(engine)