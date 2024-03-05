# driver.py
#
# ETL driver for product table to staging area.
#
# Scott Renegado

import pandas as pd
import numpy as np

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def product_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the product table
    execute_script("pipelines/product/drop.sql", con=conn)
    execute_script("pipelines/product/create.sql", con=conn)

    # Read csv data into dataframe
    df = pd.read_csv(f'data/product_size.csv')

    # Transformations
    df = (
        df.drop_duplicates()
        .rename(columns={'size_id': 'canvas_id'})
    )

    # Convert invalid canvas ids
    df['canvas_id'] = (
        df['canvas_id']
        .replace('#VALUE!', 0)
        .astype('str')
    )

    # Convert decimal valued canvas ids
    df['canvas_id'] = (
        np.where(
            df['canvas_id'].str.contains(r'\d+\.\d+'), 
            (df['canvas_id'].astype('float64') * 1000).astype(str), 
            df['canvas_id']
        )
        .astype('float64')
        .astype('int64')
    )

    # Load dataframe into table
    df.to_sql('product', con=conn, if_exists='append', index=False)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    product_driver(engine)