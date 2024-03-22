# load_csv_to_postgres.py
#
# Loads csv files to postgresql database.
# Before running, create the db!
#
# Scott Renegado
# Modified from: https://www.youtube.com/watch?v=AZ29DXaJ1Ts

import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# Connect to database - modify as needed
user = "postgres"
pw = "pokemon"
db_name = "paintings"
conn_string = f"postgresql://{user}:{pw}@localhost/{db_name}"

db = create_engine(conn_string)
conn = db.connect()

# Store csv names in a list
csv_filenames = Path("data/")
csv_basenames = [csv_filename.stem for csv_filename in csv_filenames.iterdir()]

# Load csvs as tables into DB
for csv_basename in csv_basenames:

    # Read csv into dataframe
    df = pd.read_csv(f"data/{csv_basename}.csv")

    # Load dataframe to sql table
    df.to_sql(csv_basename, con=conn, if_exists="replace", index=False)

conn.close()
