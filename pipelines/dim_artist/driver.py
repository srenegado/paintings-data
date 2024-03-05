# driver.py
#
# ETL driver for dim_artist table in presentation area.
#
# Scott Renegado

from pipelines.resources.connection import get_db_engine

def dim_artist_driver():

    # Connect to database
    print("Establishing a database connection...")

    return

if __name__ == "__main__":
    engine = get_db_engine()
    dim_artist_driver(engine)