# driver.py
#
# Driver for dim_artist table in presentation area.
#
# Scott Renegado

from pipelines.resources.connection import get_db_engine
from pipelines.presentation_driver import presentation_driver


def dim_artist_driver(engine):
    """Driver for dim_artist table."""
    presentation_driver(engine, "dim_artist")


if __name__ == "__main__":
    dim_artist_driver(get_db_engine())
