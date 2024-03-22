# driver.py
#
# Driver for dim_canvas table in presentation area.
#
# Scott Renegado

from pipelines.presentation_driver import presentation_driver
from pipelines.resources.connection import get_db_engine


def dim_canvas_driver(engine):
    """Driver for dim_canvas table."""
    presentation_driver(engine, "dim_canvas")


if __name__ == "__main__":
    engine = get_db_engine()
    dim_canvas_driver(engine)
