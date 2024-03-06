# driver.py
#
# Driver for fact_museum_hours table in presentation area.
#
# Scott Renegado

from pipelines.resources.connection import get_db_engine
from pipelines.resources.connection import get_db_connection
from pipelines.resources.sqlhandler import execute_script
from pipelines.resources.sqlhandler import read_local_sql


def fact_museum_hours_driver(engine):

    # Connect to database
    print("Establishing a database connection...")
    conn = get_db_connection(engine)

    # Create the fact_museum_hours table
    execute_script("pipelines/fact_museum_hours/create.sql", con=conn)

    # Read table into dataframe
    df = read_local_sql("pipelines/fact_museum_hours/load.sql", con=conn)

    # Load dataframe into table
    df.to_sql('fact_museum_hours', con=conn, if_exists='append', index=False)

    # Create indexes
    execute_script("pipelines/fact_museum_hours/indexes.sql", con=conn)

    # Commit transanctions to DB
    conn.commit()

    if conn:
        print("Closing database connection...")
        conn.close()


if __name__ == '__main__':
    engine = get_db_engine()
    fact_museum_hours_driver(engine)