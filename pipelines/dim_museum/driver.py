# driver.py
#
# Driver for dim_museum table in presentation area.
#
# Scott Renegado

from pipelines.presentation_driver import presentation_driver
from pipelines.resources.connection import get_db_engine


def dim_museum_driver(engine):
    """Driver for dim_museum table."""
    presentation_driver(engine, 'dim_museum')


if __name__ == '__main__':
    engine = get_db_engine()
    dim_museum_driver(engine)