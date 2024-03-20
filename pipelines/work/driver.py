# driver.py
#
# ETL driver for work table to staging area.
#
# Scott Renegado

import pandas as pd
import numpy as np

from pipelines.staging_driver import staging_driver
from pipelines.resources.connection import get_db_engine


def work_transform(df: pd.DataFrame):
    """
    Transformations for work table.
    """
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
    return df


def work_driver(engine):
    """
    Main driver for work table.
    """
    staging_driver(engine, sourcename='work', tablename='work', transform=work_transform, insert=False)


if __name__ == '__main__':
    work_driver(get_db_engine())