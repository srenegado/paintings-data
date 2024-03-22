# init_presentation.py
#
# Script to populate presentation area with tables.
#
# Scott Renegado

from pipelines.resources.connection import get_db_engine
from pipelines.dim_artist.driver import dim_artist_driver
from pipelines.dim_canvas.driver import dim_canvas_driver
from pipelines.dim_concept.driver import dim_concept_driver
from pipelines.dim_museum.driver import dim_museum_driver
from pipelines.fact_artwork.driver import fact_artwork_driver
from pipelines.fact_museum_hours.driver import fact_museum_hours_driver


def main():
    engine = get_db_engine()

    print("Preparing Presentation Area")

    print("> Setting up dimension tables")
    dim_artist_driver(engine)
    dim_canvas_driver(engine)
    dim_concept_driver(engine)
    dim_museum_driver(engine)

    print("> Setting up fact tables")
    fact_artwork_driver(engine)
    fact_museum_hours_driver(engine)


if __name__ == "__main__":
    main()
