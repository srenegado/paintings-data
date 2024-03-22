# driver.py
#
# Driver for dim_concept table in presentation area.
#
# Scott Renegado

from pipelines.presentation_driver import presentation_driver
from pipelines.resources.connection import get_db_engine


def dim_concept_driver(engine):
    """Driver for dim_concept table."""
    presentation_driver(engine, "dim_concept")


if __name__ == "__main__":
    dim_concept_driver(get_db_engine())
