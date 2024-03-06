CREATE TABLE IF NOT EXISTS dim_artist (
    id integer PRIMARY KEY,
    full_name text,
    nationality text,
    style text,
    birth_year integer,
    death_year integer
);