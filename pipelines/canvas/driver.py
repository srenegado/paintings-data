# driver.py
#
# ETL driver for canvas table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script


def canvas_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the canvas table
    execute_script("pipelines/canvas/drop.sql", con=conn)
    execute_script("pipelines/canvas/create.sql", con=conn)
    execute_script("pipelines/canvas/insert.sql", con=conn)

    # Read csv data into dataframe
    df = pd.read_csv(f'data/canvas_size.csv')

    # Transformations
    df = (
        df.drop_duplicates()
        .rename(columns={'size_id': 'id'})
    )

    # Insert missing canvas data by infering from products
    product_df = pd.read_csv(f'data/product_size.csv')
    size_id_col = product_df['size_id']

    single_dim_ids = size_id_col[size_id_col.str.match(r'\d\d\.\d+')].reset_index(drop=True)
    double_dim_ids = size_id_col[size_id_col.str.match(r'\d\d\d\d\.\d+')].reset_index(drop=True)

    inserts_df1 = pd.DataFrame()
    inserts_df1['id'] = (
        (single_dim_ids
         .astype('float64') * 1000)
         .astype('int64')
    )
    inserts_df1['width'] = single_dim_ids.astype(str)
    inserts_df1['height'] = None
    inserts_df1['label'] = inserts_df1['width'] + '" Long Edge'
    inserts_df1 = inserts_df1.drop_duplicates()

    inserts_df2 = pd.DataFrame()
    inserts_df2['id'] = (
        (double_dim_ids
         .astype('float64') * 1000)
         .astype('int64')
    )
    inserts_df2['width'] = double_dim_ids.str.extract(r'(\d\d)')
    inserts_df2['height'] = double_dim_ids.str.extract(r'(\d\d\.\d+)')
    inserts_df2['label'] = inserts_df2['width'] + '" x ' + inserts_df2['height'] + '"'
    inserts_df2 = inserts_df2.drop_duplicates()

    df = pd.concat([df, inserts_df1, inserts_df2])

    # Load dataframe into table
    df.to_sql('canvas', con=conn, if_exists='append', index=False)
    
    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    canvas_driver(engine)