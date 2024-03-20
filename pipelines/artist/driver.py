# driver.py
#
# ETL driver for artist table to staging area.
#
# Scott Renegado

import pandas as pd
from pipelines.resources.connection import get_db_engine
from pipelines.staging_driver import staging_driver


def artist_transform(df: pd.DataFrame):
    """
    Transformations for artist table.
    """
    df = (
        df.drop(columns=['first_name', 'middle_names', 'last_name'])
        .rename(columns={'artist_id': 'id', 'birth': 'birth_year', 'death': 'death_year'})
        .drop_duplicates()
    )
    return df


def artist_driver(engine):
    """
    Main driver for artist table.
    """
    staging_driver(engine, sourcename='artist', tablename='artist', transform=artist_transform, insert=False)


if __name__ == '__main__':
    artist_driver(get_db_engine())