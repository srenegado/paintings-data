# staging.py
#
# Script to populate staging area with tables.
#
# Scott Renegado

from pipelines.resources.connection import get_db_engine
from pipelines.artist.driver import artist_driver
from pipelines.canvas.driver import canvas_driver
from pipelines.museum.driver import museum_driver
from pipelines.museum_hours.driver import museum_hours_driver
from pipelines.product.driver import product_driver
from pipelines.work.driver import work_driver
from pipelines.work_subject.driver import work_subject_driver


def main():
    engine = get_db_engine()

    print("Preparing Staging Area")

    artist_driver(engine)
    museum_driver(engine)
    work_driver(engine)
    museum_hours_driver(engine)
    work_subject_driver(engine)
    canvas_driver(engine)
    product_driver(engine)


if __name__ == "__main__":
    main()
