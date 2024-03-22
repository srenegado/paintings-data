# driver.py
#
# ETL driver for product table to staging area.
#
# Scott Renegado

import pandas as pd
import numpy as np

from pipelines.staging_driver import staging_driver
from pipelines.resources.connection import get_db_engine


def product_transform(df: pd.DataFrame):
    """
    Transformations for product table.
    """
    df = df.drop_duplicates().rename(columns={"size_id": "canvas_id"})

    # Convert invalid canvas ids
    df["canvas_id"] = df["canvas_id"].replace("#VALUE!", 0).astype("str")

    # Convert decimal valued canvas ids
    df["canvas_id"] = (
        np.where(
            df["canvas_id"].str.contains(r"\d+\.\d+"),
            (df["canvas_id"].astype("float64") * 1000).astype(str),
            df["canvas_id"],
        )
        .astype("float64")
        .astype("int64")
    )
    return df


def product_driver(engine):
    """
    Main driver for product table.
    """
    staging_driver(
        engine,
        sourcename="product_size",
        tablename="product",
        transform=product_transform,
        insert=False,
    )


if __name__ == "__main__":
    product_driver(get_db_engine())
