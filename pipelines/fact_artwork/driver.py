# driver.py
#
# Driver for fact_artwork table in presentation area.
#
# Scott Renegado

from pipelines.presentation_driver import presentation_driver
from pipelines.resources.connection import get_db_engine


def fact_artwork_driver(engine):
    """Driver for fact_artwork table."""
    presentation_driver(engine, 'fact_artwork')

if __name__ == '__main__':
    fact_artwork_driver(get_db_engine())