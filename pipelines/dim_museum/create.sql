CREATE TABLE IF NOT EXISTS dim_museum (
	dim_museum_skey serial PRIMARY KEY,
	museum_id integer,
	name text,
	address text,
	city text,
	state text,
	postal text,
	country text,
	phone text
);