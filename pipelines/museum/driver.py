# driver.py
#
# ETL driver for museum table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.staging_driver import staging_driver
from pipelines.resources.connection import get_db_engine


def museum_transform(df: pd.DataFrame):
    """
    Transformations for artist table.
    """
    df = df.drop(columns=["url"]).rename(columns={"museum_id": "id"}).drop_duplicates()
    return df


def museum_driver(engine):
    """
    Main driver for museum table.
    """
    staging_driver(
        engine,
        sourcename="museum",
        tablename="museum",
        transform=museum_transform,
        insert=True,
    )


if __name__ == "__main__":
    museum_driver(get_db_engine())
