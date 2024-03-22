# driver.py
#
# ETL driver for museum_hours table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.staging_driver import staging_driver
from pipelines.resources.connection import get_db_engine


def museum_hours_transform(df: pd.DataFrame):
    """
    Transformations for museum_hours table.
    """
    df = df.drop_duplicates().copy()

    df["close"] = (
        df["close"]
        .replace("08 :00:PM", "08:00:PM")
        .apply(lambda t: pd.to_datetime(t, format="%I:%M:%p"))
    )

    df["open"] = pd.to_datetime(df["open"], format="%I:%M:%p")

    return df


def museum_hours_driver(engine):
    """
    Main driver for museum_hours table.
    """
    staging_driver(
        engine,
        sourcename="museum_hours",
        tablename="museum_hours",
        transform=museum_hours_transform,
        insert=False,
    )


if __name__ == "__main__":
    engine = get_db_engine()
    museum_hours_driver(engine)
