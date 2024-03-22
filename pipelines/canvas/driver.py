# driver.py
#
# ETL driver for canvas table to staging area.
#
# Scott Renegado

import pandas as pd

from pipelines.resources.connection import get_db_engine
from pipelines.staging_driver import staging_driver


def canvas_transform(df: pd.DataFrame):
    """
    Transformations for canvas table.
    """
    df = df.drop_duplicates().rename(columns={"size_id": "id"})

    # Insert missing canvas data by infering from source product_size
    product_df = pd.read_csv(f"data/product_size.csv")
    size_id_col = product_df["size_id"]

    # Read size_ids that are decimals
    single_dim_ids = size_id_col[size_id_col.str.match(r"\d\d\.\d+")].reset_index(
        drop=True
    )
    double_dim_ids = size_id_col[size_id_col.str.match(r"\d\d\d\d\.\d+")].reset_index(
        drop=True
    )

    # Decimal ids are converted to integers by multiplying them by 1000
    inserts_df1 = pd.DataFrame()
    inserts_df1["id"] = (single_dim_ids.astype("float64") * 1000).astype("int64")
    inserts_df1["width"] = single_dim_ids.astype(str)
    inserts_df1["height"] = None
    inserts_df1["label"] = inserts_df1["width"] + '" Long Edge'
    inserts_df1 = inserts_df1.drop_duplicates()

    inserts_df2 = pd.DataFrame()
    inserts_df2["id"] = (double_dim_ids.astype("float64") * 1000).astype("int64")
    inserts_df2["width"] = double_dim_ids.str.extract(r"(\d\d)")
    inserts_df2["height"] = double_dim_ids.str.extract(r"(\d\d\.\d+)")
    inserts_df2["label"] = inserts_df2["width"] + '" x ' + inserts_df2["height"] + '"'
    inserts_df2 = inserts_df2.drop_duplicates()

    df = pd.concat([df, inserts_df1, inserts_df2])
    return df


def canvas_driver(engine):
    """
    Main driver for artist table.
    """
    staging_driver(
        engine,
        sourcename="canvas_size",
        tablename="canvas",
        transform=canvas_transform,
        insert=True,
    )


if __name__ == "__main__":
    canvas_driver(get_db_engine())
