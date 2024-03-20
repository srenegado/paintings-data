# driver.py
#
# ETL driver for work_subject table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.staging_driver import staging_driver
from pipelines.resources.connection import get_db_engine


def work_subject_transform(df: pd.DataFrame):
    """
    Transformations for work table.
    """
    df = df.drop_duplicates()
    return df


def work_subject_driver(engine):
    """
    Main driver for work_subject table.
    """
    staging_driver(engine, sourcename='subject', tablename='work_subject', transform=work_subject_transform, insert=False)


if __name__ == '__main__':
    work_subject_driver(get_db_engine())