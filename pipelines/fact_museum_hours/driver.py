# driver.py
#
# Driver for fact_museum_hours table in presentation area.
#
# Scott Renegado

from pipelines.presentation_driver import presentation_driver
from pipelines.resources.connection import get_db_engine


def fact_museum_hours_driver(engine):
    """Driver for fact_museum_hours table."""
    presentation_driver(engine, "fact_museum_hours")


if __name__ == "__main__":
    fact_museum_hours_driver(get_db_engine())
