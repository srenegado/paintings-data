CREATE TABLE museum_hours (
	museum_id integer REFERENCES museum,
	day text,
	open time,
	close time,
	PRIMARY KEY (museum_id, day)
);