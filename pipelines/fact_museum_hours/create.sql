CREATE TABLE IF NOT EXISTS fact_museum_hours (
	dim_museum_skey integer REFERENCES dim_museum,
	day text,
	opening_hours time,
	closing_hours time,
	PRIMARY KEY (dim_museum_skey, day)
);