CREATE TABLE work (
	id integer PRIMARY KEY,
	name text,
	style text,
	artist_id integer REFERENCES artist,
	museum_id integer REFERENCES museum
);