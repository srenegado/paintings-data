# staging_driver.py
#
# ETL driver for staging tables.
#
# Scott Renegado

import pandas as pd
from typing import Callable
from sqlalchemy import Engine

from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def staging_driver(
    engine: Engine, 
    sourcename: str, 
    tablename: str, 
    transform: Callable[[pd.DataFrame], pd.DataFrame], 
    insert: bool = False   
):
    """
    Base driver for staging tables.
    """

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the staging table
    execute_script("pipelines/" + tablename + "/drop.sql", con=conn)
    execute_script("pipelines/" + tablename + "/create.sql", con=conn)
    if insert: execute_script("pipelines/" + tablename + "/insert.sql", con=conn)

    # Read csv data into dataframe
    df = pd.read_csv(f'data/' + sourcename + '.csv')

    # Perform transformations
    df = transform(df)

    # Load dataframe into table
    df.to_sql(tablename, con=conn, if_exists='append', index=False)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()