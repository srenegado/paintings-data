CREATE TABLE IF NOT EXISTS dim_artist (
    dim_artist_skey serial PRIMARY KEY,
    artist_id integer,
    full_name text,
    nationality text,
    style text,
    birth_year integer,
    death_year integer
);
